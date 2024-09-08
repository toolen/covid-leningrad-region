"""This file contains methods to work with email."""

import smtplib
from email.mime.text import MIMEText
from typing import cast

from scraper.config import ADMIN_EMAIL, DEFAULT_FROM_EMAIL, EMAIL_URL


def send_message_to_admin(text: str) -> None:
    """
    Send email to application admin.

    :param text: mail message.
    :return: None
    """
    sender_mail = DEFAULT_FROM_EMAIL

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = "[scraper] an error occurred"
    msg["From"] = sender_mail
    msg["To"] = ADMIN_EMAIL

    host = cast(str, EMAIL_URL["EMAIL_HOST"])
    port = cast(int, EMAIL_URL["EMAIL_PORT"])
    login = cast(str, EMAIL_URL["EMAIL_HOST_USER"])
    password = cast(str, EMAIL_URL["EMAIL_HOST_PASSWORD"])
    use_ssl = cast(bool, EMAIL_URL["EMAIL_USE_SSL"])

    server = smtplib.SMTP_SSL(host, port) if use_ssl else smtplib.SMTP(host, port)
    server.ehlo(host)
    server.set_debuglevel(1)

    if login and password:
        server.login(login, password)

    server.sendmail(sender_mail, ADMIN_EMAIL, msg.as_string())
    server.quit()
