import pytest
from pydantic import ValidationError
from app.schemas import ItemCreate, ItemRead

# valid input test
def test_item_create_valid():
    item = ItemCreate(
        name="book",
        description="tech book"
    )

    assert item.name == "book"
    assert item.description == "tech book"

# empty name should fail
def test_item_create_empty_name():
    with pytest.raises(ValidationError):
        ItemCreate(
            name="",
            description="Invalid"
        )

# missing name should fail
def test_item_missing_name():
    with pytest.raises(ValidationError):
        ItemCreate(description="missing name")

# response schema mapping
def test_item_response_schema():
    data = {
        "id" : 1,
        "name" : "pen",
        "description" : "blue pen"
    }

    item = ItemRead(**data)

    assert item.id == 1
    assert item.name == "pen"
