
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://myuser:mypassword@localhost/mydatabase'
engine = create_engine(DATABASE_URL)
# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)

# Create a session
db_session = Session()