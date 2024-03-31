
## **Standalone Python script that integrates with Gmail API and performs some rule based operations on emails**

#### IMPORTANT!! - This script integrates with your Gmail and requires read/write permissions. Since this is a test project, it is highly recommeded that you use personal account instead of work emails to test.

### Third party libs being used
1. official python packages for connecting with gmail: https://developers.google.com/gmail/api/quickstart/python#install_the_google_client_library
2. A rule based engine to run rules against factsets and take custom actions: https://github.com/santalvarez/python-rule-engine

## Prerequisites
1. Docker desktop installed your laptop.  This is being used to run a postgres DB instance on your local. You can also use other methods of running the database, eg: brew services. 
2. Create a new project on your personal google workspace account. Enable Gmail API from `Enabled APIs & Services` view.  Follow guide: https://developers.google.com/gmail/api/quickstart/python, to gather `credentials.json` and paste it inside `gmail` folder.  


## Usage: 
1. Clone the repo
2. Setup and activate virtual env.  Note: you can use `deactivate` command to exit the venv

```
  python3 -m venv myenv
  source myenv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

5. Make sure postgres database is running. If using default docker setup, run below commands:

```
docker build -t my-postgres-image .
docker run --name my-postgres-container -p 5432:5432 my-postgres-image:latest
```
   
7. There are two script:   One fetches emails from API and store them in email_messages table. Once emails are stored in DB, another script picks up unprocessed emails and applies rules defined in `rules.json` file and takes actions defined via the Gmail API

```
 # Fetch all recent emails 
 python3 fetch_emails.py

# Process emails stored in DB
python3 process_emails.py
``` 

