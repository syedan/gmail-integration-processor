from datetime import datetime
from gmail.authenticator import authenticate_and_get_service
from db.config import db_session
from db.database import setup_db
from db.models import EmailMessage
from gmail.api import list_messages, get_message, decode_message, decode_email_subject


def save_messages(messages):
  print("Saving {} messages to DB".format(len(messages)))
  for message in messages:
    message_id = message['id']
    msg_json = get_message(service, message_id)
    decoded_msg = decode_message(msg_json)
    label_ids = msg_json.get('labelIds', [])
    email_type = "sent" if "SENT" in label_ids else "received"
    new_message = EmailMessage(
        message_id=msg_json['id'],
        timestamp=datetime.now(),
        subject=decode_email_subject(decoded_msg['Subject']),
        sender=decoded_msg['From'],
        to_emails=decoded_msg['To'],
        label_ids=label_ids,
        email_type=email_type,
        raw_data=msg_json,
        status='unprocessed'
    )
    db_session.add(new_message)
    db_session.commit() 
  print("Messages saved to DB and ready for processing")
  
if __name__ == '__main__':  
  setup_db()
  service = authenticate_and_get_service()
  print("Fetching recent emails for the user...")
  messages = list_messages(service)
  save_messages(messages)
  