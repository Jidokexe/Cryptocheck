import psycopg2
import smtplib
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
