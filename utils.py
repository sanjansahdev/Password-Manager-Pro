# ==========================================
# Password Manager Utility Functions
# ==========================================


def display_section(title):
    """
    Display a formatted section heading.
    """

    print("\n" + "-" * 45)
    print(f" {title}")
    print("-" * 45)


def pause():
    """
    Pause the program until the user presses Enter.
    """

    input("\nPress Enter to continue...")


def validate_required_fields(*fields):
    """
    Check whether all provided fields contain values.

    Returns:
        True  -> All fields are valid.
        False -> At least one field is empty.
    """

    return all(
        str(field).strip()
        for field in fields
    )


def validate_password_length(password, minimum=8):
    """
    Check whether a password meets the minimum length.
    """

    return len(password) >= minimum