from enum import Enum


class StatementStatus(Enum):
    PENDING = 0
    CONSIDERED = 1
    DONE = 2
    REFUSED = 3
