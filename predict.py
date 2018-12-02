import torch
import datetime
from data_processor import *
import copy
#return 형식 {'road': '1000?', "E": [3시간 데이터], "S": [3시간 데이터]}
so_E = [4.47, 1.05, 4.07, 5.06, 4.85, 2.45, 2.64, 1.77, 0.79, 1.21, 1.83,
2.87, 1.97, 7.87, 8.28, 6.68, 2.76, 7.23, 2.5, 1.83, 3.21, 0.74, 3.21, 2.92, 1.55,
1.85, 2.73, 2.78, 3.95, 1.14, 1.46, 5.35, 3.88, 5.9, 3.03, 3.21, 2.76, 6.16]
so_S = [6.96, 1.63, 4.35, 2.35, 5.8, 3.73, 5.37, 2.36, 0.41, 4.66, 2.07, 3.45,
0.9, 1.89, 2.94, 3.12, 0.66, 3.11, 2.16, 3.01, 6.51, 3.47, 6.19, 8.13, 7.3, 2.68, 2.73,
2.39, 1.21, 0.8, 1.02, 2.59, 2.55, 4.91, 4.54, 5.08, 0.59, 4.12]
sy_E = [0.99, 0.54, 2.2, 3.42, 7.3, 5.42, 12.78, 14.24, 9.09, 1.38, 3.93, 0.54, 16.33]
sy_S = [15.6, 1.26, 3.93, 0.59, 8.93, 14.48, 12.77, 5.33, 8.1, 2.62, 2.2, 1.34, 0.97]
ki_E = [3.9, 2.57, 3.7, 3.84, 2.54, 0.37, 1.92, 9.95]
ki_S = [9.45, 1.63, 1.17, 2.12, 3.76, 4.2, 2.57, 3.89]
yd_E = [4.85, 3.03, 2.7, 1.77, 3.18, 2.13, 5.6, 0.91, 2.05, 1.58, 2.91,
	5.87, 5.78, 4.14, 5.69, 8.02, 7.07, 5.37, 6.91, 8.01, 6.57, 19.89, 9.07, 4.9,
	1.87, 12.68, 17.45, 16.84, 5.74, 5.74, 9.47, 6.07, 13.21, 22.56]
yd_S = [21.85, 12.91, 6.58, 9.69, 5.73, 16.6, 17.15, 13, 2.32, 3.91, 9.49, 19.98, 5.34,
9.21, 6.27, 6.14, 6.83, 8.14, 2.23, 9.14, 4.2, 6.0, 2.81, 2.22, 1.54, 1.42, 4.79, 2.11, 3.27, 2.5, 2.69, 1.01, 6.87]
ws_E = [1.35, 1.04, 16.22, 2.31, 7.97, 24.33, 15.97, 2.82, 8.54, 9.33, 16.13, 14.01, 12.53,
8.06, 6.1, 9.4, 11.85, 8.71, 11.89, 19.63, 11.1, 13.59, 10.74, 6.31, 9.57, 8.16,
12.61, 6.34, 7.95, 13.43, 4.36, 3.4, 5.25, 1.92, 1.1, 3.22, 1.22, 2.4, 4.79]
ws_S = [3.76, 2.95, 1.24, 2.88, 1.89, 0.97, 6.23, 2.83, 4.17, 13.38, 7.59, 6.89, 12.65, 7.95, 9.1, 6.97, 10.68,
13.71, 10.81, 19.72, 11.9, 8.88, 11.8, 8.82, 6.44, 8.36, 12.59, 13.91, 16.19, 10.48, 7.31, 2.71, 16.07, 24.37, 7.44,
3.03, 16.64, 0.52, 1.87]
distance_dict = {'1000E': torch.tensor(so_E, dtype=torch.float32),
		'1000S': torch.tensor(so_S, dtype=torch.float32),
		'0600E': torch.tensor(sy_E, dtype=torch.float32),
		'0600S': torch.tensor(sy_S, dtype=torch.float32),
		'yd_E': torch.tensor(yd_E, dtype=torch.float32),
		'yd_S': torch.tensor(yd_S, dtype=torch.float32),
		'1200E': torch.tensor(ki_E, dtype=torch.float32),
		'1200S': torch.tensor(ki_S, dtype=torch.float32),
		'0150E': torch.tensor(ws_E, dtype=torch.float32),
		'0150S': torch.tensor(ws_S, dtype=torch.float32)}

file_list = ["lstm_1000_E.pt", "lstm_1000_S.pt", "lstm_0600_E.pt", "lstm_0600_S.pt",
"lstm_1200_E.pt", "lstm_1200_S.pt", "lstm_0150_E.pt", "lstm_0150_S.pt"]

#lstm = torch.load("lstm_0150_S.pt", map_location='cpu')

