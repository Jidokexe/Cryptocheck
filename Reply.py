import imaplib
import email

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
