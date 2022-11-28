import time
from typing import Dict, Any

import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from fyers_api import fyersModel, accessToken
from nsepython import *
import requests, json, datetime

# from django.views.decorators.csrf import csrf_exempt
session = accessToken.SessionModel(client_id='YUBD35U8OF-100', secret_key='TJFZARII4E',
                                   redirect_uri='http://127.0.0.1:8000/user/', response_type='code',
                                   grant_type='authorization_code')

config = {
    "client_id": "YUBD35U8OF-100",
    "secret_key": "TJFZARII4E",
    "access_token": ""
}

def index(request):
    return render(request, 'main.html')
    # return HttpResponse("Hello World")


def tt(request):
    return render(request, 'main.html')


# @csrf_exempt
def test(request):
    response = "HOLA"
    data = json.loads(request.body)
    tag = data['symbol']
    return JsonResponse({'response': tag})
    # return HttpResponse(response)

def get_expiry(request):
    data = json.loads(request.body)
    symbol = data['symbol']
    expiry_number = data['expiry_number']
    return JsonResponse({'response': expiry_list(symbol)[expiry_number]})


def check_file(request):
    response = "HOLA"
    today_date = datetime.date.today().strftime('%d%m%Y')
    file_path = staticfiles_storage.path('logs') + '/' + today_date + '.json'
    if os.path.exists(file_path) == True:
        return JsonResponse({'response': 1})
    else:
        return JsonResponse({'response': 0})
    # return JsonResponse({'response': response})

def execute_trade(request):
    today_date = datetime.date.today().strftime('%d%m%Y')
    file_path = staticfiles_storage.path('logs') + '/' + today_date + '.json'
    if os.path.exists(file_path) == True:
        # file = json.load(open(file_path, 'r'))
        dataToWrite = {
            'response': 1
        }
        return JsonResponse({'response': dataToWrite})
    else:
        # spotPrice = config["fyers"].quotes({"symbols": "NSE:NIFTYBANK-INDEX"})
        # expiry_date = config["expiry_date_banknifty"]
        spotPrice = round(43000 / 100)
        expiry_date = '22D01'
        buyGap = 15
        sellGap = 3
        CE_Buy_StrikeSymbol = 'NSE:BANKNIFTY' + expiry_date + str(
            (spotPrice + buyGap + sellGap + (5 - ((spotPrice + buyGap + sellGap) % 5))) * 100) + 'CE'
        PE_Buy_StrikeSymbol = 'NSE:BANKNIFTY' + expiry_date + str(
            (spotPrice - buyGap - sellGap - ((spotPrice - buyGap - sellGap) % 5)) * 100) + 'PE'
        CE_Sell_StrikeSymbol = 'NSE:BANKNIFTY' + expiry_date + str((spotPrice + sellGap) * 100) + 'CE'
        PE_Sell_StrikeSymbol = 'NSE:BANKNIFTY' + expiry_date + str((spotPrice - sellGap) * 100) + 'PE'

        orderData_Buy = [{
            "symbol": CE_Buy_StrikeSymbol,
            "qty": 25,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "disclosedQty": 0,
            "validity": "DAY",
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0
        },
            {
                "symbol": PE_Buy_StrikeSymbol,
                "qty": 25,
                "type": 2,
                "side": 1,
                "productType": "INTRADAY",
                "limitPrice": 0,
                "stopPrice": 0,
                "disclosedQty": 0,
                "validity": "DAY",
                "offlineOrder": "False",
                "stopLoss": 0,
                "takeProfit": 0
            }]

        orderData_Sell = [{
            "symbol": CE_Sell_StrikeSymbol,
            "qty": 25,
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "disclosedQty": 0,
            "validity": "DAY",
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0
        },
            {
                "symbol": PE_Sell_StrikeSymbol,
                "qty": 25,
                "type": 2,
                "side": 1,
                "productType": "INTRADAY",
                "limitPrice": 0,
                "stopPrice": 0,
                "disclosedQty": 0,
                "validity": "DAY",
                "offlineOrder": "False",
                "stopLoss": 0,
                "takeProfit": 0
            }]

        # config["fyers"].place_basket_orders(orderData_Buy)
        # time.sleep(1)
        # config["fyers"].place_basket_orders(orderData_Sell)

        dataToWrite = {
            'response': 0,
            'strikes': [],
            'strikesLTPEntry': ['ADD LATER'],
            'spotLTPEntry': 'ADD LATER',
            'orderData': [],
            'orderEntryResponse': []
        }
        dataToWrite['strikes'].append(CE_Buy_StrikeSymbol)
        dataToWrite['strikes'].append(PE_Buy_StrikeSymbol)
        dataToWrite['strikes'].append(CE_Sell_StrikeSymbol)
        dataToWrite['strikes'].append(PE_Sell_StrikeSymbol)

        dataToWrite['orderData'].append(orderData_Buy)
        dataToWrite['orderData'].append(orderData_Sell)

        file = open(file_path, 'w')
        json.dump(dataToWrite, file)
        file.close()
        print('FILE CREATED')
        file_json = json.load(open(file_path, 'r'))
        print(file_json)
        send_telegram_message(dataToWrite['strikes'])
        return JsonResponse({'response': file_json})

    # return JsonResponse({'response': 'DONE'})

