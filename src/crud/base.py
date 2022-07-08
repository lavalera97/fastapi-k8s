import operator
from typing import Any

import sqlalchemy as sa

from db.database import database


class BaseCRUD:
    """Basic crud class"""
    database = database

    def __init__(self, model, result_model):
        self.model = model
        self.result_model = result_model

    def _construct_by_field_clause(self, data: dict):
        expressions = []
        negation_clause_mark = '__not'
        for field_name, field_value in data.items():
            is_negation_clause = False
            if field_name.endswith(negation_clause_mark):
                is_negation_clause = True
                field_name = field_name.split(negation_clause_mark)[0]
            if field_name in self.model.__table__.columns:
                if is_negation_clause:
                    clause_operator = operator.ne
                else:
                    clause_operator = operator.eq
                expressions.append(clause_operator(getattr(self.model, field_name), field_value))
        return sa.and_(*expressions)

    async def get(self, item_id: Any):
        query = sa.select(self.model).where(self.model.id == item_id)
        result = await self.database.fetch_one(query=query)
        if result is None:
            return None
        return self.result_model.parse_obj(result)

    async def get_by_data(self, **kwargs):
        where = [self._construct_by_field_clause(kwargs)]
        query = sa.select(self.model).where(sa.and_(*where))
        result = await self.database.fetch_all(query=query)
        return [self.result_model.parse_obj(item) for item in result]

    async def create(self, obj_data):
        query = sa.insert(self.model).returning(*self.model.__table__.columns)
        result = await self.database.fetch_one(query=query, values=obj_data.dict())
        if not result:
            return
        return self.result_model.parse_obj(result)

    async def update(self, item_id, obj_data):
        if isinstance(obj_data, dict):
            update_data = obj_data
        else:
            update_data = obj_data.dict(exclude_unset=True)
        query = sa.update(self.model).where(self.model.id == item_id).returning(*self.model.__table__.columns)
        result = await self.database.fetch_one(query=query, values=update_data)
        return self.result_model.parse_obj(result)

    async def delete(self, item_id: Any):
        query = sa.delete(self.model).where(self.model.id == item_id).returning(*self.model.__table__.columns)
        return await self.database.fetch_one(query=query)
