# What this file is responsible for: 
# Expose HTTP endpoints 
# Validate input Call business logic (CRUD) 
# Handle errors 
# NOT manage DB connections directly

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session

from app import schemas, crud
from app.db import SessionLocal

router = APIRouter()

# db dependency
# implementation of the Dependency Injection pattern in FastAPI for managing database connections.
# when a request hits a route that needs the database, db = SessionLocal() creates a new connection instance
# this matters because it prevents cnnection leaks and works perfectly eith kubernetes scaling. FastAPI injects this automatically
def get_db():
    """
    creates a new db session per request
    and closes it after the request finishes.

    """
    db = SessionLocal()
    try:
        # Instead of return, it uses yield. This "pauses" the function and hands the active database session to your route function.
        # Your code performs its queries (GET, POST, etc.) using that session.
        # Once the route finishes (whether it succeeds or crashes with an error), the code "unpauses" and executes db.close(). This returns the connection to the pool so the database doesn't run out of available slots.
        yield db
    finally:
        db.close()

# create item:
@router.post(
    "/items",
    # response_model=schemas.ItemRead: This is your Data Filter. Even if your database has internal fields (like hashed_password or internal_notes), FastAPI will strip them out and only return the fields defined in ItemRead.
    response_model=schemas.ItemRead,
    status_code=status.HTTP_201_CREATED
)
def create_item(
    item: schemas.ItemCreate,
    # Depends(get_db): This ensures your database connection is automatically managed and closed.
    db: session = Depends(get_db)
):
    return crud.create_item(db,item)

# list item:
@router.get(
    "/items",
    response_model=list[schemas.ItemRead]
)
def list_items(
    db: session = Depends(get_db)
):
    return crud.get_items(db)

# get single item:
@router.get(
    "/items/{item_id}",
    response_model=schemas.ItemRead
)
def get_item(
    item_id: int,
    db: session = Depends(get_db)
):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="item not found"
        )
    return item

# update item
@router.put(
    "/item/{item_id}",
    response_model=schemas.ItemRead
)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: session = Depends(get_db)
):
    updated = crud.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "item not found"
        )
    return updated

# delete item
@router.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_item(
    item_id = int,
    db: session = Depends(get_db)
):
    deleted = crud.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="item not found"
        )
    
