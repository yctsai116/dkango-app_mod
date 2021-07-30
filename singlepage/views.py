import json
from json import JSONDecodeError

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import OperatorInfo, RequestDetailsForm
from .models import SentRequests

import pandas as pd

import requests
import json

# ==================================run on AP server=============================
# url = "http://localhost:8443/demandDepositAccountInformation"
# ============================================================
# The sender code, operator code and unit code should be filled via web interface
# ============================================================
# api_reqj={
# "header":{
#   "msgNo":"UP0185_20161111195800_001",
#   "txnCode":"1010101",
#   "txnTime":"2021-11-11 19:58:00",
#   "senderCode": "UP0185",
#   "receiveCode":"up0185",
#   "operatorCode":"21853",
#   "unitCode":"C105",
#   "authorizerCode":"12345"
# },
# "requestBody":{
#   "params":{
#     "identifyType":"1",
#     "custId":"",
#     "custName":"",
#     "birthDt":"",
#     "cbCustId":"A123456789",
#     "ccCustId":""
#   }
# }
# }
# ===============================end request data===============
# request api w/ url and request json (run local AP server
# api_reqj = requests.post(url, json=api_reqj).json()

# ==================the expact response==========================================

api_resj = {'requestModel': {
    "header": {
        "msgNo": "UP0185_20161111195800_001",
        "txnCode": "1010101",
        "txnTime": "2021-11-11 19:58:00",
        "senderCode": "UP0185",
        "receiveCode": "up0185",
        "operatorCode": "21853",
        "unitCode": "C105",
        "authorizerCode": "12345"
    },
    "requestBody": {
        "params": {
            "identifyType": "1",
            "custId": "",
            "custName": "",
            "birthDt": "",
            "cbCustId": "A123456789",
            "ccCustId": ""
        }
    }},
    'resultCode': '0000',
    'resultDescription': 'success',
    "resultBody": {'resultJson':
                       [{"verifyCode": "0000",
                         "verufyDescription": "success",
                         "versionType": "S",
                         "isManageNote": "N",
                         "items":
                             [{"cbCustId": "A123456789",
                               "demandDepositAcct": "9216968000449",
                               "acctType": "Living Account",
                               "curr": "TWD",
                               "openAcctDate": "20200811",
                               "digitalSavingAcctMark": "NotDigitalAcct",
                               "realBlnc": 9.0,
                               "prodName": "blablablabla",
                               "lastMonthAvgAccrNo": None,
                               "acctStatus": "normal"},
                              {"cbCustId": "A123456789",
                               "demandDepositAcct": "9216968000488",
                               "acctType": "Saving Account",
                               "curr": "TWD",
                               "openAcctDate": "20200811",
                               "digitalSavingAcctMark": "NotDigitalAcct",
                               "realBlnc": 131313.0,
                               "prodName": "blablablabla",
                               "lastMonthAvgAccrNo": None,
                               "acctStatus": "normal"},
                              {"cbCustId": "A123456789",
                               "demandDepositAcct": "9216968000466",
                               "acctType": "Saving Account",
                               "curr": "TWD",
                               "openAcctDate": "20200811",
                               "digitalSavingAcctMark": "NotDigitalAcct",
                               "realBlnc": 5566.0,
                               "prodName": "blablablabla",
                               "lastMonthAvgAccrNo": None,
                               "acctStatus": "normal"},
                              {"cbCustId": "A123456789",
                               "demandDepositAcct": "9216968000477",
                               "acctType": "Saving Account",
                               "curr": "TWD",
                               "openAcctDate": "20200811",
                               "digitalSavingAcctMark": "NotDigitalAcct",
                               "realBlnc": 778888.0,
                               "prodName": "blablablabla",
                               "lastMonthAvgAccrNo": None,
                               "acctStatus": "normal"}
                              ]
                         }]
                   }}

# ===============================extract the main part of the api response=============================
api_resj_m = api_resj["resultBody"]["resultJson"][0]["items"]


