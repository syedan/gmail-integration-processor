from db.models import create_tables


def setup_db():
  print("Setting DB and tables...")
  create_tables()
  