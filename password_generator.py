import secrets
import string


# ==========================================
# Generate Secure Password
# ==========================================

def generate_password(length=16):

    if length < 8:
        raise ValueError(
            "Password length must be at least 8 characters."
        )

    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}"

    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    all_characters = (
        uppercase
        + lowercase
        + digits
        + symbols
    )

    for _ in range(length - 4):
        password.append(
            secrets.choice(all_characters)
        )

    secrets.SystemRandom().shuffle(password)

    return "".join(password)


# ==========================================
# Check Password Strength
# ==========================================

def check_password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(
        char in string.punctuation
        for char in password
    ):
        score += 1

    if score <= 2:
        return "WEAK"

    elif score <= 4:
        return "MEDIUM"

    else:
        return "STRONG"