# Create your views here.
def index(request):
    if request.method == 'GET':
        form = OperatorInfo()
        context = {"form": form, "title": "Your Test Dashboard"}
        return render(request, "singlepage/api_configuration.html", context)
    else:
        form = OperatorInfo(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            headers = {
                "msgNo": cleaned_data["msgNo"],
                "txnCode": cleaned_data["txnCode"],
                "txnTime": cleaned_data["txnTime"],
                "senderCode": cleaned_data["senderCode"],
                "receiveCode": cleaned_data["receiveCode"],
                "operatorCode": cleaned_data["operatorCode"],
                "unitCode": cleaned_data["unitCode"],
                "authorizerCode": cleaned_data["authorizerCode"]
            }

            request_body = {
                "identityType": cleaned_data["identityType"],
                "custId": cleaned_data["custId"],
                "custName": cleaned_data["custName"],
                "birthDt": cleaned_data["birthDt"],
                "cbCustId": cleaned_data["cbCustId"],
                "ccCustId": cleaned_data["ccCustId"],
            }

            context = {"request_body": request_body, "headers": headers, "title": "Your Test Dashboard"}
            request.session["data"] = context
            return render(request, "singlepage/api_urls.html", context)


def api_data(request):
    return render(request, "singlepage/api_configuration.html")


def api_details(request, id):
    if "data" not in request.session:
        if "requests" in request.session["data"]:
            return HttpResponseRedirect("/")

    sent_request = SentRequests.objects.get(id=id)
    context = {
        "obj": sent_request,
        "title": sent_request.name,
        "form": RequestDetailsForm()
    }

    if "data" in request.session:
        context = {**context, **request.session["data"]}

    if request.method == "POST":
        form = RequestDetailsForm(request.POST)
        if form.is_valid():
            notes = form.cleaned_data["notes"]
            api_content = form.cleaned_data["api_content"]

            sent_request.notes = notes
            # sent_request.api_content = api_content
            sent_request.save()

            for api_request in request.session["data"]["requests"]:
                if api_request["id"] == id:
                    api_request["api_content"] = api_content
                    request.session.modified = True

    api_content = ""
    for api_request in request.session["data"]["requests"]:
        if api_request["id"] == id:
            api_content = api_request["api_content"]

    context["api_content"] = api_content

    return render(request, "singlepage/api_details.html", context)


def api_response(request):
    if "data" not in request.session:
        return HttpResponseRedirect("/")

    if request.method == "GET":
        if "requests" not in request.session["data"]:
            return HttpResponseRedirect("/")
        else:
            context = {**request.session["data"], "title": "Overall Performance"}
            return render(request, "singlepage/api_response.html", context)

    elif request.method == "POST":
        host = "https://www.netflix.com"

        data = request.session["data"]
        session_request_body = data["request_body"]
        session_request_headers = data["headers"]

        sent_requests = list()

        request_body = json.loads(request.body)
        for api_path in request_body.values():
            req = requests.post(f"{host}/{api_path}", data=data["request_body"], headers=data["headers"])
            try:
                response = req.json()
            except JSONDecodeError:
                response = {}

            saved_req, saved = SentRequests.objects.update_or_create(
                name=api_path,
                unit_code=session_request_headers["unitCode"],
                customer_id=session_request_body["cbCustId"],
                api_request=req.status_code,
            )

            sent_requests.append(saved_req.serialize(api_content=response))
            request.session["data"] = {"requests": sent_requests, **request.session["data"]}

    context = {"title": "Overall Performance", **request.session["data"]}
    return render(request, "singlepage/api_response.html", context)


def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(pd.DataFrame([api_resj_m[num - 1]], index=None).to_html())
    else:
        raise Http404("No such section")


def operator_info(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OperatorInfo(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            senderCode = form.cleaned_data['senderCode']
            operatorCode = form.cleaned_data['operatorCode']
            unitCode = form.cleaned_data['unitCode']
            identifyType = form.cleaned_data['identifyType']
            cbCustId = form.cleaned_data['cbCustId']
            ccCustId = form.cleaned_data['ccCustId']
            custId = form.cleaned_data['custId']
            birthDt = form.cleaned_data['birthDt']
            custName = form.cleaned_data['custName']
            # redirect to a new URL:
            return render(request, 'singlepage/index.html', {
                'senderCode': senderCode,
                'operatorCode': operatorCode,
                'unitCode': unitCode,
                'identifyType': identifyType,
                'cbCustId': cbCustId,
                'ccCustId': ccCustId,
                'custId': custId,
                'birthDt': birthDt,
                'custName': custName
            })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OperatorInfo()

    return render(request, 'singlepage/operator_info.html', {'form': form})
