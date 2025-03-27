import logging
import aiosmtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .settings import (
    EMAIL_SENDER, 
    EMAIL_SENDER_PASSWORD
    )


class EmailSender:
    def __init__(self, email_sender: str = EMAIL_SENDER,
                 password: str = EMAIL_SENDER_PASSWORD,
                 smtp_server: str = 'smtp.mail.ru',
                 port: int = 465):
        self.email_sender = email_sender
        self.password = password
        self.smtp_server = smtp_server
        self.port = port
        self.max_retries = 2
        self.retry_delay = 2

    async def _send_with_retry(self, msg: MIMEMultipart, recipients: list) -> bool:
        for attempt in range(self.max_retries):
            try:
                await aiosmtplib.send(
                    msg,
                    sender=self.email_sender,
                    recipients=recipients,
                    hostname=self.smtp_server,
                    port=self.port,
                    username=self.email_sender,
                    password=self.password,
                    use_tls=True,
                    timeout=30
                )
                return True
            except Exception as e:
                if attempt < self.max_retries - 1:
                    logging.warning(f"EMAIL: Attempt {attempt + 1} failed. Retrying in {self.retry_delay} seconds... Error: {e}")
                    await asyncio.sleep(self.retry_delay)
                else:
                    logging.error(f"EMAIL: All {self.max_retries} attempts failed. Error: {e}")
                    return False

    async def send_email(
            self,
            html_table: str,
            email_list: list,
            email_subj: str,
            cc_list: list = None,
            bcc_list: list = None
    ):
        cc_list = cc_list or []
        bcc_list = bcc_list or []

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = ', '.join(email_list)
            msg['Subject'] = email_subj
            
            if cc_list:
                msg['Cc'] = ', '.join(cc_list)
            
            msg.attach(MIMEText(html_table, 'html'))
            recipients = email_list + cc_list + bcc_list

            success = await self._send_with_retry(msg, recipients)
            if success:
                logging.info(f"EMAIL: Email sent successfully to {recipients}")
            else:
                logging.error(f"EMAIL: Failed to send email after {self.max_retries} attempts")

        except Exception as e:
            logging.error(f"EMAIL: Failed to prepare email. Error: {e}")
            