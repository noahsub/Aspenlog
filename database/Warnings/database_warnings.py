import warnings


class AlreadyExistsWarning(Warning):
    pass


def already_exists_warning(item: str, database_name: str):
    # Creating a custom warning using a custom warning class
    warnings.warn(f"{item} already exists in {database_name}", category=AlreadyExistsWarning)
