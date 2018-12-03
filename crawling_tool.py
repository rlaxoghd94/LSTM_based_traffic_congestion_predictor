import requests
import lxml.html as lh
import pandas as pd


def parseURL(url):
    # create a handle, page, to handle the contents of the website
    page = requests.get(url)

    # store the contents of the website under doc
    doc = lh.fromstring(page.content)

    # parse <tr>
    tr_elements = doc.xpath("/html/body/div[@id='wrapper']/div[@id='container']//tr")

    # create empty list
    col = []
    i = 0

    # for each row, store each first element (header) and an empty list
    for tr_data in tr_elements:
        td_elements = doc.xpath("/html/body/div[@id='wrapper']/div[@id='container']//tr[{}]//td".format(i))
        j = 0

        '''
        rowData[]
        1. 구간시점
        2. 구간종점
        3. 속도
        4. 거리
        '''
        rowData = []

        for td_data in td_elements:
            # print('\t[{}] {} - {}'.format(j, td_data.text_content(), type(td_data)))
            if i == 2:
                if j == 1:
                    # section
                    rowData.append(td_data.text_content())
                elif j == 3:
                    # terminal section
                    rowData.append(td_data.text_content())
                elif j == 4:
                    # speed
                    rowData.append(td_data.text_content())
                elif j == 5:
                    # duration
                    rowData.append(td_data.text_content())
            else:
                if j == 0:
                    # section
                    rowData.append(td_data.text_content())
                elif j == 2:
                    # terminal section
                    rowData.append(td_data.text_content())
                elif j == 3:
                    # speed
                    rowData.append(td_data.text_content())
                elif j == 4:
                    # duration
                    rowData.append(td_data.text_content())
            j += 1
        col.append(rowData)
        i += 1

    # print col for safety
    del col[0]  # MUST del first and last element
    del col[-1]  # it contains empty elements

    # printCol(col)
    col = dataInpection(col)
    # printCol(col)
    return refineData(col)


def printCol(col):
    k = 0
    for row in col:
        print('\t[{}] row'.format(k))
        for elem in row:
            print('\t\t[+] - {}'.format(elem))
        k += 1

    '''
    rowData[]
    0. 구간시점
    1. 구간종점
    2. 속도
    3. 거리
    '''


def dataInpection(col):
    colLen = len(col)
    nextIdx = 1
    curIdx = 0

    while nextIdx != (colLen - 1):
        cur = col[curIdx]
        next = col[nextIdx]
        if '휴게소' in cur[1]:
            tempP = cur[1]
            cur[1] = next[1]
            curSpeed = cur[2]
            nextSpeed = next[2]
            cur[2] = str(int((int(curSpeed[:-4]) + int(nextSpeed[:-4])) / 2)) + 'km/h'
            curTime = cur[3]
            nextTime = next[3]
            cur[3] = str((int(curTime[:-1]) + int(nextTime[:-1]))) + '분'
            print('\t\t\t[removed]-{}'.format(tempP))
            col.remove(col[nextIdx])
            colLen -= 1
        curIdx += 1
        nextIdx += 1
    return col

'''
def refineData(col):
    data = {}
    sectionData = []
    sectionName = []

    for i in range(0, len(col)):
        speed = col[i][2]
        sectionData.append(speed[:-4])
        start = col[i][0]
        end = col[i][1]
        strEnd = start + ' -> ' + end
        sectionName.append(strEnd)

    data['data'] = sectionData
    data['name'] = sectionName
    return data
'''
def refineData(col):
    data = {}
    sectionData = []
    sectionName = []

    for i in range(0, len(col)):
        speed = col[i][2]
        sectionData.append(speed[:-4])
        start = col[i][0]
        end = col[i][1]
        strEnd = start + ' -> ' + end
        sectionName.append(strEnd)

    cur = 0
    next = 1
    sectionLen = len(sectionData)
    while next != (sectionLen - 1):
       if sectionName[cur] == sectionName[next]:
          sectionData.remove( sectionData[next] )
          sectionName.remove( sectionName[next] )
          sectionLen -= 1

       cur += 1
       next += 1

    data['data'] = sectionData
    data['name'] = sectionName
    return data

# parseURL(url_up)
