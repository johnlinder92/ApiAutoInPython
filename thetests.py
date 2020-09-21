import csv
import datetime
import json
import time

from selenium.webdriver.chrome.options import Options
import clipboard
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


baseurl = "https://qaeurc02.teleopticloud.com/api"
apitoken = "Y2JjYzk3ZmI4OWQ0NGYwZWJmYThjOTkyOTNlMTk2OWQ2NDZmNzA0ZDAzM2E0NWRlOWVlODM4ZTdmZTAyYTI0YQ=="


#date functions to make requests work over time

def gettodaysdatewith0m0d_zeroformats():
    global date
    date = datetime.datetime.now()
    theday = int(date.day)
    themonth = int(date.month)
    if theday < 10 and themonth < 10:
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        total = year + "-0" + month + "-0" + day
        return total
    elif theday > 9 and themonth < 10:
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        total = year + "-0" + month + "-" + day
        return total
    elif theday < 10 and themonth > 9:
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        total = year + "-" + month + "-0" + day
        return total
    elif theday > 9 and themonth > 9:
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        total = year + "-" + month + "-" + day
        return total
def getdateonemonthahead_zeroformats():
    date = datetime.datetime.now()
    themonth = int(date.month)
    theday = int(date.day)
    if themonth != 12 and theday > 9:

        monthstr = str(themonth +1)

        day2 = str(date.day)
        year = str(date.year)
        total = year + "-" +monthstr + "-" + day2

        return total
    elif themonth == 12 and theday > 9:

        extrayear = int(date.year)
        yearstr = str(extrayear + 1)
        day = str(date.day)

        total = yearstr + "-01-" + day
        return total
    elif themonth != 12 and theday < 10:
        monthstr = str(themonth + 1)
        yearstr=str(date.year)
        day = str(date.day)


        total = yearstr + "-" + monthstr + "-0" + day

        return total
    elif themonth == 12 and theday < 10:
        extrayear = int(date.year)
        yearstr = str(extrayear + 1)
        day = str(date.day)

        total = yearstr + "-01-0" + day
        return total
def getdatetwomonthsahead_zeroformats():
    date = datetime.datetime.now()
    themonth = int(date.month)
    theday = int(date.day)
    if themonth < 11 and theday < 10:

        monthstr = str(themonth +2)
        day2 = str(date.day)
        year = str(date.year)
        total = year + "-" +monthstr + "-0" + day2

        return total
    elif themonth < 11 and theday > 9:

        monthstr = str(themonth + 2)
        day2 = str(date.day)
        year = str(date.year)
        total = year + "-" + monthstr + "-" + day2

        return total

    elif themonth == 11 and theday < 10:


        extrayear= int(date.year)
        yearstr=str(extrayear+1)
        day = str(date.day)


        total = yearstr + "-1-0" + day

        return total
    elif themonth == 11 and theday > 9:

         extrayear = int(date.year)
         yearstr = str(extrayear + 1)
         day = str(date.day)

         total = yearstr + "-1-" + day

         return total
    elif themonth == 12 and theday < 10:

         extrayear = int(date.year)
         yearstr = str(extrayear + 1)
         day = str(date.day)

         total = yearstr + "-2-0" + day

         return total
    elif themonth == 12 and theday > 9:

         extrayear = int(date.year)
         yearstr = str(extrayear + 1)
         day = str(date.day)

         total = yearstr + "-2-" + day

         return total
    else:
         hmm= "error"
         return hmm

#environment variables
# fullDayAbsenceRequestID obtained inside test_AddFullDayAbsenceRequest
# overTimeRequestId obtained inside test_AddOvertimeRequest
fullDayAbsenceRequestID = '8e793f5a-b4c8-40c1-9156-ac3d00bb51a9'

#testdata for the add/remove meeting


@pytest.mark.command
@pytest.mark.queries
@pytest.mark.runfirst
@pytest.mark.flaky(reruns=5)
def test_seleniumtogetAPItoken():


    #chrome_options = Options()

    #chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()
    driver.get("https://qaeurc02.teleopticloud.com")
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
    driver.find_element(By.CSS_SELECTOR, ".ant-input").send_keys("johnapiautomation2")
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, ".ant-form-item-control-input-content > .ng-tns-c129-23").click()
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, ".ant-col > .ant-input").click()

    apitoken2 = clipboard.paste()

    driver.close()
    global apitoken
    apitoken = apitoken2

