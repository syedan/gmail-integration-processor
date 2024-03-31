import email
from email.header import decode_header
import base64


def modify_message(service, message_id, addLabelIds=[], removeLabelIds=[], user_id="me"):
  try:
    post_body = {
        "addLabelIds": addLabelIds,
        "removeLabelIds": removeLabelIds
    }
    results = service.users().messages().modify(userId=user_id, id=message_id, body=post_body).execute()
    messages = results.get("messages", [])
    return messages
  except Exception as e:
    print('An error occurred:', e)
    return []

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

