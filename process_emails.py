from db.config import db_session
from db.models import EmailMessage

def run_validations():
  email_message_count = db_session.query(EmailMessage).count()
  unprocessed_count = db_session.query(EmailMessage).filter_by(status='unprocessed').count()
  if email_message_count == 0:
      raise ValueError("No rows found in the EmailMessage table.")
  if unprocessed_count == 0:
      raise ValueError("No rows with status 'unprocessed' found in the EmailMessage table.")

  
def process_rows():
  unprocessed_rows = db_session.query(EmailMessage).filter_by(status='unprocessed').all()
  for row in unprocessed_rows: 
    

  
if __name__ == '__main__':
  run_validations()
  process_rows()
  # user = db_session.query(EmailMessage).offset(2).first()
  # print(user.message_id, user.timestamp, user.subject, user.sender, user.to_emails, user.label_ids, user.email_type, user.status)