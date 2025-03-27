from email_akv.email_sender import EmailSender
from asyncio import run

async def main():
    email_sender = EmailSender()
    await email_sender.send_email("test",
                            email_list=["77pto@mail.ru"],
                            email_subj="Тема тест",
                            # cc_list = ["gricyuk@group-akvilon.ru"],
                            bcc_list=["gricyuk@group-akvilon.ru"]
                            )

if __name__ == "__main__":
    run(main())
