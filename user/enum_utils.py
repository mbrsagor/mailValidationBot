from enum import IntEnum

class UserRole(IntEnum):
    ADMIN    = 1
    EDITOR = 2
    AUTHOR = 3
    SUBSCRIBER = 4

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]


class Gender(IntEnum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

    @classmethod
    def get_gender(cls):
        return [(key.value, key.name) for key in cls]
