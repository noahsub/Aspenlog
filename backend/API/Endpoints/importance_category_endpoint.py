from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.importance_category_manager import process_importance_category_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_importance_category
from backend.API.Models.importance_category_input import ImportanceCategoryInput

importance_category_router = APIRouter()


@importance_category_router.post("/importance_category")
def importance_category_endpoint(importance_category_input: ImportanceCategoryInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        importance_category = process_importance_category_data(importance_category_input.importance_category)
        set_user_importance_category(username=username, importance_category=importance_category)
        return importance_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