test_dict = {'road': '1000', 'direction': 'S', 'data':[100.35, 100.04, 16.22, 2.31, 7.97, 24.33, 15.97, 2.82, 8.54, 9.33, 16.13, 14.01, 12.53,
8.06, 6.1, 9.4, 11.85, 8.71, 11.89, 19.63, 11.1, 13.59, 10.74, 6.31, 9.57, 8.16,
12.61, 6.34, 7.95, 13.43, 4.36, 3.4, 5.25, 1.92, 1.1, 3.22, 1.22, 2.4]}
#input에 이어붙여서 추가 예측 ! --> 시간값도 바꿔서 넣기
def predictor(lstm, inp, d_inp, first_val, n_times=3):
	#lstm = torch.load("lstm_1000_E.pt", map_location='cpu')
	hidden = lstm.init_hidden()
	cell = lstm.init_hidden()
	#print(inp)
	mod_d_inp = d_inp.reshape(24, 6)
	#first_val = inp.reshape(24, -1)[-1][:]
	#print(inp.size())
	#print(first_val)
	#print(mod_d_inp.size())
	last_time_vec = copy.deepcopy(mod_d_inp[-1,:])#tensor's last vector deep copy
	last_hour = last_time_vec[-1]
	#print(torch.cat((last_time_vec[:-1], torch.tensor(last_hour+1, dtype=torch.float32).view(1))))
	all_output = []
	#
	mod_inp = inp.reshape(24, -1)
	for i in range(0, n_times):
		output, hidden, cell = lstm(inp, hidden, cell, d_inp)
		#print(output.size())
		#print(output[0][-1])#1*n
		last_hour += 1
		last_time_vec = torch.cat((last_time_vec[:-1], torch.tensor(last_hour, dtype=torch.float32).view(1)))
		mod_inp = torch.cat((mod_inp, output[0][-1].reshape(1,-1)), dim=0)
		#print(last_time_vec)
		#print(mod_d_inp)
		mod_d_inp = torch.cat((mod_d_inp, last_time_vec.reshape(1,-1)))
		#print(mod_d_inp)
		#print(mod_inp[i+1:].size())
		inp = mod_inp[i+1:].reshape(6,4,-1)#seq_len, batch, -1
		d_inp = mod_d_inp[i+1:].reshape(1,-1)
		all_output.append(output[0][-1])
	
	return_list = []
	return_list.append(list(first_val.detach().numpy()))
	for m in all_output:
		new_element = list(m.detach().numpy())
		return_list.append(new_element)
	#print(return_list)
	return_list = list(map(list, zip(*return_list)))
	return return_list
	#print(list(all_output[0].detach().numpy()))


def get_timenow(hol_date):
	#현재 기준 24시간 전까지
	_now = datetime.datetime.now()
	_now_str = _now.strftime("%Y.%m.%d %H")
	_now_date = _now_str[:-3]
	_now_time = int(_now_str[-2:])
	yesterday = (_now - datetime.timedelta(days=1)).strftime("%Y.%m.%d %H")
	yesterday_date = yesterday[:-3]
	yesterday_time = int(yesterday[-2:])

	now_tl = range(0, _now_time+1)
	yes_tl = range(yesterday_time+1, 24)
	#hv = yes_tl + now_tl
	prev_hol_vec = holiday_vector(yesterday_date, hol_date, yes_tl)
	hol_vec = holiday_vector(_now_date, hol_date, now_tl)
	#hol_vec.append(_now_time)
	return_vec = torch.tensor(prev_hol_vec+hol_vec, dtype=torch.float32)
	#print(return_vec[-1][-1])
	print(return_vec.size())
	return return_vec.reshape(1,-1)

def pre_processor(target_dict):
	with open("./holiday_date.txt", 'r') as f:
		hol_date = f.read()
		hol_date = hol_date.split('\n')
	road = target_dict['road']
	direction = target_dict['direction']
	data = target_dict['data']
	for i, m in enumerate(data):
		data[i] = float(m)
	data = torch.tensor(data, dtype=torch.float32).reshape(-1, 1)

	file_path = './data/'+road+'/'+direction+'/'+'past_data.csv'
	lstm = torch.load("lstm_"+road+"_"+direction+".pt", map_location='cpu')
	past_data = read_data(file_path)
	use_data = past_data[0:,17:40]#16시 기준
	use_data = torch.cat((use_data, data), dim=1).transpose(0,1)#.reshape(6, 4, -1)

	#print('tq', use_data.size())
	time_data = distance_dict[road+direction]
	#print(time_data.size())
	use_data = torch.div(60*time_data, use_data)
	#print()
	first_val = use_data[-1][:]
	use_data = use_data.transpose(0,1).reshape(6,4,-1)
	
	#use_data = torch.cat((use_data, data), dim=0).reshape(6, 4, -1)
	#print(use_data.size())
	d_inp = get_timenow(hol_date)
	dict_template = target_dict#{"road":road, "direction":direction}
	return lstm, use_data, d_inp, dict_template, first_val

def change_format(result):
	for i,item in enumerate(result):
		for ii, m in enumerate(item):
			temp = round(m, 1)
			item[ii] = str(temp)
		result[i] = item
	return result

def main(target_dict):
	lstm, use_data, d_inp, result_dict, first_val = pre_processor(target_dict)
	result = predictor(lstm, use_data, d_inp, first_val)
	#print(result)
	result = change_format(result)
	result_dict['data'] = result
	return result_dict

if __name__ == '__main__':
	#lstm, use_data, d_inp = pre_processor(test_dict)
	x = main(test_dict)
	print(x)
	#print(use_data)
	#print(d_inp)
	'''
	with open("./holiday_date.txt", 'r') as f:
		hol_date = f.read()
		hol_date = hol_date.split('\n')
	test_data = read_data('./data/0150/test_data_S.csv')
	#get_timenow()
	test_time = "2018.11.20"#2018.09.28
	tt2 = "2018.11.19"#2018.09.29
	tl_list2 = range(17, 24)
	tl_list1 = range(0,17)
	prev_h = holiday_vector(tt2, hol_date, tl_list2)
	now_h = holiday_vector(test_time, hol_date, tl_list1)
	prev_h.extend(now_h)
	hv = torch.tensor(prev_h, dtype=torch.float32).reshape(1, -1)
	#hv = get_timenow(hol_date)
	#print(hv)
	inp = test_data[0:,1193:1217]
	#print(inp)
	inp = torch.tensor(inp).transpose(0,1).reshape(6,4,-1)
	r_inp = torch.div(60*distance_dict['ws_S'], inp)
	predictor(r_inp, hv)'''
