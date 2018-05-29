import imaplib
import email
import base64
import socket

class EmailExtractor():

    @staticmethod
    def extract_email_lines_and_sender(address, password, index, folder='inbox'):
    
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(address, password)
            mail.list()
        except (imaplib.IMAP4.error, UnicodeEncodeError):
            raise EmailException("Не удалось подключиться к почтовому ящику.\
                \nПроверьте адрес и пароль.")
        except socket.gaierror:
            raise EmailException("Не удалось подключиться к почтовому ящику.\
                \nПроверьте интернет-соединение.")

        mail.select(folder)

        _, data = mail.uid('search', None, 'ALL')
        email_ids = data[0].split()
        if len(email_ids) < index:
            raise EmailWarning('Некорректный номер письма.\nВсего входящих писем: ' + str(len(email_ids)))
        
        latest_email_uid = email_ids[-index]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]

        lines = []
        msg = email.message_from_bytes(raw_email)
        for part in msg.walk():
            if part.get_content_type() == 'text/plain' and part['Content-Transfer-Encoding'] == 'base64':
                s = part.get_payload() 
                new_s = base64.b64decode(s).decode("UTF-8")
                lines_of_part = new_s.split("\n")
                lines += lines_of_part
        
        if not len(lines):
            raise EmailWarning('Не удалось получить текст письма.')

        sender_list = email.header.decode_header(msg['From'])
        sender = ""
        for item in sender_list:
            if isinstance(item[0], str):
                sender += bytearray(item[0], "utf-8").decode("UTF-8")
            else:
                sender += item[0].decode("UTF-8")
        
        print(sender)
        return lines, sender

class EmailException(BaseException):
    pass

class EmailWarning(BaseException):
    pass
            

        