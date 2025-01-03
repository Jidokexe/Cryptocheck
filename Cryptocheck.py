import psycopg2
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def connect_db():
        return psycopg2.connect("dbname=yourdb user=youruser password=yourpassword")

def verify_signature(document_data, signature, public_key):
        public_key = serialization.load_pem_public_key(public_key)
        try:
            public_key.verify(
                signature,
                document_data,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            return False

def check_document_signature(document_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT document_data, signature, public_key FROM documents JOIN employees ON documents.employee_id = employees.id WHERE documents.id = %s", (document_id,))
        record = cursor.fetchone()

        if record:
            document_data, signature, public_key = record
            is_valid = verify_signature(document_data, signature, public_key.encode())
            cursor.close()
            return is_valid
        cursor.close()
        return False

def send_email(to_email, subject, body, attachment=None):
    from_email = "your_email@example.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        part = MIMEApplication(attachment, Name='document.pdf')
        part['Content-Disposition'] = 'attachment; filename="document.pdf"'
        msg.attach(part)

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)


def check_incoming_emails():
    mail = imaplib.IMAP4_SSL('imap.example.com')
    mail.login('your_email@example.com', 'your_password')
    mail.select('inbox')

    result, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
 
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        from_email = msg['From']
        subject = msg['Subject']

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'application/pdf':  
                    document_data = part.get_payload(decode=True)
                    # проверяем подпись
                    is_valid = check_document_signature(document_data)  

                    reply_subject = 'Результат проверки: {}'.format(subject)
                    reply_body = 'Документ {} имеет действительную ЭЦП: {}'.format(subject, is_valid)
                    send_email(from_email, reply_subject, reply_body)
        else:
            continue

    mail.logout()
