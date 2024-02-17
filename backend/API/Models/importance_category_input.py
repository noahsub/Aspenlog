from pydantic import BaseModel


class ImportanceCategoryInput(BaseModel):
    importance_category: str
