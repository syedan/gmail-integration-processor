from python_rule_engine import RuleEngine
from db.config import db_session
from db.models import EmailMessage
import json
from gmail.api import modify_message
from gmail.authenticator import authenticate_and_get_service


#======== Rules getter and validations =====
def run_validations():
  email_message_count = db_session.query(EmailMessage).count()
  unprocessed_count = db_session.query(EmailMessage).filter_by(status='unprocessed').count()
  if email_message_count == 0:
      raise ValueError("No rows found in the EmailMessage table.")
  if unprocessed_count == 0:
      raise ValueError("No rows with status 'unprocessed' found in the EmailMessage table.")

def all_rule_objs():
  # TODO:  Add validation on input json data
  with open('rules.json', 'r') as file:
      data_dict = json.load(file)
  return data_dict
  
  
#======== Process methods =====
def process_row(row, service):
   # Run all rules
  for rule_obj in all_rule_objs():
    for rule in rule_obj['rules']:
      factset = {
        'subject': row.subject,
        'sender': row.sender,
        'to_emails': row.to_emails
      }
      engine = RuleEngine([rule])
      matched_objs = engine.evaluate(factset)
      if len(matched_objs) > 0:
        process_actions(row, rule_obj['actions'], service)

  
def process_rows(service):
  unprocessed_rows = db_session.query(EmailMessage).filter_by(status='unprocessed').all()
  for row in unprocessed_rows: 
    process_row(row, service)


#========  methods using gmail API interfaces =====
def process_actions(row, actions, service): 
  print(actions)
  for action in actions:
      action_id = action.get('id')
      action_val = action.get('val')
      if action_id == 'mark_read':
        mark_email_as_read(row, service)
      elif action_id == 'mark_unread':
        mark_email_as_unread(row, service)
      elif action_id == 'move_message':
        email_move_message(row, action_val, service)

def email_move_message(row, moveToLabel, service):
    standard_labels = ["SPAM", "CATEGORY_SOCIAL", "CATEGORY_FORUMS",
                       "CATEGORY_UPDATES", "CATEGORY_PERSONAL","CATEGORY_PROMOTIONS"]
    addLabelIds = [moveToLabel]
    removeLabelIds = [label for label in standard_labels if label not in addLabelIds]
    modify_message(service, row.message_id, addLabelIds=addLabelIds, removeLabelIds=removeLabelIds)

def mark_email_as_read(row, service):
    removeLabelIds = ["UNREAD"]
    modify_message(service, row.message_id, removeLabelIds=removeLabelIds)

def mark_email_as_unread(row, service):
    addLabelIds = ["UNREAD"]
    modify_message(service, row.message_id, addLabelIds=addLabelIds)


if __name__ == '__main__':
  service = authenticate_and_get_service()
  run_validations()
  process_rows(service)