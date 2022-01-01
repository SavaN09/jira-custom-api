from jira import JIRA
from flask import Flask, render_template, request
from pymongo import MongoClient, collection

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods =['POST'])
def submit_page():
    submit_to_jira(request.form.get('pid'),request.form.get('ttitle'),request.form.get('tdesc'))
    submit_to_mongo(request.form.get('pid'),request.form.get('ttitle'),request.form.get('tdesc'))
    return render_template('index.html')

def submit_to_jira(pid, title, description):
    jira_instance = JIRA(basic_auth=('savankumarbhupendrabhai@gmail.com','kqmXvm3huHKQWU9eKUsY1212'),options={"server":"https://savankumarbhupendrabhai.atlassian.net/"})
    jira_instance.create_issue(project=pid, summary=title, description=description, issuetype={'name':'Bug'})

def submit_to_mongo(pid, title, description):
    print("into mongo")
    conn = MongoClient("mongodb+srv://admin:admin@savanpatel.al352.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = conn["jira"]
    collection = db["tickets"]
    object_to_store = {}

    object_to_store['ProjectID'] = pid
    object_to_store['TicketTitle'] = title
    object_to_store['TicketDescription'] = description

    collection.insert_one(object_to_store)