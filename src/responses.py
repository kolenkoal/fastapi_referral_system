from fastapi import status
from fastapi_users.router.common import ErrorCode, ErrorModel


UNAUTHORIZED_RESPONSE = {
    status.HTTP_401_UNAUTHORIZED: {
        "content": {
            "application/json": {
                "examples": {
                    "Unauthorized.": {
                        "summary": "A user is not authorized.",
                        "value": {"detail": "Unauthorized."},
                    },
                }
            }
        }
    }
}

REFERRAL_CODE_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Referral Code Not Found.": {
                        "summary": "Referral Code Not Found.",
                        "value": {"detail": "Referral Code Not Found."},
                    },
                }
            }
        }
    }
}

REFERRER_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Referrer Not Found.": {
                        "summary": "Referrer Not Found.",
                        "value": {"detail": "Referrer Not Found."},
                    },
                }
            }
        }
    }
}

FORBIDDEN_RESPONSE = {
    status.HTTP_403_FORBIDDEN: {
        "content": {
            "application/json": {
                "examples": {
                    "Forbidden.": {
                        "summary": "Forbidden.",
                        "value": {"detail": "Forbidden."},
                    },
                }
            }
        }
    },
}

EMAIL_NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "examples": {
                    "Email Not Found.": {
                        "summary": "Email Not Found.",
                        "value": {"detail": "Email  Not Found."},
                    },
                }
            }
        }
    }
}

UNAUTHORIZED_REFERRAL_CODE_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **REFERRAL_CODE_NOT_FOUND_RESPONSE,
}

UNAUTHORIZED_FORBIDDEN_REFERRER_NOT_FOUND_RESPONSE = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **REFERRER_NOT_FOUND_RESPONSE,
}

REGISTER_NOT_FOUND_RESPONSE = (
    {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
