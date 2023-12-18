from enum import Enum


class PrivilegeType(Enum):
    ADMIN: str = 'admin'
    WRITE: str = 'write'
    READ: str = 'read'
