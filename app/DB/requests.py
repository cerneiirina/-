from app.DB.models import async_session
from app.DB.models import User, Category, Item
from app.DB.models import Item, async_session
from sqlalchemy import select

async def set_user(tg_id: int) -> None:
    """Add a user if they don't exist in the database."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
async def get_categories() -> list[Category]:
    """Retrieve all categories from the database."""
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result.all()  # `.all()` will work now as `result` is no longer a coroutine

async def get_item(item_id: int) -> Item:
    """Retrieve a single item by its ID."""
    async with async_session() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        return result.scalar()
    

async def get_category_items(category_id: int):
    """Retrieve all items within a specified category."""
    async with async_session() as session:
        result = await session.scalars(select(Item).where(Item.category == category_id))
        return result.all()
    


        