#these test are commands
with open('csvtestdata/test_AddFullDayAbsence.csv') as f:
 reader = csv.reader(f)
 dataaddfulldayabsence= list(reader)
@pytest.mark.command
@pytest.mark.parametrize("AbsenceId, ScenarioId", dataaddfulldayabsence)
def test_AddFullDayAbsence(AbsenceId,ScenarioId):

     requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": getdateonemonthahead_zeroformats(),
  "AbsenceId": AbsenceId,
  "ScenarioId": ScenarioId
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
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdateonemonthahead_zeroformats()
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

    o = json.loads(response.text.encode('utf8'))
    global fullDayAbsenceRequestID

    fullDayAbsenceRequestID = o.get("Id")

    assert response.status_code == 200
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
    "StartTime": gettodaysdatewith0m0d_zeroformats() + "T16:57:48.068Z",
    "EndTime": gettodaysdatewith0m0d_zeroformats() + "T17:57:48.068Z"
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

    assert response.status_code == 200
with open('csvtestdata/addorremovemeeting.csv') as f:
 reader = csv.reader(f)
 dataforaddmeeting = list(reader)

#using firstrow of that list to remove all created meetings

 dataforremovemeeting = []
 for x in dataforaddmeeting:
    dataforremovemeeting.append(x[0])
