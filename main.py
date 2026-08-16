import msvcrt

from database import (
    create_tables,
    add_credential,
    get_credentials,
    search_credentials,
    update_credential,
    delete_credential
)

from password_generator import (
    generate_password,
    check_password_strength
)

from security import (
    master_password_exists,
    create_master_password,
    verify_master_password
)

from logger import (
    log_info,
    log_error,
    log_warning
)

from utils import (
    display_section,
    validate_required_fields,
    validate_password_length,
    pause
)


# ==========================================
# Masked Password Input
# ==========================================

def masked_input(prompt="Password: "):

    print(prompt, end="", flush=True)

    password = ""

    while True:

        char = msvcrt.getwch()

        # Enter
        if char in ("\r", "\n"):

            print()

            return password

        # Backspace
        elif char == "\b":

            if password:

                password = password[:-1]

                print(
                    "\b \b",
                    end="",
                    flush=True
                )

        # Special / Function keys
        elif char in ("\x00", "\xe0"):

            msvcrt.getwch()

        # Normal character
        else:

            password += char

            print(
                "*",
                end="",
                flush=True
            )


# ==========================================
# Display Banner
# ==========================================

def display_banner():

    print("\n" + "=" * 45)
    print("        PASSWORD MANAGER PRO")
    print("=" * 45)


# ==========================================
# Master Password Authentication
# ==========================================

def authenticate_user():

    display_section("MASTER PASSWORD")

    # First-time setup
    if not master_password_exists():

        print("\nNo master password found.")
        print("Let's create one.")

        password = masked_input(
            "\nCreate master password: "
        )

        confirm_password = masked_input(
            "Confirm master password: "
        )

        if password != confirm_password:

            print("\nPasswords do not match.")

            log_warning(
                "Master password confirmation failed."
            )

            return False

        if not validate_password_length(
            password,
            minimum=6
        ):

            print(
                "\nPassword must contain at least 6 characters."
            )

            log_warning(
                "Master password rejected: too short."
            )

            return False

        create_master_password(password)

        print(
            "\nMaster password created successfully!"
        )

        log_info(
            "Master password created successfully."
        )

        return True

    # Existing user
    password = masked_input(
        "\nEnter master password: "
    )

    if verify_master_password(password):

        print("\nAccess granted!")

        log_info(
            "User authenticated successfully."
        )

        return True

    print("\nIncorrect master password.")

    log_warning(
        "Failed master password authentication attempt."
    )

    return False


# ==========================================
# Display Menu
# ==========================================

def display_menu():

    print("\n1. Add Credential")
    print("2. View Credentials")
    print("3. Search Credential")
    print("4. Update Credential")
    print("5. Delete Credential")
    print("6. Generate Password")
    print("7. Check Password Strength")
    print("8. Exit")


# ==========================================
# Add Credential
# ==========================================

def add_credential_menu():

    display_section("ADD CREDENTIAL")

    website = input(
        "Website: "
    ).strip()

    username = input(
        "Username: "
    ).strip()

    password = masked_input(
        "Password: "
    ).strip()

    if not validate_required_fields(
        website,
        username,
        password
    ):

        print("\nAll fields are required.")

        log_warning(
            "Credential addition failed: missing field."
        )

        return

    try:

        add_credential(
            website,
            username,
            password
        )

        print(
            "\nCredential saved successfully!"
        )

        log_info(
            f"Credential added: {website}"
        )

    except Exception as error:

        print(
            "\nFailed to save credential."
        )

        log_error(
            f"Failed to add credential for {website}: {error}"
        )


# ==========================================
# View Credentials
# ==========================================

def view_credentials():

    display_section("SAVED CREDENTIALS")

    try:

        credentials = get_credentials()

        if not credentials:

            print("\nNo credentials found.")

            log_info(
                "Viewed credentials: no credentials found."
            )

            return

        for credential in credentials:

            print("\n" + "-" * 45)

            print(f"ID       : {credential[0]}")
            print(f"Website  : {credential[1]}")
            print(f"Username : {credential[2]}")
            print(f"Password : {credential[3]}")
            print(f"Created  : {credential[4]}")

        print("-" * 45)

        log_info(
            "Credentials viewed successfully."
        )

    except Exception as error:

        print(
            "\nFailed to retrieve credentials."
        )

        log_error(
            f"Failed to retrieve credentials: {error}"
        )


# ==========================================
# Search Credential
# ==========================================

def search_credential_menu():

    display_section("SEARCH CREDENTIAL")

    search_term = input(
        "Enter website: "
    ).strip()

    if not search_term:

        print(
            "\nSearch term cannot be empty."
        )

        log_warning(
            "Credential search failed: empty search term."
        )

        return

    try:

        credentials = search_credentials(
            search_term
        )

        if not credentials:

            print(
                "\nNo matching credentials found."
            )

            log_info(
                f"No search results for: {search_term}"
            )

            return

        for credential in credentials:

            print("\n" + "-" * 45)

            print(f"ID       : {credential[0]}")
            print(f"Website  : {credential[1]}")
            print(f"Username : {credential[2]}")
            print(f"Password : {credential[3]}")
            print(f"Created  : {credential[4]}")

        print("-" * 45)

        log_info(
            f"Credential search completed: {search_term}"
        )

    except Exception as error:

        print(
            "\nSearch failed."
        )

        log_error(
            f"Credential search failed for {search_term}: {error}"
        )


