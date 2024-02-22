from backend.Constants.importance_factor_constants import ImportanceFactor


def process_importance_category_data(importance_category: str):
    match importance_category:
        case 'LOW':
            return ImportanceFactor.LOW
        case 'NORMAL':
            return ImportanceFactor.NORMAL
        case 'HIGH':
            return ImportanceFactor.HIGH
        case 'POST_DISASTER':
            return ImportanceFactor.POST_DISASTER
