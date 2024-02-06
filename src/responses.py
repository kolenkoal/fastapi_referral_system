from fastapi import status


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
