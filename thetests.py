import csv
import datetime
from datetime import timedelta
import json
import time
from selenium.webdriver.chrome.options import Options
import clipboard
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from jsonschema import validate, Draft3Validator
import pypyodbc
import pandas as pd
import re
import sqlalchemy
import ssl
#baseurl = 'https://qaeurc05.teleopticloud.com/api'
#apitoken ='YjY3ZjcyZDUzOGVjNGNmYmFiNDVmNzY2YTk0ZTBhNWY5NTYzYjcwMTU3ZmY0OWMyYmNjZmJkYzQ3MDFjYjQ5NQ=='
baseurl = "https://devtest-k8s.teleopticloud.com//api"
apitoken = "NTc1YWM4ZjIzMmFmNDgyYmE1ZjViNDAyZmE2OTNiNzU0YjVkZDI1NjZkNGE0M2JmYjc4ODRlZGFjODAwMGFhMQ=="


#databaseconnection

cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                             "Server=testcluster.database.windows.net;"
                             "Database=testcluster_devtest_app;"
                             "uid=TestCluster;pwd=X4vmfdZ9")

#date functions to make requests work over time
def getdate30daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=30)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate31daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=31)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate32daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=32)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate34daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=34)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate36daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=36)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate45daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=45)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate60daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=60)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def gettodaysdatewith_zeroformats():
    now = datetime.datetime.now()
    result = now.strftime("%Y-%m-%d")
    return result
def getdate7daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=7)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result
def getdate3daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=3)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result

#environment variables
# fullDayAbsenceRequestID obtained inside test_AddFullDayAbsenceRequest
# overTimeRequestId obtained inside test_AddOvertimeRequest
fullDayAbsenceRequestID = '8e793f5a-b4c8-40c1-9156-ac3d00bb51a9'
overTimeRequestId = '30fadb41-90b5-48dd-832f-ac3e00c0e8a7'

#Seleniumtest to get API-token, not neccesary currently.
'''
@pytest.mark.command
@pytest.mark.queries
@pytest.mark.runfirst
@pytest.mark.flaky(reruns=5)
def test_seleniumtogetAPItoken():


    #chrome_options = Options()

    #chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()
    driver.get("https://devtest-k8s.teleopticloud.com/")
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.find_element(By.ID, "webteamschedule").click()

    driver.implicitly_wait(70)
    driver.find_element(By.ID, "Username-input").send_keys("tdemo")
    driver.find_element(By.ID, "Password-input").send_keys("tdemo")
    driver.find_element(By.ID, "Signin-button").click()
    driver.implicitly_wait(70)

    driver.find_element(By.LINK_TEXT, "tdemo tdemo").click()
    driver.implicitly_wait(10)

    driver.find_element(By.CSS_SELECTOR, ".ant-tabs-tab:nth-child(2)").click()
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, ".ant-input").click()
    driver.find_element(By.CSS_SELECTOR, ".ant-input").send_keys("johnapiautomation")
    driver.implicitly_wait(20)
    driver.find_element(By.CSS_SELECTOR, ".ng-tns-c141-23 > .ng-star-inserted").click()
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "(//input[@type='text'])[6]").click()

    apitoken2 = clipboard.paste()

    driver.close()
    global apitoken
    apitoken = apitoken2

'''

def test_DatabaseConnection():
    cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                            "Server=testcluster.database.windows.net;"
                            "Database=testcluster_devtest_app;"
                            "uid=TestCluster;pwd=X4vmfdZ9")
    df = pd.read_sql_query("Select * from [dbo].[Person] where FirstName = 'JohnTest'", cnxn)
    print(df)

#these test are commands
with open('csvtestdata/test_AddAgent.csv') as f:
 reader = csv.reader(f)
 addAgentData= list(reader)
@pytest.mark.command
@pytest.mark.parametrize("TimeZoneId, Contract, ContractSchedule, BudgetGroup, PartTimePercentage ", addAgentData)
def test_AddAgent(TimeZoneId, Contract, ContractSchedule, BudgetGroup, PartTimePercentage):

     requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "FirstName": "JohnTest",
  "LastName": "TestJohn",
  "Email": "",
  "EmploymentNumber": "",
  "StartDate": gettodaysdatewith_zeroformats(),
  "ApplicationLogon": "",
  #"Identity": "Agent",
  "Site": "London",
  "Team": "Students",
  "Contract": Contract,
  "ContractSchedule": ContractSchedule,
  "PartTimePercentage": PartTimePercentage,
  #"Culture": "string",
  "Roles": [
    'Agent'
  ],
  "WorkflowControlSet": "Default WCS",
  "ShiftBag": '',
  "BudgetGroup": BudgetGroup,
  "FirstDayOfWeek": 0
}
     payload = json.dumps(requestdata)
     headers = {
         'Authorization': apitoken,
         'Content-Type': 'application/json'
     }
     try:
        response = requests.request("POST", baseurl + "/command/AddAgent", headers=headers, data=payload)
     except requests.exceptions.ConnectionError:
         print("Internet connection down")
     else:
         print(response.text.encode('utf8'))

     if (response.status_code != 200):
         file = open("Failedresponses/Addagent" + gettodaysdatewith_zeroformats() + ".txt", "w")
         file.write(str(response.text.encode('utf8')))
         file.close()

     assert response.status_code == 200

     #regex to seperate id from wierd string returned by DB
     dbid = str(pd.read_sql_query("SELECT TOP 1 Id FROM [dbo].[Person] ORDER BY ID DESC", cnxn))
     idtemp= re.sub("id","", dbid)
     idtemp2= re.sub("0  b", "",idtemp)
     idtemp3= re.sub("\n", "", idtemp2)
     id = re.sub("                                        ", "", idtemp3)

     #select everything from another db table using the id from the persontable.
     persontest = str(pd.read_sql_query("SELECT * FROM [dbo].[PersonAbsence] where Person =" + id, cnxn))
     print(persontest)

     #select everything the easy way but doesn't work for other db tables
     test = str(pd.read_sql_query("SELECT TOP 1 * FROM [dbo].[Person] ORDER BY ID DESC", cnxn))
     print(test)


     dblastname = str(pd.read_sql_query("SELECT TOP 1 LastName FROM [dbo].[Person] ORDER BY ID DESC", cnxn))
     dbfirstname = str(pd.read_sql_query("SELECT TOP 1 FirstName FROM [dbo].[Person] ORDER BY ID DESC", cnxn))

     lastname = re.findall("TestJohn", dblastname)
     firstname = re.findall("JohnTest", dbfirstname)


     assert lastname == ['TestJohn']
     assert firstname == ['JohnTest']

with open('csvtestdata/test_AddFullDayAbsence.csv') as f:
 reader = csv.reader(f)
 dataaddfulldayabsence= list(reader)
@pytest.mark.command
@pytest.mark.parametrize("AbsenceId, PersonId", dataaddfulldayabsence)
def test_AddFullDayAbsence(AbsenceId,PersonId):

     requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": PersonId,
  "Date": getdate30daysahead_zeroformats(),
  "AbsenceId": AbsenceId,
  "ScenarioId": ""
}
     payload = json.dumps(requestdata)
     headers = {
         'Authorization': apitoken,
         'Content-Type': 'application/json'
     }
     try:
        response = requests.request("POST", baseurl + "/command/AddFullDayAbsence", headers=headers, data=payload)
     except requests.exceptions.ConnectionError:
         print("Internet connection down")
     else:
         print(response.text.encode('utf8'))

     if (response.status_code != 200):
         file = open("Failedresponses/AddFullDayAbsence" + gettodaysdatewith_zeroformats() + ".txt", "w")
         file.write(str(response.text.encode('utf8')))
         file.close()

     assert response.status_code == 200
with open('csvtestdata/test_AddFullDayAbsenceRequest.csv') as f:
    reader = csv.reader(f)
    dataaddfulldayabsencerequest = list(reader)