@pytest.mark.command
@pytest.mark.parametrize("ExternalMeetingId, Title, StartMeetingHour, EndMeetingHour, ActivityId, TimeZoneId, ScenarioId", dataforaddmeeting)
def test_AddMeeting(ExternalMeetingId, Title, StartMeetingHour, EndMeetingHour, ActivityId, TimeZoneId, ScenarioId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "ScenarioId": ScenarioId,
  "ExternalMeetingId":ExternalMeetingId,
  "Participants": [
    "B0E35119-4661-4A1B-8772-9B5E015B2564"
  ],
  "ActivityId": ActivityId,
  "Period": {
    "StartTime": getdateonemonthahead_zeroformats()+ "T"+StartMeetingHour+":00:00.000",
    "EndTime": getdateonemonthahead_zeroformats()+"T"+EndMeetingHour+":00:00.000"
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
    "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
    "Period": {
        "StartTime":  gettodaysdatewith0m0d_zeroformats() + "T13:56:34.604Z",
        "EndTime":  gettodaysdatewith0m0d_zeroformats() + "T17:56:34.604Z"
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

   z = json.loads(response.text.encode('utf8'))
   global overTimeRequestId
   overTimeRequestId = z.get("Id")
   assert response.status_code == 200

with open('csvtestdata/test_AddPartDayAbsence.csv') as f:
    reader = csv.reader(f)
    addPartDayAbsenceData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("AbsenceId, ScenarioId, TimeZoneId", addPartDayAbsenceData)
def test_AddPartDayAbsence(AbsenceId, ScenarioId, TimeZoneId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartTime": getdateonemonthahead_zeroformats()+"T10:06:03.698Z",
    "EndTime": getdateonemonthahead_zeroformats()+"T16:06:03.698Z"
  },
  "AbsenceId": AbsenceId,
  "ScenarioId": ScenarioId
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

    assert response.status_code == 200
#what does the URL mean/do? below
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

    assert response.status_code == 200
@pytest.mark.command
def test_AddTeam():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "TeamName": "Johnsteam",
  "SiteId": "3C0B7719-557D-4B3A-B349-A7BB00E7E198"
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

    assert response.status_code == 200
with open('csvtestdata/test_RemovePersonAbsence.csv') as f:
    reader = csv.reader(f)
    RemovePersonAbsenceData = list(reader)
@pytest.mark.command
@pytest.mark.parametrize("ScenarioId, TimeZoneId", RemovePersonAbsenceData)
def test_RemovePersonAbsence(ScenarioId, TimeZoneId):
    requestdata = {
  "TimeZoneId": TimeZoneId,
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartTime": gettodaysdatewith0m0d_zeroformats()+"T08:10:09.155Z",
    "EndTime": getdateonemonthahead_zeroformats()+"T16:10:09.155Z"
  },
  "ScenarioId": ScenarioId
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

    assert response.status_code == 200
@pytest.mark.command
def test_SetSchedulesForPerson():
    requestdata = {
  "TimeZoneId": "Europe/Stockholm",
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "DatePeriod": {
    "StartDate": getdateonemonthahead_zeroformats(),
    "EndDate": getdatetwomonthsahead_zeroformats()
  },
  "ScheduleDays": [
    {
      "Date": getdateonemonthahead_zeroformats(),
      "ShiftCategoryId": "EC7F6475-1AE7-4A94-83C1-9B5E015AB4C3",
      #"DayOffTemplateId": "F2F35A09-9453-4944-A3F7-550DC06EA0FF",
      "FullDayAbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330",
      "Layers": [
        {
          "Period": {
            "StartTime": getdateonemonthahead_zeroformats()+"T08:18:00.000",
            "EndTime": getdateonemonthahead_zeroformats()+"T16:18:00.000"
          },
          "ActivityId": "0FFEB898-11BF-43FC-8104-9B5E015AB3C2",
          #"AbsenceId": "47D9292F-EAD6-40B2-AC4F-9B5E015AB330"
        }
      ]
    }
  ],
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "ScenarioId": "E21D813C-238C-4C3F-9B49-9B5E015AB432"
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

    assert response.status_code == 200


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

    assert response.status_code == 200
@pytest.mark.queries
def test_AbsencePossibilityByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdateonemonthahead_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_AbsenceRequestRulesByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdatetwomonthsahead_zeroformats()
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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_OvertimePossibilityByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdateonemonthahead_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_OvertimeRequestConfigurationByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": getdateonemonthahead_zeroformats()
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_PersonAccountsByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith0m0d_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_PeopleByEmploymentNumbers():
    requestdata = {  "EmploymentNumbers": [
    "137567", "518"
  ],
  "Date": gettodaysdatewith0m0d_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_PeopleByTeamId():
    requestdata = {
  "TeamId": "30E6530B-3271-470C-852F-AA6C00E7E732",
  "Date": gettodaysdatewith0m0d_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_PersonById():
    requestdata = {
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith0m0d_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.xfail(reason="known issue(if you set WFM_API_UseScope_91609 toggle to false and restart WFM system it works)")
@pytest.mark.queries
def test_ScheduleAbsencesByPersonIds():
    requestdata = {
  "PersonIds": [
    "B0E35119-4661-4A1B-8772-9B5E015B2564"
  ],
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdatetwomonthsahead_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_SchedulesByChangeDate():
    requestdata = {
  "ChangesFrom": gettodaysdatewith0m0d_zeroformats()+"T06:42:03.055Z",
  "ChangesTo": getdateonemonthahead_zeroformats()+"T06:42:03.055Z",
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_ScheduleByPersonId():
    requestdata = {
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdatetwomonthsahead_zeroformats()
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
    assert response.status_code == 200
@pytest.mark.queries
def test_ScheduleByPersonIds():
    requestdata = {
   "PersonIds": [
    "B0E35119-4661-4A1B-8772-9B5E015B2564"
  ],
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdatetwomonthsahead_zeroformats()
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
    assert response.status_code == 200
#The scenario ID in test below has to be added, cannot find one that works in a fresh installation
@pytest.mark.queries
def test_ScheduleByTeamId():
    requestdata = {
  "BusinessUnitId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "TeamId": "1F795D99-A8B1-473B-BAD3-ABA500EF4D59",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdateonemonthahead_zeroformats()
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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_AllTeamsWithAgents():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdateonemonthahead_zeroformats()
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_TeamsBySiteId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "SiteId": "3C0B7719-557D-4B3A-B349-A7BB00E7E198"
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
    assert response.status_code == 200
@pytest.mark.queries
def test_PermissionByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith0m0d_zeroformats()
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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_WeeklyMaxWorkTimeByPersonId():
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Date": gettodaysdatewith0m0d_zeroformats()
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
    assert response.status_code == 200
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
    assert response.status_code == 200
@pytest.mark.queries
def test_WorkTimeByPersonId(benchmark):
    requestdata = {
  "BusinessUnitId": "928DD0BC-BF40-412E-B970-9B5E015AADEA",
  "PersonId": "B0E35119-4661-4A1B-8772-9B5E015B2564",
  "Period": {
    "StartDate": gettodaysdatewith0m0d_zeroformats(),
    "EndDate": getdateonemonthahead_zeroformats()
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
    benchmark(time.sleep, 0.02)
    assert response.status_code == 200
