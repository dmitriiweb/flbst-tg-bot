from __future__ import annotations

import sqlalchemy as sa
from aiogram import types as tg_types
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas


async def get_or_create_user(
    session: AsyncSession, user_id: int, message: tg_types.Message
) -> schemas.User:
    user_obj = await get_user_by_id(session, user_id)
    if user_obj:
        return user_obj

    new_user_data = deserialize_telegram_object_to_python(message.from_user)
    new_user_data["user_id"] = new_user_data.pop("id")
    new_user = schemas.NewUser(**new_user_data)
    user = models.User(**new_user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return schemas.User.model_validate(user)


async def get_user_by_id(session: AsyncSession, user_id: int) -> schemas.User | None:
    user_stmt = sa.select(models.User).where(models.User.user_id == user_id)
    user_res = await session.execute(user_stmt)
    user_record = user_res.scalars().first()
    return schemas.User.model_validate(user_record) if user_record else None
