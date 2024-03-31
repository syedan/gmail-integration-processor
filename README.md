# happyfox-interview

python3 -m venv myenv
source myenv/bin/activate
pip3 freeze > requirements.txt

# Follow guide: https://developers.google.com/gmail/api/quickstart/python

#

<!-- pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib -->

pip install -r requirements.txt

deactivate

====

docker build -t my-postgres-image .

docker run --name my-postgres-container1 -p 5432:5432 my-postgres-image:latest
