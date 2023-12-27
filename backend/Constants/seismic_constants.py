from enum import Enum


class SiteClass(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

    def __str__(self):
        return self.value


class SiteDesignation(Enum):
    XV = 'xv'
    XS = 'xs'

    def __str__(self):
        return self.value
