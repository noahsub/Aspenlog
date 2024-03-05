from pydantic import BaseModel


class RegisterInput(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: str
