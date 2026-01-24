from app.crud import create_item, get_items
from app.schemas import ItemCreate

def test_create_item(db_session):
    item = ItemCreate(
        name ="crud-test",
        description="created via crud"
    )

    db_item = create_item(db_session, item)

    assert db_item.id is not None
    assert db_item.name == "crud-test"
    assert db_item.description == "created via crud"

def test_get_items(db_session):
    item1 = ItemCreate(name="one", desctiption="first")
    item2 = ItemCreate(name="two", description="second")

    create_item(db_session, item1)
    create_item(db_session, item2)

    items = get_items(db_session)

    assert len(items) == 2
    names = [item.name for item in items]
    assert "one" in names
    assert "two in names"