def exit_trade(request):
    today_date = datetime.date.today().strftime('%d%m%Y')
    file_path = staticfiles_storage.path('logs') + '/' + today_date + '.json'
    if os.path.exists(file_path) == True:
        # file = json.load(open(file_path, 'r'))
        # spotPrice = config["fyers"].quotes({"symbols": "NSE:NIFTYBANK-INDEX"})

        exitOrderData_Sell = [{
                                "id": "CE SELL ORDER ID"
                            },
                                {
                                    "id": "PE SELL ORDER ID"
                                }]
        exitOrderData_Buy = [{
                                "id": "CE BUY ORDER ID"
                            },
                                {
                                    "id": "PE BUY ORDER ID"
                                }]

        # config["fyers"].exit_positions(exitOrderData_Sell)
        # time.sleep(1)
        # config["fyers"].exit_positions(exitOrderData_Buy)

        dataToWrite = {
            'strikesLTPExit': ['ADD LATER'],
            'spotLTPExit': 'ADD LATER',
            'orderExitResponse': []
        }

        # file = open(file_path, 'w')
        # json.dump(dataToWrite, file)
        # file.close()
        # print('FILE CREATED')
        file = json.load(open(file_path, 'r'))
        combinedDataToWrite = dict(list(file.items()) + list(dataToWrite.items()))
        file = open(file_path, 'w')
        json.dump(combinedDataToWrite, file)
        file.close()
        print('FILE CREATED')
        file = json.load(open(file_path, 'r'))
        print(file)
        send_telegram_message(dataToWrite['strikesLTPExit'])
        return JsonResponse({'response': file})
    else:
        dataToWrite = {
            'response': 1
        }
        return JsonResponse({'response': dataToWrite})


    # return JsonResponse({'response': 'DONE'})


def send_telegram_message(request):
    bot_token = '5969891290:AAE13zPtwdc2P3VqZy6o_7opvRHbAtH_vfE'
    bot_chatID = '998029180'
    message = request
    apiURL = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': bot_chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)
    return HttpResponse("Hello World")


def get_data(request):
    # access_token = config["access_token"]
    # fyers = fyersModel.FyersModel(client_id='YUBD35U8OF-100', token=access_token, log_path="/home/Desktop/apiV2")
    # data1 = {"symbol":"NSE:SBIN-EQ","resolution":"5","date_format":"0","range_from":"1622097600","range_to":"1622097685","cont_flag":"1"}
    requested_data = json.loads(request.body)
    received_data = config["fyers"].history(requested_data)
    return JsonResponse({'response': received_data})


def token_view(request):
    # from fyers_api import fyersModel,accessToken
    # session=accessToken.SessionModel(client_id='YUBD35U8OF-100',secret_key='TJFZARII4E',redirect_uri='https://www.google.com', response_type='code', grant_type='authorization_code')
    response = session.generate_authcode()

    return render(request, 'token.html', {'response': response})

def user_detail(request):
    auth_code = request.GET.get('auth_code')
    session.set_token(auth_code)
    response = session.generate_token()
    access_token = response["access_token"]
    config["access_token"] = response["access_token"]

    expiry_date_banknifty = expiry_list('BANKNIFTY')[0] + ' 20:00:00'
    expiry_date_banknifty = int(time.mktime(time.strptime(expiry_date_banknifty, '%d-%b-%Y %H:%M:%S')))
    instruments = pd.read_csv('https://public.fyers.in/sym_details/NSE_FO.csv', header=None)
    ism = instruments[instruments[13] == '{}'.format('BANKNIFTY')]
    config["expiry_date_banknifty"] = ism[9].tolist()[ism[8].tolist().index(expiry_date_banknifty)][13:-7]
    print(config["expiry_date_banknifty"])

    config["fyers"] = fyersModel.FyersModel(client_id='YUBD35U8OF-100', token=access_token, log_path="/home/Desktop/apiV2")
    new_link = "/"
    return render(request, 'token.html', {'response': new_link})
