import psycopg2

class ConnectionInfo:
    host: str
    port: int
    username: str
    password: str
    database_name: str