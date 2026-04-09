import enum


class ClientType(str, enum.Enum):
    """
    confidential: server-side web apps, backend services
    public: cannot keep a secret (SPAs, mobile apps). Must use PKCE.
    """

    CONFIDENTIAL = "confidential"
    PUBLIC = "public"


class MFAMethod(str, enum.Enum):
    TOTP = "totp"
    EMAIL = "email"
    SMS = "sms"
    NONE = "none"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
