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

baseurl = "https://test.com//api"
apitoken = "NTc1YWM4ZjIzMmFmNDgyYmE1ZjViNDAyZmE2OTNiNzU0YjVkZDI1NjZkNGE0M2JmYjc4ODRlZGFjODAwMGFhMQ=="


#databaseconnection

cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                             "Server=test.database.windows.net;"
                             "Database=test_devtest_app;"
                             "uid=Test;pwd=test")

#date functions to make requests work over time
def getdate30daysahead_zeroformats():
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=30)
    future = now + diff
    result = future.strftime("%Y-%m-%d")
    return result


#environment variables
# fullDayAbsenceRequestID obtained inside test_AddFullDayAbsenceRequest
# overTimeRequestId obtained inside test_AddOvertimeRequest
fullDayAbsenceRequestID = '8e793f5a-b4c8-40c1-9156-ac3d00bb51a9'
overTimeRequestId = '30fadb41-90b5-48dd-832f-ac3e00c0e8a7'

#Seleniumtest to get API-token


def test_DatabaseConnection():
    cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                            "Server=test.database.windows.net;"
                            "Database=devtest_app;"
                            "uid=Test;pwd=test")
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


     #select everything the easy way but doesn't work for other db tables
     test = str(pd.read_sql_query("SELECT TOP 1 * FROM [dbo].[Person] ORDER BY ID DESC", cnxn))
     print(test)


     dblastname = str(pd.read_sql_query("SELECT TOP 1 LastName FROM [dbo].[Person] ORDER BY ID DESC", cnxn))
     dbfirstname = str(pd.read_sql_query("SELECT TOP 1 FirstName FROM [dbo].[Person] ORDER BY ID DESC", cnxn))

     lastname = re.findall("TestJohn", dblastname)
     firstname = re.findall("JohnTest", dbfirstname)


     assert lastname == ['TestJohn']
     assert firstname == ['JohnTest']

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
