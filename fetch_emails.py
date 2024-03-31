import base64
from datetime import datetime
import email
import json
import authenticator
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import os
from db.config import db_session
from db.database import setup_db
from db.models import EmailMessage
from email.header import decode_header

def list_messages(service, user_id="me"):
  try:
    results = service.users().messages().list(userId=user_id).execute()
    messages = results.get("messages", [])
    return messages
  except Exception as e:
    print('An error occurred:', e)
    return []
    
def get_message(service, message_id, user_id='me'):
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='raw').execute()
        return message
    except Exception as e:
        print('An error occurred:', e)
        return None

def decode_message(message):
    try:
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)
        return mime_msg
    except Exception as e:
        print('An error occurred:', e)
        return None


def decode_email_subject(subject):
    decoded_parts = decode_header(subject)
    decoded_subject = ''.join(
        part[0].decode(part[1] or 'ascii') if isinstance(part[0], bytes) else part[0]
        for part in decoded_parts
    )
    return decoded_subject



def save_messages(messages):
  count= 0
  for message in messages:
    count=count+1
    message_id = message['id']
    msg_json = get_message(service, message_id)
    # print(msg_json)
    decoded_msg = decode_message(msg_json)
    # print(decoded_msg.keys())
    # for key in decoded_msg.keys():
    #     if key in decoded_msg:
    #         print(f"{key}: {decoded_msg[key]}")
    #     else:
    #         print(f"{key}: <Not Found>")

    # print(dir(decoded_msg))
    # print(decoded_msg.get_payload()[0])
    
    if decoded_msg:
      # print('From:', decoded_msg['From'])
      # print('Subject:', decoded_msg['Subject'])
      # print('Body:', decoded_msg.get_payload())
      # print('-----------------------')
      
      #       # TODO: Add payload, threadid
      # thread_id=msg_json['threadId'],

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
      
      if count > 5:
        break
      # new_message = EmailMessage(
      #     message_id='example_message_id',
      #     timestamp=datetime.now(),
      #     subject='Example Subject',
      #     sender='example_sender@example.com',
      #     recipients=['example_recipient1@example.com', 'example_recipient2@example.com'],
      #     label_ids=['label1', 'label2'],
      #     email_type='sent',
      #     raw_data={'key': 'value'},
      #     status='unprocessed'
      # )
      # db_session.add(new_message)
      # db_session.commit() 
    
    
      # ===
      # user = db_session.query(EmailMessage).first()
      # print(user.message_id, user.timestamp, user.subject, user.sender, user.recipients, user.label_ids, user.email_type, user.status, user.raw_data)
      # break
  
if __name__ == '__main__':
  setup_db()
  # Authenticate and get Gmail service
  service = authenticator.authenticate_and_get_service()
  messages = list_messages(service)
  save_messages(messages)
  
  # user = db_session.query(EmailMessage).offset(2).first()
  # print(user.message_id, user.timestamp, user.subject, user.sender, user.recipients, user.label_ids, user.email_type, user.status, user.raw_data)