import psycopg


def setup_db():
  conn = _setup_connection()
  _setup_tables(conn)
  
  
# Private methods
def _setup_connection():
  conn = psycopg.connect(dbname = "mydatabase", 
                      user = "myuser", 
                      host= 'localhost',
                      password = "mypassword",
                      port = 5432)
  return conn

def _setup_tables(conn):
  cur = conn.cursor()
  cur.execute("""CREATE TABLE datacamp_courses(
              course_id SERIAL PRIMARY KEY,
              course_name VARCHAR (50) UNIQUE NOT NULL,
              course_instructor VARCHAR (100) NOT NULL,
              topic VARCHAR (20) NOT NULL);
              """)
  conn.commit()
  cur.close()
  conn.close()

  
