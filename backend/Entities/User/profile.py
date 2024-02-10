class Profile:
    username: str
    first_name: str
    last_name: str
    email: str

    def __init__(self, username: str, first_name: str, last_name: str, email: str):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
