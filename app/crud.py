# crud.py is where your actual business logic lives.
# What this file is responsible for:
# Creating database records
# Fetching data
# Updating entities
# Deleting entities
# Handling database-level behavior

# Design Principles Used:
# One function per DB operation 
# Explicit DB session passing 
# No global state
# Predictable return values

from sqlalchemy.orm import Session
from app import models, schemas

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(
        name=item.name,
        description=item.description
    )
    # This places the db_item object into the session's "pending" state. Crucially: It has not been saved to the database yet. It is essentially sitting in an "outbox," waiting to be sent.
    db.add(db_item)
    # This sends the actual INSERT command to the database and finalizes the transaction. If you have made multiple db.add() calls, db.commit() saves them all at once. If any part of the save fails, the database remains unchanged (Atomic property).
    db.commit()
    # pulls DB-generated values (like id), ensures returned object is fully populated. 
    db.refresh(db_item)
    return db_item

# why pagination defaults:
# protects DB from large reads
# CI and production-safe
def get_items(db:Session, skip: int = 0, limit: int = 100):
    return (
        #  Generates the base SQL SELECT statement. It tells the database, "I want to retrieve data from the table associated with the Item model."
        # SQL equivalent: SELECT * FROM items;
        db.query(models.Item)
        # Tells the database how many rows to ignore from the top of the list.
        #  If skip=20, the database will skip the first 20 records and start from the 21st.
        # SQL equivalent: OFFSET 20
        .offset(skip)
        # Tells the database the maximum number of rows to return.
        # Use Case: If limit=10, even if there are 1,000 items in the table, you will only receive 10.
        # SQL equivalent: LIMIT 10
        .limit(limit)
        # This is the execution command.
        # Up until this point, the query was just a "plan." .all() triggers the actual communication with the database, retrieves the rows, and converts them into a Python list of objects.
        # Return Type: List[models.Item]
        .all()
    )

def get_item(db:Session, item_id: int):
    return (
        db.query(models.Item)
        # Adds a WHERE clause to your SQL query. It tells the database to only look for rows where the id column matches the item_id variable you provided.
        # SQL Equivalent: WHERE items.id = 5;
        .filter(models.Item.id == item_id)
        #  Executes the query and returns only the first result found. If a match is found, it returns the single Python object (not a list). If no match is found, it returns None.
        .first()
    )

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        # let api layer decide htttp response
        # clean seperation of concerns
        return None
    
    db_item.name = item.name
    db_item.description = item.description

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id:int):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    db.delete(db_item)
    db.commit()
    return db_item
