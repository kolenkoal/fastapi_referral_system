import secrets


def generate_referral_code():
    return secrets.token_urlsafe(7)
