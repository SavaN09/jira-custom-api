from jira import JIRA
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods =['POST'])
def submit_page():
    result = submit_to_jira(request.form.get('pid'),request.form.get('ttitle'),request.form.get('tdesc'),request.form.get('atoken'))
    if result == "existing_issue":
        condition = "The same title exist, please change the title and create an issue again"
    else:
        condition = "Issue has been created and stored to DB successfully"

    return render_template('index.html', condition = condition)

def submit_to_jira(pid, title, description, token):
    print("connecitng jira")
    jira_instance = JIRA(basic_auth=('savankumarbhupendrabhai@gmail.com',token),options={"server":"https://savankumarbhupendrabhai.atlassian.net/"})

    print("checking if title already exist or not")
    list_of_titles = []
   
    all_issues = jira_instance.search_issues('project='+pid, fields='summary')
   
    for single_issue in all_issues:
        list_of_titles.append(single_issue.raw['fields']['summary'])
    
    if title in list_of_titles:
        print(title)
        print("issue already exist, will not create a jira and wont push data to mongo")
        return "existing_issue"
    else:
        print("creating issue")
        jira_instance.create_issue(project=pid, summary=title, description=description, issuetype={'name':'Bug'})
        print("done creating usse")
        print("submitting to mongo as this issue title does not already exist")
        submit_to_mongo(pid, title, description)
        return "new_issue"
    

def submit_to_mongo(pid, title, description):
    print("Trying to connect to Mongo Atlas DB")
    conn = MongoClient("mongodb://admin:admin@cluster0-shard-00-00.al352.mongodb.net:27017,cluster0-shard-00-01.al352.mongodb.net:27017,cluster0-shard-00-02.al352.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-1r67m5-shard-0&authSource=admin&retryWrites=true&w=majority")
    
    print("connection established successfully")
    
    db = conn["jira"]
    collection = db["tickets"]
    object_to_store = {}

    object_to_store['ProjectID'] = pid
    object_to_store['TicketTitle'] = title
    object_to_store['TicketDescription'] = description

    collection.insert_one(object_to_store)
    print("data stored to db successfully")

