# Creating a Revision with Alembic 📝

1. **Create a new revision**:
   Use the `alembic revision` command to create a new migration script. The `--autogenerate` flag will automatically detect changes to your models and generate the appropriate migration script.

   ```bash
   alembic revision --autogenerate -m "Add Item model"
   ```

   This will create a new file in the `alembic/versions/` directory. The filename will include a unique identifier and the message you provided.

## Applying the Migration (Upgrade) 🚀

1. **Apply the latest migration**:
   Use the `alembic upgrade` command to apply the latest migration to the database.

   ```bash
   alembic upgrade head
   ```

   The `head` keyword refers to the latest revision. You can also specify a specific revision identifier if needed.

## Rolling Back the Migration (Downgrade) ⏪

1. **Downgrade to the previous revision**:
   Use the `alembic downgrade` command to revert the database to a previous state. The `-1` specifies to go back one revision.

   ```bash
   alembic downgrade -1
   ```

   You can also specify a specific revision identifier to downgrade to a particular state.

## Full Example

1. **Add a new model to your `models.py`**:

   ```python
   # models.py
   from sqlalchemy import Column, Integer, String
   from .database import Base

   class Item(Base):
       __tablename__ = "items"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
       description = Column(String, index=True)
   ```

2. **Create a new revision**:

   ```bash
   alembic revision --autogenerate -m "Add Item model"
   ```

   This generates a new migration script in `alembic/versions/`.

3. **Apply the migration**:

   ```bash
   alembic upgrade head
   ```

4. **Check the status**:

   You can check the current status of the migrations with:

   ```bash
   alembic current
   ```

5. **Downgrade the migration**:

   ```bash
   alembic downgrade -1
   ```

6. **Apply the migration again**:

   ```bash
   alembic upgrade head
   ```

## Summary

You have now created a new revision with Alembic, applied it to the database, and learned how to downgrade and upgrade the database schema. This workflow allows you to manage changes to your database schema efficiently and safely.
