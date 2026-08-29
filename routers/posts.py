from fastapi import APIRouter, HTTPException, status, Depends, Query
from schema import PostCreate,PostResponse,PostUpdate, PaginatedPostsResponse
from typing import Annotated
from database import get_db
import model
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from auth import CurrentUser
from config import setting

router = APIRouter()



# Create

@router.post('',response_model=PostResponse,status_code=status.HTTP_201_CREATED)
async def create_post(post:PostCreate, current_user: CurrentUser , db: Annotated[AsyncSession,Depends(get_db)]):

    new_post = model.Post(
        title= post.title,
        content = post.content,
        user_id = current_user.id
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=['author'])
    return new_post



# RETRIEVE

@router.get("", response_model=PaginatedPostsResponse)
async def get_posts(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = setting.posts_per_page,
):

    count_result = await db.execute(select(func.count()).select_from(model.Post))
    total = count_result.scalar() or 0

    result = await db.execute(
        select(model.Post)
        .options(selectinload(model.Post.author))
        .order_by(model.Post.date_posted.desc())
        .offset(skip)
        .limit(limit),
    )
    posts = result.scalars().all()

    has_more = skip + len(posts) < total

    return PaginatedPostsResponse(
        posts=[PostResponse.model_validate(post) for post in posts],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )




@router.get("/{post_id}",response_model=PostResponse)
async def get_post(post_id: int, db: Annotated[AsyncSession,Depends(get_db)]):
    
    result = await db.execute(select(model.Post).options(selectinload(model.Post.author)).where(model.Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post



# UPDATE

# update full post     here we used put for full update of the post
@router.put('/{post_id}', response_model=PostResponse)
async def update_full_post(post_id:int , post_data:PostCreate,current_user: CurrentUser , db: Annotated[AsyncSession,Depends(get_db)]):

    #post authentication
    result = await db.execute(select(model.Post).where(model.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # ownership check
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    post.title = post_data.title
    post.content = post_data.content

    await db.commit()
    await db.refresh(post, attribute_names=['author'])

    return post




# post partial update          patch is used
@router.patch('/{post_id}', response_model=PostResponse)
async def update_partial_post(post_id:int, current_user: CurrentUser, post_data:PostUpdate, db: Annotated[AsyncSession,Depends(get_db)]):

    #post authentication
    result = await db.execute(select(model.Post).where(model.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


    # ownership check
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")


    #update the attribute
    updated_post = post_data.model_dump(exclude_unset=True)
    for key,val in updated_post.items():
        setattr(post,key,val)

    await db.commit()
    await db.refresh(post, attribute_names=['author'])

    return post



# DELETE

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int, current_user:CurrentUser, db:Annotated[AsyncSession, Depends(get_db)]):

    result = await db.execute(select(model.Post).where(model.Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="post not found")

    # ownership check
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    
    await db.delete(post)
    await db.commit()