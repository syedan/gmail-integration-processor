import base64
import email
import json
import authenticator
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import os
from database import setup_db


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

def save_messages(messages):
  for message in messages:
    message_id = message['id']
    msg = get_message(service, message_id)
    # print(msg)
    decoded_msg = decode_message(msg)
    # print(decoded_msg.keys())
    # print(decoded_msg.get_payload()[1])
    if decoded_msg:
        print('From:', decoded_msg['From'])
        print('Subject:', decoded_msg['Subject'])
        print('Body:', decoded_msg.get_payload())
        print('-----------------------')
    break
  
if __name__ == '__main__':
  setup_db()
  # Authenticate and get Gmail service
  service = authenticator.authenticate_and_get_service()
  messages = list_messages(service)
  save_messages(messages)