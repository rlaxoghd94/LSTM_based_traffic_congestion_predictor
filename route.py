from flask import Flask, request, render_template
from flask_cors import CORS
import pandas as pd
import os
import time
import numpy as np
import json
from crawling_tool import parseURL

# 서울외곽순환도로
up_1000 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H1002&roadIdE=H1001&roadName=%EC%84%9C%EC%9A%B8%EC%99%B8%EA%B3%BD%EC%88%9C%ED%99%98%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=E&state=small&onPage=&noTab='
down_1000 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H1002&roadIdE=H1001&roadName=%EC%84%9C%EC%9A%B8%EC%99%B8%EA%B3%BD%EC%88%9C%ED%99%98%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=S&state=small&onPage=&noTab='

# 경인고속도로
up_1200 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H1202&roadIdE=H1201&roadName=%EA%B2%BD%EC%9D%B8%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=E&state=small&onPage=&noTab='
down_1200 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H1202&roadIdE=H1201&roadName=%EA%B2%BD%EC%9D%B8%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=S&state=small&onPage=&noTab='

# 서해안고속도로
up_0150 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H0152&roadIdE=H0151&roadName=%EC%84%9C%ED%95%B4%EC%95%88%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=E&state=small&onPage=&noTab='
down_0150 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H0152&roadIdE=H0151&roadName=%EC%84%9C%ED%95%B4%EC%95%88%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=S&state=small&onPage=&noTab='

# 서울양양고속도로
up_0600 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H0604&roadIdE=H0603&roadName=%EC%84%9C%EC%9A%B8%EC%96%91%EC%96%91%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=E&state=small&onPage=&noTab='
down_0600 = 'http://www.roadplus.co.kr/trafficState.do?roadIdS=H0604&roadIdE=H0603&roadName=%EC%84%9C%EC%9A%B8%EC%96%91%EC%96%91%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C&mCode=A050010&op=highwayItem&highway=&bound=S&state=small&onPage=&noTab='

app = Flask(__name__, template_folder='templates', static_url_path='/static')
CORS(app)

tempData = {}


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/redefined')
def redefined():
    return render_template('refined_index.html', data=json.dumps(tempData))


@app.route("/tempData")
def geo_code():
    return json.dumps(tempData)


@app.route('/getChartData/<roadName>')
def getData(roadName):
    global tempData
    road = roadName[:-2]
    url = ""

    if '1000_E' in roadName:
        url = up_1000
        print()
    elif '1000_S' in roadName:
        url = down_1000
        print()
    elif '1200_E' in roadName:
        url = up_1200
        print()
    elif '1200_S' in roadName:
        url = down_1200
        print()
    elif '0150_E' in roadName:
        url = up_0150
        print()
    elif '0150_S' in roadName:
        url = down_0150
        print()
    elif '0600_E' in roadName:
        url = up_0600
        print()
    elif '0600_S' in roadName:
        url = up_0600
        print()
    else:
        print('\t[+] ERROR in roadName request - {}'.format(roadName))
        return

    parsedList = parseURL(url)
    data = formatData(roadName[-1], parsedList, road)
    temp_csv(data, road)
    print(tempData)
    return json.dumps(tempData)


def temp_csv(data, road):
    global tempData
    csv_E = pd.read_csv('1000_E.csv')
    currentHr = int(time.strftime("%H")) + 12
    pastFutureData = csv_E.values[0:, currentHr + 1:currentHr + 4]
    tempData['data'] = pastFutureData.tolist()
    combineData(data, road)


def init():
    global tempData
    parsedE_1000 = parseURL(up_1000)
    parsedS_1000 = parseURL(down_1000)
    dataE_1000 = formatData("E", parsedE_1000, '1000')
    dataS_1000 = formatData("S", parsedS_1000, '1000')
    # parsedE_1200 = parseURL(up_1200)
    # parsedS_1200 = parseURL(down_1200)
    # dataE_1200 = formatData("E", parsedE_1200, '1200')
    # dataE_1200 = formatData("S", parsedS_1200, '1200')
    # parsedE_0150 = parseURL(up_0150)
    # parsedS_0150 = parseURL(down_0150)
    # dataE_0150 = formatData("E", parsedE_0150, '0150')
    # dataE_0150 = formatData("S", parsedS_0150, '0150')
    # parsedE_0600 = parseURL(up_0600)
    # parsedS_0600 = parseURL(down_0600)
    # dataE_0600= formatData("E", parsedE_0600, '0600')
    # dataE_0600= formatData("S", parsedS_0600, '0600')

    csv_E = pd.read_csv('1000_E.csv')
    csv_S = pd.read_csv('1000_S.csv')
    currentHr = int(time.strftime("%H")) + 12

    pastFutureData_E = csv_E.values[0:, currentHr - 3:currentHr + 3]
    pastFutureData_S = csv_S.values[0:, currentHr - 3:currentHr + 3]
    print(currentHr)
    tempData['E'] = pastFutureData_E.tolist()
    tempData['S'] = pastFutureData_S.tolist()
    # print(tempData)
    combineData(parsedE_1000, parsedS_1000, '1000')
    print(tempData)


def formatData(direction, sectionList, name):
    data = {}
    data['road'] = name
    data['direction'] = direction
    data['data'] = sectionList['data']
    data['name'] = sectionList['name']

    # savedict = open('output1.txt', 'w')
    # savedict.write(str(data))
    # savedict.close()
    return data


def combineData(sectionList, name):
    global tempData
    tempData['road'] = name
    temp = insertCurrentData(tempData['data'], sectionList['data'])
    tempData['data'] = temp
    tempData['name'] = sectionList['name']
    tempData['direction'] = sectionList['direction']


def insertCurrentData(sectionList, currentList):
    sectionListLen = len(sectionList)
    i = 0
    for rowData in sectionList:
        rowData.insert(0, int(currentList[i]))
        i += 1

    return sectionList


if __name__ == '__main__':
    print('main')
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '8080')))
else:
    print('fucking sub')
