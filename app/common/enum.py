import enum


class MFAMethod(str, enum.Enum):
    TOTP = "totp"
    EMAIL = "email"
    SMS = "sms"
    NONE = "none"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
