from app.models import  Item

def test_item_model_feilds():
    assert Item.__tablename__== "items"

    columns = Item.__table__.columns
    assert "id" in columns
    assert "name" in columns
    assert "description" in columns