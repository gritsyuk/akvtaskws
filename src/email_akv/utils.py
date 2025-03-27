from typing import List
from email_validator import validate_email, EmailNotValidError
import logging


def read_valid_emails(file_path: str) -> List[str | None]:
    valid_emails = []
    with open(file_path, 'r') as file:
        for line in file:
            email_line = line.strip()
            try:
                email_info = validate_email(email_line, check_deliverability=False)
                email = email_info.normalized
                valid_emails.append(email)
            except EmailNotValidError as e:
                logging.error(f"EMAIL: Invalid email: {email}")

    return valid_emails
