import requests
import lxml.html as lh
import pandas as pd

url = 'http://www.roadplus.co.kr/trafficState.do?mCode=A050010&op=highwayItem&bound=S&roadIdS=H1002&roadIdE=H1001&roadName=%EC%84%9C%EC%9A%B8%EC%99%B8%EA%B3%BD%EC%88%9C%ED%99%98%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C' #서울외곽순환도로

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
#print('\t[{}] {} - {}'.format(j, td_data.text_content(), type(td_data)))
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
del col[0]		# MUST del first and last element
del col[-1]		# it contains empty elements

k = 0
for row in col:
	print('[{}] row'.format(k))
	for elem in row:
		print('\t[+] - {}'.format(elem))
	k += 1