# ==========================================
# Update Credential
# ==========================================

def update_credential_menu():

    display_section("UPDATE CREDENTIAL")

    try:

        credential_id = int(
            input("Enter credential ID: ")
        )

    except ValueError:

        print(
            "\nPlease enter a valid ID."
        )

        log_warning(
            "Credential update failed: invalid ID."
        )

        return

    website = input(
        "New website: "
    ).strip()

    username = input(
        "New username: "
    ).strip()

    password = masked_input(
        "New password: "
    ).strip()

    if not validate_required_fields(
        website,
        username,
        password
    ):

        print(
            "\nAll fields are required."
        )

        log_warning(
            f"Credential update failed for ID {credential_id}: missing field."
        )

        return

    try:

        updated = update_credential(
            credential_id,
            website,
            username,
            password
        )

        if updated:

            print(
                "\nCredential updated successfully!"
            )

            log_info(
                f"Credential updated: ID {credential_id}"
            )

        else:

            print(
                "\nCredential ID not found."
            )

            log_warning(
                f"Credential update failed: ID {credential_id} not found."
            )

    except Exception as error:

        print(
            "\nFailed to update credential."
        )

        log_error(
            f"Failed to update credential ID {credential_id}: {error}"
        )


# ==========================================
# Delete Credential
# ==========================================

def delete_credential_menu():

    display_section("DELETE CREDENTIAL")

    try:

        credential_id = int(
            input("Enter credential ID: ")
        )

    except ValueError:

        print(
            "\nPlease enter a valid ID."
        )

        log_warning(
            "Credential deletion failed: invalid ID."
        )

        return

    confirm = input(
        "Are you sure you want to delete this credential? (y/n): "
    ).strip().lower()

    if confirm != "y":

        print(
            "\nDeletion cancelled."
        )

        log_info(
            f"Credential deletion cancelled: ID {credential_id}"
        )

        return

    try:

        deleted = delete_credential(
            credential_id
        )

        if deleted:

            print(
                "\nCredential deleted successfully!"
            )

            log_info(
                f"Credential deleted: ID {credential_id}"
            )

        else:

            print(
                "\nCredential ID not found."
            )

            log_warning(
                f"Credential deletion failed: ID {credential_id} not found."
            )

    except Exception as error:

        print(
            "\nFailed to delete credential."
        )

        log_error(
            f"Failed to delete credential ID {credential_id}: {error}"
        )


# ==========================================
# Generate Password
# ==========================================

def generate_password_menu():

    display_section("PASSWORD GENERATOR")

    try:

        length = int(
            input("Password length: ")
        )

        if not validate_password_length(
            "A" * length,
            minimum=8
        ):

            print(
                "\nPassword length should be at least 8."
            )

            log_warning(
                "Password generation rejected: length below 8."
            )

            return

        password = generate_password(
            length
        )

        print(
            "\nGenerated Password:"
        )

        print(password)

        log_info(
            f"Password generated successfully: length {length}"
        )

    except ValueError:

        print(
            "\nPlease enter a valid number."
        )

        log_warning(
            "Password generation failed: invalid length."
        )

    except Exception as error:

        print(
            "\nFailed to generate password."
        )

        log_error(
            f"Password generation error: {error}"
        )


# ==========================================
# Password Strength Checker
# ==========================================

def password_strength_menu():

    display_section(
        "PASSWORD STRENGTH CHECKER"
    )

    password = input(
        "Enter password to check: "
    )

    if not password:

        print(
            "\nPassword cannot be empty."
        )

        return

    strength = check_password_strength(
        password
    )

    print(
        "\nPassword Strength:"
    )

    print(strength)

    log_info(
        f"Password strength checked: {strength}"
    )


# ==========================================
# Main Application
# ==========================================

def main():

    log_info(
        "Password Manager application started."
    )

    create_tables()

    display_banner()

    if not authenticate_user():

        print(
            "\nAccess denied."
        )

        print(
            "Exiting Password Manager..."
        )

        log_warning(
            "Application access denied."
        )

        return

    while True:

        display_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            add_credential_menu()

        elif choice == "2":

            view_credentials()

        elif choice == "3":

            search_credential_menu()

        elif choice == "4":

            update_credential_menu()

        elif choice == "5":

            delete_credential_menu()

        elif choice == "6":

            generate_password_menu()

        elif choice == "7":

            password_strength_menu()

        elif choice == "8":

            print(
                "\nThank you for using Password Manager Pro."
            )

            print(
                "Goodbye!"
            )

            log_info(
                "Password Manager application closed."
            )

            break

        else:

            print(
                "\nInvalid choice. Please try again."
            )

            log_warning(
                f"Invalid menu choice: {choice}"
            )


# ==========================================
# Program Entry Point
# ==========================================

if __name__ == "__main__":

    main()