@pytest.mark.command
@pytest.mark.queries #marked querie because a querie requires the ID obtained in this test
@pytest.mark.parametrize("AbsenceId, Subject", dataaddfulldayabsencerequest)
def test_AddFullDayAbsenceRequest(AbsenceId,Subject):
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "AbsenceId": AbsenceId,
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate30daysahead_zeroformats()
  },
  "Subject": Subject,
  "Message": "johntest"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/AddFullDayAbsenceRequest", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    resp = json.loads(response.text.encode('utf8'))
    global fullDayAbsenceRequestID

    fullDayAbsenceRequestID = resp.get("Id")

    if (response.status_code != 200):
        file = open("Failedresponses/AddFullDayAbsenceRequest"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    schema = {
    "type": "object",
    "properties": {
    "StatusCode": {"type": "number"},
    "Id": {"type": "string"},
    "Message": {"type": "null"},
    },
    }
    e = Draft3Validator(schema)
    errors = sorted(e.iter_errors(resp), key=lambda e: e.path)
    print(errors)
    validate(resp, schema)

with open('csvtestdata/test_AddIntradayAbsenceRequest.csv') as f:
    reader = csv.reader(f)
    intraRequestData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("Subject,Message,TimeZoneID,AbsenceID", intraRequestData)
def test_AddIntradayAbsenceRequest(Subject,Message,TimeZoneID,AbsenceID):
    requestdata = {
  "TimeZoneId": TimeZoneID,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "AbsenceId": AbsenceID,
  "Period": {
    "StartTime": gettodaysdatewith_zeroformats() + "T16:57:00.000Z",
    "EndTime": gettodaysdatewith_zeroformats() + "T17:57:00.000Z"
  },
  "Subject": Subject,
  "Message": Message
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", baseurl + "/command/AddIntradayAbsenceRequest", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AddIntradayAbsenceRequest" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    schema = {
        "type": "object",
        "properties": {
            "StatusCode": {"type": "number"},
            "Id": {"type": "string"},
            "Message": {"type": "null"},
        },
    }
    e = Draft3Validator(schema)
    errors = sorted(e.iter_errors(resp), key=lambda e: e.path)
    print(errors)
    validate(resp, schema)

with open('csvtestdata/addorremovemeeting.csv') as f:
 reader = csv.reader(f)
 dataforaddmeeting = list(reader)

#using firstrow of that list to remove all created meetings

 dataforremovemeeting = []
 for x in dataforaddmeeting:
    dataforremovemeeting.append(x[0])
@pytest.mark.command
@pytest.mark.parametrize("ExternalMeetingId, Title, StartMeetingHour, EndMeetingHour, ActivityId, TimeZoneId", dataforaddmeeting)
def test_AddMeeting(ExternalMeetingId, Title, StartMeetingHour, EndMeetingHour, ActivityId, TimeZoneId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "ScenarioId": "E21D813C-238C-4C3F-9B49-9B5E015AB432",
  "ExternalMeetingId":ExternalMeetingId,
  "Participants": [
    "B0E35119-4661-4A1B-8772-9B5E015B2564"
  ],
  "ActivityId": ActivityId,
  "Period": {
    "StartTime": getdate30daysahead_zeroformats()+ "T"+StartMeetingHour+":00:00.000",
    "EndTime": getdate30daysahead_zeroformats()+"T"+EndMeetingHour+":00:00.000"
  },
  "Title": Title,
  "Location": "Stockholm",
  "Agenda": "meetingjohntest"
}
    payload = json.dumps(requestdata)

    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/AddMeeting", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AddMeeting"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200
@pytest.mark.command
@pytest.mark.parametrize("ExternalMeetingId", dataforremovemeeting)
def test_RemoveMeeting(ExternalMeetingId):
    requestdata = {
  "ExternalMeetingId": ExternalMeetingId
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/RemoveMeeting", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/RemoveMeeting"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

with open('csvtestdata/test_AddOvertimeRequest.csv') as f:
    reader = csv.reader(f)
    overTimeRequestData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("TimeZoneId, OverTimeType, Subject", overTimeRequestData)
def test_AddOvertimeRequest(TimeZoneId,OverTimeType,Subject):


   requestdata = {
    "TimeZoneId": TimeZoneId,
    "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
    "PersonId": "E34730FD-9B4D-4572-961A-9B5E015B2564",
    "Period": {
        "StartTime":  gettodaysdatewith_zeroformats() + "T13:56:00.000Z",
        "EndTime":  gettodaysdatewith_zeroformats() + "T17:56:00.000Z"
    },
    "Subject": Subject,
    "Message": "johnsabsence",
    "OvertimeType": OverTimeType
}
   payload = json.dumps(requestdata)
   headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

   try:
       response = requests.request("POST", baseurl + "/command/AddOvertimeRequest", headers=headers, data=payload)

   except requests.exceptions.ConnectionError:
       print("Internet connection down")
   else:
       print(response.text.encode('utf8'))


   resp = json.loads(response.text.encode('utf8'))
   global overTimeRequestId
   overTimeRequestId = resp.get("Id")

   if (response.status_code != 200):
       file = open("Failedresponses/AddOvertimeRequest" + gettodaysdatewith_zeroformats() + ".txt", "w")
       file.write(str(response.text.encode('utf8')))
       file.close()

   assert response.status_code == 200

   schema = {
       "type": "object",
       "properties": {
           "StatusCode": {"type": "number"},
           "Id": {"type": "string"},
           "Message": {"type": "null"},
       },
   }
   e = Draft3Validator(schema)
   errors = sorted(e.iter_errors(resp), key=lambda e: e.path)
   print(errors)
   validate(resp, schema)

with open('csvtestdata/test_AddPartDayAbsence.csv') as f:
    reader = csv.reader(f)
    addPartDayAbsenceData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("AbsenceId, TimeZoneId", addPartDayAbsenceData)
def test_AddPartDayAbsence(AbsenceId, TimeZoneId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartTime": getdate30daysahead_zeroformats()+"T10:06:00.000Z",
    "EndTime": getdate30daysahead_zeroformats()+"T16:06:00.000Z"
  },
  "AbsenceId": AbsenceId,
  "ScenarioId": ""
}
    payload = json.dumps(requestdata)

    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", baseurl + "/command/AddPartDayAbsence", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AddpartdayAbsence"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

@pytest.mark.command
def test_AddScheduleChangesListener():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "Url": "http://localhost/TeleoptiWFM",
  "Name": "jonhtest",
  "DaysStartFromCurrentDate": 1,
  "DaysEndFromCurrentDate": 4
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/AddScheduleChangesListener", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AddScheduleChangesListener"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

@pytest.mark.command
def test_AddTeam():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "TeamName": "Johnsteam",
  "SiteId": "D970A45A-90FF-4111-BFE1-9B5E015AB45C"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/AddTeam", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AddTeam"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    schema = {
        "type": "object",
        "properties": {
            "StatusCode": {"type": "number"},
            "Id": {"type": "string"},
            "Message": {"type": "null"},
        },
    }
    e = Draft3Validator(schema)
    errors = sorted(e.iter_errors(resp), key=lambda e: e.path)
    print(errors)
    validate(resp, schema)

with open('csvtestdata/test_RemovePersonAbsence.csv') as f:
    reader = csv.reader(f)
    RemovePersonAbsenceData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("TimeZoneId, PersonId",  RemovePersonAbsenceData)
def test_RemovePersonAbsence(TimeZoneId, PersonId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": PersonId,
  "Period": {
    "StartTime": gettodaysdatewith_zeroformats()+"T08:10:00.000Z",
    "EndTime": getdate30daysahead_zeroformats()+"T08:10:00.000Z"
  },
  "ScenarioId": "E21D813C-238C-4C3F-9B49-9B5E015AB432"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/RemovePersonAbsence", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/RemovepersonAbsence"+gettodaysdatewith_zeroformats()+".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200


@pytest.mark.xfail(reason="Currently under toggle")
@pytest.mark.command
def test_RemoveFullDayAbsence():
    requestdata = {
            "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
            "PersonId": "9D42C9BF-F766-473F-970C-9B5E015B2564",
            "Period": {
                "StartDate": gettodaysdatewith_zeroformats(),
                "EndDate": getdate7daysahead_zeroformats()
            },
            "ScenarioId": ""
        }


    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", baseurl + "/command/RemoveFullDayAbsence", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/RemoveFullDayAbsence" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

@pytest.mark.xfail(reason="Currently under toggle")
@pytest.mark.command
def test_RemovePartDayAbsence():
    requestdata = {
            "TimeZoneId": 'Europe/London',
            "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
            "PersonId": '9D42C9BF-F766-473F-970C-9B5E015B2564',
            "Period": {
                "StartTime": gettodaysdatewith_zeroformats()+"T10:51:00.000Z",
                "EndTime": getdate7daysahead_zeroformats()+"T10:51:00.000Z"
            },
            "ScenarioId": ""
        }

    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", baseurl + "/command/RemovePartDayAbsence", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/RemovePartDayAbsence" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200


with open('csvtestdata/test_SetSchedulesForPerson.csv') as f:
    reader = csv.reader(f)
    SetSchedulesForPersonData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("ScenarioId, TimeZoneId, ActivityId", SetSchedulesForPersonData)
def test_SetSchedulesForPerson(ScenarioId,TimeZoneId,ActivityId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "DatePeriod": {
    "StartDate": getdate30daysahead_zeroformats(),
    "EndDate": getdate60daysahead_zeroformats()
  },
  "ScheduleDays": [
    {
      "Date": getdate31daysahead_zeroformats(),
      "ShiftCategoryId": "EC7F6475-1AE7-4A94-83C1-9B5E015AB4C3",
      #"DayOffTemplateId": "F2F35A09-9453-4944-A3F7-550DC06EA0FF",
      #"FullDayAbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330",
      "Layers": [
        {
          "Period": {
            "StartTime": getdate31daysahead_zeroformats()+"T08:18:00.000",
            "EndTime": getdate31daysahead_zeroformats()+"T16:18:00.000"
          },
          "ActivityId": ActivityId,
          #"AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
        }
      ]
    }
  ],
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "ScenarioId": ScenarioId
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/SetSchedulesForPerson", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/SetSchedulesForPerson" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

@pytest.mark.command
@pytest.mark.parametrize("ScenarioId, TimeZoneId, ActivityId", SetSchedulesForPersonData)
def test_SetSchedulesForPerson_MultipleLayersOfActivitysWithinDateAndMultipleScheduleDays(ScenarioId,TimeZoneId,ActivityId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "DatePeriod": {
    "StartDate": getdate30daysahead_zeroformats(),
    "EndDate": getdate60daysahead_zeroformats()
  },
  "ScheduleDays": [
    {
      "Date": getdate30daysahead_zeroformats(),
      "ShiftCategoryId": "EC7F6475-1AE7-4A94-83C1-9B5E015AB4C3",
      #"DayOffTemplateId": "F2F35A09-9453-4944-A3F7-550DC06EA0FF",
      #"FullDayAbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330",
      "Layers": [
        {
          "Period": {
            "StartTime": getdate30daysahead_zeroformats()+"T08:18:00.000",
            "EndTime": getdate30daysahead_zeroformats()+"T10:18:00.000"
          },
          "ActivityId": ActivityId,
          #"AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
        },
          {
              "Period": {
                  "StartTime": getdate30daysahead_zeroformats() + "T13:18:00.000",
                  "EndTime": getdate30daysahead_zeroformats() + "T14:18:00.000"
              },
              "ActivityId": "BA3624B0-0AEA-4B72-A585-9B5E015AB3C6",
              # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
          },
          {
              "Period": {
                  "StartTime": getdate30daysahead_zeroformats() + "T14:18:00.000",
                  "EndTime": getdate30daysahead_zeroformats() + "T16:18:00.000"
              },
              "ActivityId": "92159C8B-69B9-4F16-AD18-9B5E015AB3C6",
              # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
          }
      ]
    },
      {
          "Date": getdate32daysahead_zeroformats(),
          "ShiftCategoryId": "EC7F6475-1AE7-4A94-83C1-9B5E015AB4C3",
          # "DayOffTemplateId": "F2F35A09-9453-4944-A3F7-550DC06EA0FF",
          # "FullDayAbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330",
          "Layers": [
              {
                  "Period": {
                      "StartTime": getdate32daysahead_zeroformats() + "T08:18:00.000",
                      "EndTime": getdate32daysahead_zeroformats() + "T10:18:00.000"
                  },
                  "ActivityId": "BA3624B0-0AEA-4B72-A585-9B5E015AB3C6",
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              },
              {
                  "Period": {
                      "StartTime": getdate32daysahead_zeroformats() + "T13:18:00.000",
                      "EndTime": getdate32daysahead_zeroformats() + "T14:18:00.000"
                  },
                  "ActivityId": ActivityId,
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              },
              {
                  "Period": {
                      "StartTime": getdate32daysahead_zeroformats() + "T14:18:00.000",
                      "EndTime": getdate32daysahead_zeroformats() + "T16:18:00.000"
                  },
                  "ActivityId": "92159C8B-69B9-4F16-AD18-9B5E015AB3C6",
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              }
          ]
      },
      {
          "Date": getdate34daysahead_zeroformats(),
          "ShiftCategoryId": "EC7F6475-1AE7-4A94-83C1-9B5E015AB4C3",
          # "DayOffTemplateId": "F2F35A09-9453-4944-A3F7-550DC06EA0FF",
          # "FullDayAbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330",
          "Layers": [
              {
                  "Period": {
                      "StartTime": getdate34daysahead_zeroformats() + "T08:18:00.000",
                      "EndTime": getdate34daysahead_zeroformats() + "T10:18:00.000"
                  },
                  "ActivityId": "92159C8B-69B9-4F16-AD18-9B5E015AB3C6",
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              },
              {
                  "Period": {
                      "StartTime": getdate34daysahead_zeroformats() + "T13:18:00.000",
                      "EndTime": getdate34daysahead_zeroformats() + "T14:18:00.000"
                  },
                  "ActivityId": "BA3624B0-0AEA-4B72-A585-9B5E015AB3C6",
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              },
              {
                  "Period": {
                      "StartTime": getdate34daysahead_zeroformats() + "T14:18:00.000",
                      "EndTime": getdate34daysahead_zeroformats() + "T16:18:00.000"
                  },
                  "ActivityId": ActivityId,
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              }
          ]
      },
      {
          "Date": getdate36daysahead_zeroformats(),
          "ShiftCategoryId": "EC7F6475-1AE7-4A94-83C1-9B5E015AB4C3",
          # "DayOffTemplateId": "F2F35A09-9453-4944-A3F7-550DC06EA0FF",
          # "FullDayAbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330",
          "Layers": [
              {
                  "Period": {
                      "StartTime": getdate36daysahead_zeroformats() + "T08:18:00.000",
                      "EndTime": getdate36daysahead_zeroformats() + "T10:18:00.000"
                  },
                  "ActivityId": ActivityId,
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              },
              {
                  "Period": {
                      "StartTime": getdate36daysahead_zeroformats() + "T13:18:00.000",
                      "EndTime": getdate36daysahead_zeroformats() + "T14:18:00.000"
                  },
                  "ActivityId": "BA3624B0-0AEA-4B72-A585-9B5E015AB3C6",
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              },
              {
                  "Period": {
                      "StartTime": getdate36daysahead_zeroformats() + "T14:18:00.000",
                      "EndTime": getdate36daysahead_zeroformats() + "T16:18:00.000"
                  },
                  "ActivityId": "92159C8B-69B9-4F16-AD18-9B5E015AB3C6",
                  # "AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
              }
          ]
      }
  ],
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "ScenarioId": ScenarioId
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/SetSchedulesForPerson", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/SetSchedulesForPerson" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

'''
#The timezonestests are dependant on the users in https://qaeurc02.teleopticloud.com environment
with open('csvtestdata/addorremovemeetingtimezones.csv') as f:
 reader = csv.reader(f)
 dataforaddmeetingtimezones = list(reader)

#using firstrow of that list to remove all created meetings

 dataforremovemeetingtimezones = []
 for x in dataforaddmeetingtimezones:
    dataforremovemeetingtimezones.append(x[0])
@pytest.mark.command
@pytest.mark.parametrize("ExternalMeetingId, StartMeetingHour, EndMeetingHour, ActivityId, TimeZoneId, ScenarioId, Participant1, Participant2, Participant3, Participant4, Participant5, Participant6, Participant7, Participant8, Participant9, Participant10", dataforaddmeetingtimezones)
def test_AddMeeting_AllTimeZonesLoopThrough(ExternalMeetingId, StartMeetingHour, EndMeetingHour, ActivityId, TimeZoneId, ScenarioId, Participant1, Participant2, Participant3, Participant4, Participant5, Participant6, Participant7, Participant8, Participant9, Participant10):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "ScenarioId": ScenarioId,
  "ExternalMeetingId":ExternalMeetingId,
  "Participants": [
    Participant1, Participant2, Participant3, Participant4, Participant5, Participant6, Participant7, Participant8, Participant9, Participant10
  ],
  "ActivityId": ActivityId,
  "Period": {
    "StartTime": getdate30daysahead_zeroformats()+ "T"+StartMeetingHour+":00:00.000",
    "EndTime": getdate30daysahead_zeroformats()+"T"+EndMeetingHour+":00:00.000"
  },
  "Title": "TimeZoneTest",
  "Location": "Stockholm",
  "Agenda": "meetingjohntest"
}
    payload = json.dumps(requestdata)

    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/AddMeeting", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    assert response.status_code == 200

@pytest.mark.command
@pytest.mark.parametrize("ExternalMeetingId", dataforremovemeetingtimezones)
def test_RemoveMeeting_Timezones(ExternalMeetingId):
    requestdata = {
  "ExternalMeetingId": ExternalMeetingId
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/command/RemoveMeeting", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    assert response.status_code == 200
'''

# below tests are queries
@pytest.mark.queries
def test_AllAbsences():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Absence/AllAbsences", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllAbsences" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string",
                        "minLength": 25,
                        "maxLength": 50
            },
            "Priority": {
                "type": "integer"
            },
            "Name": {
                "type": "string"
            },
            "Requestable": {
                "type": "boolean"
            },
            "InWorkTime": {
                "type": "boolean"
            },
            "InPaidTime": {
                "type": "boolean"
            },
            "PayrollCode": {
                "type": "string"
            },
            "Confidential": {
                "type": "boolean"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AbsencePossibilityByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate45daysahead_zeroformats()
  }
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/AbsencePossibility/AbsencePossibilityByPersonId", headers=headers, data=payload)

    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AbsencePossibilityByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

@pytest.mark.queries
def test_AbsenceRequestById():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "RequestId": fullDayAbsenceRequestID
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/AbsenceRequest/AbsenceRequestById", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AbsenceRequestById" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
  "type": "object",
  "properties": {
        "Id": {
          "type": "string"
        },
        "IsNew": {
          "type": "boolean"
        },
        "IsPending": {
          "type": "boolean"
        },
        "IsWaitlisted": {
          "type": "boolean"
        },
        "IsAlreadyAbsent": {
          "type": "boolean"
        },
        "IsAutoAproved": {
          "type": "boolean"
        },
        "IsAutoDenied": {
          "type": "boolean"
        },
        "IsCancelled": {
          "type": "boolean"
        },
        "IsDeleted": {
          "type": "boolean"
        },
        "IsDenied": {
          "type": "boolean"
        },
        "IsExpired": {
          "type": "boolean"
        }
      }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AbsenceRequestRulesByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate60daysahead_zeroformats()
  }
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/AbsenceRequestRule/AbsenceRequestRulesByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AbsenceRequestRulesByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]["Projection"][0]
    schema = {
        "type": "object",
        "properties": {
            "Period": {
                "type": "object"
            },
            "RequestProcess": {
                "type": "string"
            },
            "PersonAccountValidator": {
                "type": "string"
            },
            "StaffingThresholdValidator": {
                "type": "string"
            },
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllActivities():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Activity/AllActivities", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllActivities" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    #dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    
    "required": [
        "Result",
        "Message"
    ],
    "properties": {
        "Result": {
            "$id": "#/properties/Result",
            "type": "array",
            "title": "The Result schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "Id": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                        "Name": "Phone",
                        "InReadyTime": True,
                        "RequiresSkill": True,
                        "InWorkTime": True,
                        "InPaidTime": True,
                        "ReportLevelDetail": "None",
                        "RequiresSeat": False,
                        "PayrollCode": 'null',
                        "AllowOverwrite": True,
                        "DisplayColor": "#00FF00FF"
                    },
                    {
                        "Id": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                        "Name": "Short break",
                        "InReadyTime": False,
                        "RequiresSkill": False,
                        "InWorkTime": True,
                        "InPaidTime": True,
                        "ReportLevelDetail": "ShortBreak",
                        "RequiresSeat": False,
                        "PayrollCode": 'null',
                        "AllowOverwrite": True,
                        "DisplayColor": "#FF0000FF"
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/Result/items",
                "anyOf": [
                    {
                        "$id": "#/properties/Result/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "Id": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                                "Name": "Phone",
                                "InReadyTime": True,
                                "RequiresSkill": True,
                                "InWorkTime": True,
                                "InPaidTime": True,
                                "ReportLevelDetail": "None",
                                "RequiresSeat": False,
                                "PayrollCode": 'null',
                                "AllowOverwrite": True,
                                "DisplayColor": "#00FF00FF"
                            }
                        ],
                        "required": [
                            "Id",
                            "Name",
                            "InReadyTime",
                            "RequiresSkill",
                            "InWorkTime",
                            "InPaidTime",
                            "ReportLevelDetail",
                            "RequiresSeat",
                            "PayrollCode",
                            "AllowOverwrite",
                            "DisplayColor"
                        ],
                        "properties": {
                            "Id": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/Id",
                                "type": "string",
                                "title": "The Id schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "0ffeb898-11bf-43fc-8104-9b5e015ab3c2"
                                ]
                            },
                            "Name": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/Name",
                                "type": "string",
                                "title": "The Name schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "Phone"
                                ]
                            },
                            "InReadyTime": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/InReadyTime",
                                "type": "boolean",
                                "title": "The InReadyTime schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    True
                                ]
                            },
                            "RequiresSkill": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/RequiresSkill",
                                "type": "boolean",
                                "title": "The RequiresSkill schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    True
                                ]
                            },
                            "InWorkTime": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/InWorkTime",
                                "type": "boolean",
                                "title": "The InWorkTime schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    True
                                ]
                            },
                            "InPaidTime": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/InPaidTime",
                                "type": "boolean",
                                "title": "The InPaidTime schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    True
                                ]
                            },
                            "ReportLevelDetail": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/ReportLevelDetail",
                                "type": "string",
                                "title": "The ReportLevelDetail schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "None"
                                ]
                            },
                            "RequiresSeat": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/RequiresSeat",
                                "type": "boolean",
                                "title": "The RequiresSeat schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    False
                                ]
                            },
                            "PayrollCode": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/PayrollCode",
                                "type": ["null", "string"],
                                "title": "The PayrollCode schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 'null',
                                "examples": [
                                    'null'
                                ]
                            },
                            "AllowOverwrite": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/AllowOverwrite",
                                "type": "boolean",
                                "title": "The AllowOverwrite schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": False,
                                "examples": [
                                    True
                                ]
                            },
                            "DisplayColor": {
                                "$id": "#/properties/Result/items/anyOf/0/properties/DisplayColor",
                                "type": "string",
                                "title": "The DisplayColor schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "#00FF00FF"
                                ]
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        },
        "Message": {
            "$id": "#/properties/Message",
            "type": "null",
            "title": "The Message schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 'null',
            "examples": [
                'null'
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(resp), key=lambda e: e.path)
    print(errors)
    validate(resp, schema)
@pytest.mark.queries
def test_PermissionByPerson():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/ApplicationFunction/PermissionByPerson", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/PermissionByPerson" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string"
            },
            "FunctionCode": {
                "type": "string"
            },
            "FunctionPath": {
                "type": "string"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllBusinessUnits():
    requestdata = {}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/BusinessUnit/AllBusinessUnits", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllBusinessUnits" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string"
            },
            "Name": {
                "type": "string"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllDayOffTemplates():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/DayOffTemplate/AllDayOffTemplates", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllDayOffTemplates" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string"
            },
            "Name": {
                "type": "string"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_OvertimePossibilityByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate7daysahead_zeroformats()
  }
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/OvertimePossibility/OvertimePossibilityByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/OvertimePossibilityByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200 or 204

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]["Period"]
    schema = {
        "type": "object",
        "properties": {
            "StartTime": {
                "type": "string"
            },
            "EndTime": {
                "type": "string"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_OvertimeRequestConfigurationByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": getdate30daysahead_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/OvertimeRequestConfiguration/OvertimeRequestConfigurationByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/OvertimeRequestConfigurationBypersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "OvertimeProbabilityEnabled": {
                "type": "boolean"
            },
            "MaxOvertimeRestriction": {
                "type": "object"
            },
            "MinConsecutiveLunchTimeRestriction": {
                "type": "object"
            },
            "MaxContinuousWorkTimeRestriction": {
                "type": "object"
            } ,
            "MinRestTimeThresholdRestriction": {
                "type": "object"
            },
            "CancellationThresholdInMinute": {
                "type": "integer"
            },
            "OpenPeriod": {
                "type": "object",
                "type": "null"
            },
            "AutoGrant": {
                "type": "object"
            },
            "ContractRestriction": {
                "type": "object"
            },
            "OvertimeTypes": {
                "type": "array"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_OvertimeRequestById():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "RequestId": overTimeRequestId
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/OvertimeRequest/OvertimeRequestById", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/OvertimeRequestById" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "PersonId": {
                "type": "string"
            },
            "Period": {
                "type": "object"
            },
            "OvertimeType": {
                "type": "string"
            },
            "Subject": {
                "type": "string"
            },
            "Message": {
                "type": "string"
            },
            "Status": {
                "type": "object"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_PersonAccountsByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/PersonAccount/PersonAccountsByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/PersonAccountsByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "TrackedBy": {
                "type": "string"
            },
            "Period": {
                "type": "object"
            },
            "Remaining": {
                "type": "integer"
            },
            "AbsenceId": {
                "type": "string"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_PeopleByEmploymentNumbers():
    requestdata = {  "EmploymentNumbers": [
    "137567", "518"
  ],
  "Date": gettodaysdatewith_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Person/PeopleByEmploymentNumbers", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/PeopleByEmploymentNumbers" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string"
            },
            "FirstName": {
                "type": "string"
            },
            "LastName": {
                "type": "string"
            },
            "EmploymentNumber": {
                "type": "string"
            },
            "Email": {
                "type": "string"
            },
            "DisplayName": {
                "type": "string"
            },
            "TimeZoneId": {
                "type": "string"
            },
            "BusinessUnitId": {
                "type": "string"
            },
            "SiteId": {
                "type": "string"
            },
            "TeamId": {
                "type": "string"
            },
            "WorkflowControlSetId": {
                "type": "string"
            },
            "FirstDayOfWeek": {
                "type": "integer"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)

@pytest.mark.queries
def test_PeopleByTeamId():
    requestdata = {
  "TeamId": "D66F60F5-264C-4277-80EB-9B5E015AB495",
  "Date": gettodaysdatewith_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Person/PeopleByTeamId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/PeopleByTeamId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string"
            },
            "FirstName": {
                "type": "string"
            },
            "LastName": {
                "type": "string"
            },
            "EmploymentNumber": {
                "type": "string"
            },
            "Email": {
                "type": "string"
            },
            "DisplayName": {
                "type": "string"
            },
            "TimeZoneId": {
                "type": "string"
            },
            "BusinessUnitId": {
                "type": "string"
            },
            "SiteId": {
                "type": "string"
            },
            "TeamId": {
                "type": "string"
            },
            "WorkflowControlSetId": {
                "type": "string"
            },
            "FirstDayOfWeek": {
                "type": "integer"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_PersonById():
    requestdata = {
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Person/PersonById", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/PersonById" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "Id": {
                "type": "string"
            },
            "FirstName": {
                "type": "string"
            },
            "LastName": {
                "type": "string"
            },
            "EmploymentNumber": {
                "type": "string"
            },
            "Email": {
                "type": "string"
            },
            "DisplayName": {
                "type": "string"
            },
            "TimeZoneId": {
                "type": "string"
            },
            "BusinessUnitId": {
                "type": "string"
            },
            "SiteId": {
                "type": "string"
            },
            "TeamId": {
                "type": "string"
            },
            "WorkflowControlSetId": {
                "type": "string"
            },
            "FirstDayOfWeek": {
                "type": "integer"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)

@pytest.mark.queries
def test_ScheduleAbsencesByPersonIds():
    requestdata = {
  "PersonIds": [
    "B0E35119-4661-4A1B-8772-9B5E015B2564"
  ],
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate60daysahead_zeroformats()
  },
  "ScenarioId": "E21D813C-238C-4C3F-9B49-9B5E015AB432"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/ScheduleAbsence/ScheduleAbsencesByPersonIds", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/ScheduleAbsencesByPersonIds" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
        "type": "object",
        "properties": {
            "PersonId": {
                "type": "string"
            },
            "Date": {
                "type": "string"
            },
            "FullDayAbsence": {
                "type": "null"
            },
            "Shift": {
                "type": "array"
            }
        }
    }

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_SchedulesByChangeDate():
    requestdata = {
  "ChangesFrom": gettodaysdatewith_zeroformats()+"T06:42:03.055Z",
  "ChangesTo": getdate30daysahead_zeroformats()+"T06:42:03.055Z",
  "Page": 0,
  "PageSize": 0,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/ScheduleChanges/SchedulesByChangeDate", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/SchedulesByChangeDate" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Schedules": [],
            "Page": 0,
            "TotalPages": 1,
            "TotalSchedules": 0,
            "ChangesUpTo": "2020-11-05T06:42:03.055Z"
        }
    ],
    "required": [
        "Schedules",
        "Page",
        "TotalPages",
        "TotalSchedules",
        "ChangesUpTo"
    ],
    "properties": {
        "Schedules": {
            "$id": "#/properties/Schedules",
            "type": "array",
            "title": "The Schedules schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                []
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/Schedules/items"
            }
        },
        "Page": {
            "$id": "#/properties/Page",
            "type": "integer",
            "title": "The Page schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "TotalPages": {
            "$id": "#/properties/TotalPages",
            "type": "integer",
            "title": "The TotalPages schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                1
            ]
        },
        "TotalSchedules": {
            "$id": "#/properties/TotalSchedules",
            "type": "integer",
            "title": "The TotalSchedules schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "ChangesUpTo": {
            "$id": "#/properties/ChangesUpTo",
            "type": "string",
            "title": "The ChangesUpTo schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "2020-11-05T06:42:03.055Z"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllScheduleChangesListenerSubscription():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/ScheduleChangesListenerSubscription/AllScheduleChangesListenerSubscription", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllScheduleChangesListenerSubscription" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]["Listeners"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Url": "http://localhost/TeleoptiWFM",
            "Name": "jonhtest",
            "DaysStartFromCurrentDate": 1,
            "DaysEndFromCurrentDate": 4
        }
    ],
    "required": [
        "Url",
        "Name",
        "DaysStartFromCurrentDate",
        "DaysEndFromCurrentDate"
    ],
    "properties": {
        "Url": {
            "$id": "#/properties/Url",
            "type": "string",
            "title": "The Url schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "http://localhost/TeleoptiWFM"
            ]
        },
        "Name": {
            "$id": "#/properties/Name",
            "type": "string",
            "title": "The Name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "jonhtest"
            ]
        },
        "DaysStartFromCurrentDate": {
            "$id": "#/properties/DaysStartFromCurrentDate",
            "type": "integer",
            "title": "The DaysStartFromCurrentDate schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                1
            ]
        },
        "DaysEndFromCurrentDate": {
            "$id": "#/properties/DaysEndFromCurrentDate",
            "type": "integer",
            "title": "The DaysEndFromCurrentDate schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                4
            ]
        }
    },
    "additionalProperties": True
}


    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_ScheduleByPersonId():
    requestdata = {
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": getdate7daysahead_zeroformats(),
    "EndDate": getdate7daysahead_zeroformats()
  },
  "ScenarioId": "E21D813C-238C-4C3F-9B49-9B5E015AB432"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Schedule/ScheduleByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/ScheduleByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "required": [
        "PersonId",
        "Date",
        "Shift"
    ],
    "properties": {
        "PersonId": {
            "$id": "#/properties/PersonId",
            "type": "string",
            "title": "The PersonId schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "b0e35119-4661-4a1b-8772-9b5e015b2564"
            ]
        },
        "Date": {
            "$id": "#/properties/Date",
            "type": "string",
            "title": "The Date schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "2020-10-09"
            ]
        },
        "Shift": {
            "$id": "#/properties/Shift",
            "type": "array",
            "title": "The Shift schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "Name": "Administration",
                        "Period": {
                            "StartTime": "2020-10-09T09:00:00Z",
                            "EndTime": "2020-10-09T10:45:00Z"
                        },
                        "ActivityId": "564b1a0c-4445-42d3-a24c-9b5e015ab3c6",
                        "AbsenceId": 'null',
                        "DisplayColor": -4144897,
                        "ExternalMeetingId": 'null'
                    },
                    {
                        "Name": "Short break",
                        "Period": {
                            "StartTime": "2020-10-09T10:45:00Z",
                            "EndTime": "2020-10-09T11:00:00Z"
                        },
                        "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                        "AbsenceId": 'null',
                        "DisplayColor": -65536,
                        "ExternalMeetingId": 'null'
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/Shift/items",
                "anyOf": [
                    {
                        "$id": "#/properties/Shift/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "Name": "Administration",
                                "Period": {
                                    "StartTime": "2020-10-09T09:00:00Z",
                                    "EndTime": "2020-10-09T10:45:00Z"
                                },
                                "ActivityId": "564b1a0c-4445-42d3-a24c-9b5e015ab3c6",
                                "AbsenceId": 'null',
                                "DisplayColor": -4144897,
                                "ExternalMeetingId": 'null'
                            }
                        ],
                        "required": [
                            "Name",
                            "Period",
                            "ActivityId",
                            "AbsenceId",
                            "DisplayColor",
                            "ExternalMeetingId"
                        ],
                        "properties": {
                            "Name": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/Name",
                                "type": "string",
                                "title": "The Name schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "Administration"
                                ]
                            },
                            "Period": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/Period",
                                "type": "object",
                                "title": "The Period schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "StartTime": "2020-10-09T09:00:00Z",
                                        "EndTime": "2020-10-09T10:45:00Z"
                                    }
                                ],
                                "required": [
                                    "StartTime",
                                    "EndTime"
                                ],
                                "properties": {
                                    "StartTime": {
                                        "$id": "#/properties/Shift/items/anyOf/0/properties/Period/properties/StartTime",
                                        "type": "string",
                                        "title": "The StartTime schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "2020-10-09T09:00:00Z"
                                        ]
                                    },
                                    "EndTime": {
                                        "$id": "#/properties/Shift/items/anyOf/0/properties/Period/properties/EndTime",
                                        "type": "string",
                                        "title": "The EndTime schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "2020-10-09T10:45:00Z"
                                        ]
                                    }
                                },
                                "additionalProperties": True
                            },
                            "ActivityId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/ActivityId",
                                "type": "string",
                                "title": "The ActivityId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "564b1a0c-4445-42d3-a24c-9b5e015ab3c6"
                                ]
                            },
                            "AbsenceId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/AbsenceId",
                                "type": "null",
                                "title": "The AbsenceId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 'null',
                                "examples": [
                                    'null'
                                ]
                            },
                            "DisplayColor": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/DisplayColor",
                                "type": "integer",
                                "title": "The DisplayColor schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 0,
                                "examples": [
                                    -4144897
                                ]
                            },
                            "ExternalMeetingId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/ExternalMeetingId",
                                "type": "null",
                                "title": "The ExternalMeetingId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 'null',
                                "examples": [
                                    'null'
                                ]
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_ScheduleByPersonIds():
    requestdata = {
   "PersonIds": [
    "B0E35119-4661-4A1B-8772-9B5E015B2564"
  ],
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate60daysahead_zeroformats()
  },
  "ScenarioId": "E21D813C-238C-4C3F-9B49-9B5E015AB432"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Schedule/ScheduleByPersonIds", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/ScheduleByPersonIds" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "PersonId": "b0e35119-4661-4a1b-8772-9b5e015b2564",
            "Date": "2020-10-06",
            "Shift": [
                {
                    "Name": "Phone",
                    "Period": {
                        "StartTime": "2020-10-06T08:00:00Z",
                        "EndTime": "2020-10-06T10:00:00Z"
                    },
                    "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                    "AbsenceId": 'null',
                    "DisplayColor": -8323200
                },
                {
                    "Name": "Short break",
                    "Period": {
                        "StartTime": "2020-10-06T10:00:00Z",
                        "EndTime": "2020-10-06T10:15:00Z"
                    },
                    "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -65536
                },
                {
                    "Name": "Phone",
                    "Period": {
                        "StartTime": "2020-10-06T10:15:00Z",
                        "EndTime": "2020-10-06T12:00:00Z"
                    },
                    "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                    "AbsenceId": 'null',
                    "DisplayColor": -8323200
                },
                {
                    "Name": "Lunch",
                    "Period": {
                        "StartTime": "2020-10-06T12:00:00Z",
                        "EndTime": "2020-10-06T13:00:00Z"
                    },
                    "ActivityId": "ba3624b0-0aea-4b72-a585-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -256
                },
                {
                    "Name": "Administration",
                    "Period": {
                        "StartTime": "2020-10-06T13:00:00Z",
                        "EndTime": "2020-10-06T15:00:00Z"
                    },
                    "ActivityId": "564b1a0c-4445-42d3-a24c-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -4144897
                },
                {
                    "Name": "Short break",
                    "Period": {
                        "StartTime": "2020-10-06T15:00:00Z",
                        "EndTime": "2020-10-06T15:15:00Z"
                    },
                    "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -65536
                },
                {
                    "Name": "Phone",
                    "Period": {
                        "StartTime": "2020-10-06T15:15:00Z",
                        "EndTime": "2020-10-06T17:00:00Z"
                    },
                    "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                    "AbsenceId": 'null',
                    "DisplayColor": -8323200
                }
            ]
        }
    ],
    "required": [
        "PersonId",
        "Date",
        "Shift"
    ],
    "properties": {
        "PersonId": {
            "$id": "#/properties/PersonId",
            "type": "string",
            "title": "The PersonId schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "b0e35119-4661-4a1b-8772-9b5e015b2564"
            ]
        },
        "Date": {
            "$id": "#/properties/Date",
            "type": "string",
            "title": "The Date schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "2020-10-06"
            ]
        },
        "Shift": {
            "$id": "#/properties/Shift",
            "type": "array",
            "title": "The Shift schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "Name": "Phone",
                        "Period": {
                            "StartTime": "2020-10-06T08:00:00Z",
                            "EndTime": "2020-10-06T10:00:00Z"
                        },
                        "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                        "AbsenceId": 'null',
                        "DisplayColor": -8323200
                    },
                    {
                        "Name": "Short break",
                        "Period": {
                            "StartTime": "2020-10-06T10:00:00Z",
                            "EndTime": "2020-10-06T10:15:00Z"
                        },
                        "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                        "AbsenceId": 'null',
                        "DisplayColor": -65536
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/Shift/items",
                "anyOf": [
                    {
                        "$id": "#/properties/Shift/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "Name": "Phone",
                                "Period": {
                                    "StartTime": "2020-10-06T08:00:00Z",
                                    "EndTime": "2020-10-06T10:00:00Z"
                                },
                                "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                                "AbsenceId": 'null',
                                "DisplayColor": -8323200
                            }
                        ],
                        "required": [
                            "Name",
                            "Period",
                            "ActivityId",
                            "AbsenceId",
                            "DisplayColor"
                        ],
                        "properties": {
                            "Name": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/Name",
                                "type": "string",
                                "title": "The Name schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "Phone"
                                ]
                            },
                            "Period": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/Period",
                                "type": "object",
                                "title": "The Period schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "StartTime": "2020-10-06T08:00:00Z",
                                        "EndTime": "2020-10-06T10:00:00Z"
                                    }
                                ],
                                "required": [
                                    "StartTime",
                                    "EndTime"
                                ],
                                "properties": {
                                    "StartTime": {
                                        "$id": "#/properties/Shift/items/anyOf/0/properties/Period/properties/StartTime",
                                        "type": "string",
                                        "title": "The StartTime schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "2020-10-06T08:00:00Z"
                                        ]
                                    },
                                    "EndTime": {
                                        "$id": "#/properties/Shift/items/anyOf/0/properties/Period/properties/EndTime",
                                        "type": "string",
                                        "title": "The EndTime schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "2020-10-06T10:00:00Z"
                                        ]
                                    }
                                },
                                "additionalProperties": True
                            },
                            "ActivityId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/ActivityId",
                                "type": "string",
                                "title": "The ActivityId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "0ffeb898-11bf-43fc-8104-9b5e015ab3c2"
                                ]
                            },
                            "AbsenceId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/AbsenceId",
                                "type": "null",
                                "title": "The AbsenceId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 'null',
                                "examples": [
                                    'null'
                                ]
                            },
                            "DisplayColor": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/DisplayColor",
                                "type": "integer",
                                "title": "The DisplayColor schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 0,
                                "examples": [
                                    -8323200
                                ]
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_ScheduleByTeamId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "TeamId": "D66F60F5-264C-4277-80EB-9B5E015AB495",
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate30daysahead_zeroformats()
  },
  "ScenarioId": ""
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Schedule/ScheduleByTeamId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/ScheduleByTeamId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "PersonId": "b0e35119-4661-4a1b-8772-9b5e015b2564",
            "Date": "2020-10-06",
            "Shift": [
                {
                    "Name": "Phone",
                    "Period": {
                        "StartTime": "2020-10-06T08:00:00Z",
                        "EndTime": "2020-10-06T10:00:00Z"
                    },
                    "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                    "AbsenceId": 'null',
                    "DisplayColor": -8323200
                },
                {
                    "Name": "Short break",
                    "Period": {
                        "StartTime": "2020-10-06T10:00:00Z",
                        "EndTime": "2020-10-06T10:15:00Z"
                    },
                    "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -65536
                },
                {
                    "Name": "Phone",
                    "Period": {
                        "StartTime": "2020-10-06T10:15:00Z",
                        "EndTime": "2020-10-06T12:00:00Z"
                    },
                    "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                    "AbsenceId": 'null',
                    "DisplayColor": -8323200
                },
                {
                    "Name": "Lunch",
                    "Period": {
                        "StartTime": "2020-10-06T12:00:00Z",
                        "EndTime": "2020-10-06T13:00:00Z"
                    },
                    "ActivityId": "ba3624b0-0aea-4b72-a585-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -256
                },
                {
                    "Name": "Administration",
                    "Period": {
                        "StartTime": "2020-10-06T13:00:00Z",
                        "EndTime": "2020-10-06T15:00:00Z"
                    },
                    "ActivityId": "564b1a0c-4445-42d3-a24c-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -4144897
                },
                {
                    "Name": "Short break",
                    "Period": {
                        "StartTime": "2020-10-06T15:00:00Z",
                        "EndTime": "2020-10-06T15:15:00Z"
                    },
                    "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                    "AbsenceId": 'null',
                    "DisplayColor": -65536
                },
                {
                    "Name": "Phone",
                    "Period": {
                        "StartTime": "2020-10-06T15:15:00Z",
                        "EndTime": "2020-10-06T17:00:00Z"
                    },
                    "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                    "AbsenceId": 'null',
                    "DisplayColor": -8323200
                }
            ]
        }
    ],
    "required": [
        "PersonId",
        "Date",
        "Shift"
    ],
    "properties": {
        "PersonId": {
            "$id": "#/properties/PersonId",
            "type": "string",
            "title": "The PersonId schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "b0e35119-4661-4a1b-8772-9b5e015b2564"
            ]
        },
        "Date": {
            "$id": "#/properties/Date",
            "type": "string",
            "title": "The Date schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "2020-10-06"
            ]
        },
        "Shift": {
            "$id": "#/properties/Shift",
            "type": "array",
            "title": "The Shift schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "Name": "Phone",
                        "Period": {
                            "StartTime": "2020-10-06T08:00:00Z",
                            "EndTime": "2020-10-06T10:00:00Z"
                        },
                        "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                        "AbsenceId": 'null',
                        "DisplayColor": -8323200
                    },
                    {
                        "Name": "Short break",
                        "Period": {
                            "StartTime": "2020-10-06T10:00:00Z",
                            "EndTime": "2020-10-06T10:15:00Z"
                        },
                        "ActivityId": "90ea529a-eea0-4e22-80ab-9b5e015ab3c6",
                        "AbsenceId": 'null',
                        "DisplayColor": -65536
                    }
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/Shift/items",
                "anyOf": [
                    {
                        "$id": "#/properties/Shift/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "Name": "Phone",
                                "Period": {
                                    "StartTime": "2020-10-06T08:00:00Z",
                                    "EndTime": "2020-10-06T10:00:00Z"
                                },
                                "ActivityId": "0ffeb898-11bf-43fc-8104-9b5e015ab3c2",
                                "AbsenceId": 'null',
                                "DisplayColor": -8323200
                            }
                        ],
                        "required": [
                            "Name",
                            "Period",
                            "ActivityId",
                            "AbsenceId",
                            "DisplayColor"
                        ],
                        "properties": {
                            "Name": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/Name",
                                "type": "string",
                                "title": "The Name schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "Phone"
                                ]
                            },
                            "Period": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/Period",
                                "type": "object",
                                "title": "The Period schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "StartTime": "2020-10-06T08:00:00Z",
                                        "EndTime": "2020-10-06T10:00:00Z"
                                    }
                                ],
                                "required": [
                                    "StartTime",
                                    "EndTime"
                                ],
                                "properties": {
                                    "StartTime": {
                                        "$id": "#/properties/Shift/items/anyOf/0/properties/Period/properties/StartTime",
                                        "type": "string",
                                        "title": "The StartTime schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "2020-10-06T08:00:00Z"
                                        ]
                                    },
                                    "EndTime": {
                                        "$id": "#/properties/Shift/items/anyOf/0/properties/Period/properties/EndTime",
                                        "type": "string",
                                        "title": "The EndTime schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": "",
                                        "examples": [
                                            "2020-10-06T10:00:00Z"
                                        ]
                                    }
                                },
                                "additionalProperties": True
                            },
                            "ActivityId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/ActivityId",
                                "type": "string",
                                "title": "The ActivityId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "0ffeb898-11bf-43fc-8104-9b5e015ab3c2"
                                ]
                            },
                            "AbsenceId": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/AbsenceId",
                                "type": "null",
                                "title": "The AbsenceId schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 'null',
                                "examples": [
                                    'null'
                                ]
                            },
                            "DisplayColor": {
                                "$id": "#/properties/Shift/items/anyOf/0/properties/DisplayColor",
                                "type": "integer",
                                "title": "The DisplayColor schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": 0,
                                "examples": [
                                    -8323200
                                ]
                            }
                        },
                        "additionalProperties": True
                    }
                ]
            }
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllShiftCategories():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/ShiftCategory/AllShiftCategories", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllShiftCategories" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Id": "ec7f6475-1ae7-4a94-83c1-9b5e015ab4c3",
            "Name": "Night",
            "ShortName": "NT"
        }
    ],
    "required": [
        "Id",
        "Name",
        "ShortName"
    ],
    "properties": {
        "Id": {
            "$id": "#/properties/Id",
            "type": "string",
            "title": "The Id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "ec7f6475-1ae7-4a94-83c1-9b5e015ab4c3"
            ]
        },
        "Name": {
            "$id": "#/properties/Name",
            "type": "string",
            "title": "The Name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Night"
            ]
        },
        "ShortName": {
            "$id": "#/properties/ShortName",
            "type": "string",
            "title": "The ShortName schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "NT"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllSites():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Site/AllSites", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllSites" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllTeamsWithAgents():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate30daysahead_zeroformats()
  }
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Team/AllTeamsWithAgents", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllTeamsWithAgents" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Id": "e5f968d7-6f6d-407c-81d5-9b5e015ab495",
            "Name": "London/Students"
        }
    ],
    "required": [
        "Id",
        "Name"
    ],
    "properties": {
        "Id": {
            "$id": "#/properties/Id",
            "type": "string",
            "title": "The Id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "e5f968d7-6f6d-407c-81d5-9b5e015ab495"
            ]
        },
        "Name": {
            "$id": "#/properties/Name",
            "type": "string",
            "title": "The Name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "London/Students"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_TeamById():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "Id": "e5f968d7-6f6d-407c-81d5-9b5e015ab495"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Team/TeamById", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/TeambyId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Id": "e5f968d7-6f6d-407c-81d5-9b5e015ab495",
            "Name": "London/Students"
        }
    ],
    "required": [
        "Id",
        "Name"
    ],
    "properties": {
        "Id": {
            "$id": "#/properties/Id",
            "type": "string",
            "title": "The Id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "e5f968d7-6f6d-407c-81d5-9b5e015ab495"
            ]
        },
        "Name": {
            "$id": "#/properties/Name",
            "type": "string",
            "title": "The Name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "London/Students"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_TeamsBySiteId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "SiteId": "D970A45A-90FF-4111-BFE1-9B5E015AB45C"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/Team/TeamsBySiteId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/TeamsBySiteId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Id": "e5f968d7-6f6d-407c-81d5-9b5e015ab495",
            "Name": "London/Students"
        }
    ],
    "required": [
        "Id",
        "Name"
    ],
    "properties": {
        "Id": {
            "$id": "#/properties/Id",
            "type": "string",
            "title": "The Id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "e5f968d7-6f6d-407c-81d5-9b5e015ab495"
            ]
        },
        "Name": {
            "$id": "#/properties/Name",
            "type": "string",
            "title": "The Name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "London/Students"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_PermissionByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/TeamsAccess/PermissionByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/PermissionByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "HasFullAccess": False,
            "TeamIds": []
        }
    ],
    "required": [
        "HasFullAccess",
        "TeamIds"
    ],
    "properties": {
        "HasFullAccess": {
            "$id": "#/properties/HasFullAccess",
            "type": "boolean",
            "title": "The HasFullAccess schema",
            "description": "An explanation about the purpose of this instance.",
            "default": False,
            "examples": [
                False
            ]
        },
        "TeamIds": {
            "$id": "#/properties/TeamIds",
            "type": "array",
            "title": "The TeamIds schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                []
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/TeamIds/items"
            }
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllTimeZones():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/TimeZone/AllTimeZones", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllTimeZones" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "TimeZone": "America/Denver"
        }
    ],
    "required": [
        "TimeZone"
    ],
    "properties": {
        "TimeZone": {
            "$id": "#/properties/TimeZone",
            "type": "string",
            "title": "The TimeZone schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "America/Denver"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_UserById():
    requestdata = {
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/User/UserById", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/UserById" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Id": "b0e35119-4661-4a1b-8772-9b5e015b2564",
            "FirstName": "Pierre",
            "LastName": "Baldi",
            "EmploymentNumber": "137567",
            "Email": "behrooz.aghakhanian@teleopti.com"
        }
    ],
    "required": [
        "Id",
        "FirstName",
        "LastName",
        "EmploymentNumber",
        "Email"
    ],
    "properties": {
        "Id": {
            "$id": "#/properties/Id",
            "type": "string",
            "title": "The Id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "b0e35119-4661-4a1b-8772-9b5e015b2564"
            ]
        },
        "FirstName": {
            "$id": "#/properties/FirstName",
            "type": "string",
            "title": "The FirstName schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Pierre"
            ]
        },
        "LastName": {
            "$id": "#/properties/LastName",
            "type": "string",
            "title": "The LastName schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Baldi"
            ]
        },
        "EmploymentNumber": {
            "$id": "#/properties/EmploymentNumber",
            "type": "string",
            "title": "The EmploymentNumber schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "137567"
            ]
        },
        "Email": {
            "$id": "#/properties/Email",
            "type": "string",
            "title": "The Email schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "behrooz.aghakhanian@teleopti.com"
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_WeeklyMaxWorkTimeByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith_zeroformats()
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/WeeklyMaxWorkTime/WeeklyMaxWorkTimeByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/WeeklyMaxWorkTimeByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "WeeklyMaxWorkTimeInMinute": 2880
        }
    ],
    "required": [
        "WeeklyMaxWorkTimeInMinute"
    ],
    "properties": {
        "WeeklyMaxWorkTimeInMinute": {
            "$id": "#/properties/WeeklyMaxWorkTimeInMinute",
            "type": "integer",
            "title": "The WeeklyMaxWorkTimeInMinute schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                2880
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.queries
def test_AllWorkflowControlSets():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA"
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/WorkflowControlSet/AllWorkflowControlSets", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/AllWorkflowControlSets)" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200

    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Id": "55d92888-2e81-4fdc-8315-9d9d00a1e9e1",
            "AbsenceRequestExpiredThreshold": 15
        }
    ],
    "required": [
        "Id",
        "AbsenceRequestExpiredThreshold"
    ],
    "properties": {
        "Id": {
            "$id": "#/properties/Id",
            "type": "string",
            "title": "The Id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "55d92888-2e81-4fdc-8315-9d9d00a1e9e1"
            ]
        },
        "AbsenceRequestExpiredThreshold": {
            "$id": "#/properties/AbsenceRequestExpiredThreshold",
            "type": "integer",
            "title": "The AbsenceRequestExpiredThreshold schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                15
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)
@pytest.mark.xfail(reason="needs a schedule for the given person on the given period")
@pytest.mark.queries
def test_WorkTimeByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith_zeroformats(),
    "EndDate": getdate3daysahead_zeroformats()
  }
}
    payload = json.dumps(requestdata)
    headers = {
        'Authorization': apitoken,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", baseurl + "/query/WorkTime/WorkTimeByPersonId", headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Internet connection down")
    else:
        print(response.text.encode('utf8'))

    if (response.status_code != 200):
        file = open("Failedresponses/WorkTimeByPersonId" + gettodaysdatewith_zeroformats() + ".txt", "w")
        file.write(str(response.text.encode('utf8')))
        file.close()

    assert response.status_code == 200



    resp = json.loads(response.text.encode('utf8'))
    dict = resp["Result"][0]
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "TotalWorkTimeInMinutes": 1350,
            "TotalOverTimeInMinutes": 0,
            "TotalContractTimeInMinutes": 1440,
            "TotalPaidTimeInMinutes": 1440
        }
    ],
    "required": [
        "TotalWorkTimeInMinutes",
        "TotalOverTimeInMinutes",
        "TotalContractTimeInMinutes",
        "TotalPaidTimeInMinutes"
    ],
    "properties": {
        "TotalWorkTimeInMinutes": {
            "$id": "#/properties/TotalWorkTimeInMinutes",
            "type": "integer",
            "title": "The TotalWorkTimeInMinutes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                1350
            ]
        },
        "TotalOverTimeInMinutes": {
            "$id": "#/properties/TotalOverTimeInMinutes",
            "type": "integer",
            "title": "The TotalOverTimeInMinutes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                0
            ]
        },
        "TotalContractTimeInMinutes": {
            "$id": "#/properties/TotalContractTimeInMinutes",
            "type": "integer",
            "title": "The TotalContractTimeInMinutes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                1440
            ]
        },
        "TotalPaidTimeInMinutes": {
            "$id": "#/properties/TotalPaidTimeInMinutes",
            "type": "integer",
            "title": "The TotalPaidTimeInMinutes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": 0,
            "examples": [
                1440
            ]
        }
    },
    "additionalProperties": True
}

    err = Draft3Validator(schema)
    errors = sorted(err.iter_errors(dict), key=lambda e: e.path)
    print(errors)
    validate(dict, schema)

