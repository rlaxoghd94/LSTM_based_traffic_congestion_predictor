import pandas as pd
import torch
import os
import random
#0600, 0150, 1000, 1200 - 양양, 서해안, 외곽, 경인
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
distance_dict = {'so_E': torch.tensor(so_E, dtype=torch.float32),
		'so_S': torch.tensor(so_S, dtype=torch.float32),
		'sy_E': torch.tensor(sy_E, dtype=torch.float32),
		'sy_S': torch.tensor(sy_S, dtype=torch.float32),
		'yd_E': torch.tensor(yd_E, dtype=torch.float32),
		'yd_S': torch.tensor(yd_S, dtype=torch.float32),
		'ki_E': torch.tensor(ki_E, dtype=torch.float32),
		'ki_S': torch.tensor(ki_S, dtype=torch.float32),
		'ws_E': torch.tensor(ws_E, dtype=torch.float32),
		'ws_S': torch.tensor(ws_S, dtype=torch.float32)}
target = distance_dict['ws_E']
def read_data(path):
	data = pd.read_csv(path)
	torch_data = torch.tensor(data.values, dtype=torch.float32)
	result = torch_data

	return result

#으으으ㅇ,...
def read_date():
	date_data = pd.read_csv('./data/date.csv', header=None)
	#print(type(date_data), type(date_data.values))
	torch_data = torch.tensor(date_data.values, dtype=torch.float32)
	return torch_data

def read_all(road_code:str=None, road_dir:str=None):
	if road_code: dirname = "./data/"+road_code+'/'+road_dir+'/'
	else: dirname = "./data/"
	file_list = os.listdir(dirname)
	main_tensor = read_data(dirname+file_list.pop(0))#first file
	for each_file in file_list:
		each_tensor = read_data(dirname+each_file)
		main_tensor = torch.cat([main_tensor, each_tensor], dim=1)

	return main_tensor

def batch_generator(full_data, input_size, seq_len, batch_size):
	total_size = input_size * batch_size
	#chunk_size = input_size * seq_len
	col_chunk = seq_len*batch_size
	col_num = full_data.size()[1]

	if True:
		div = int(col_num / (seq_len))
		for i in range(0, div):
			start = int(i*seq_len)
			end = int((i+1)*seq_len)

			if end + 1 > col_num:
				raise StopIteration
			train_batch = full_data[0:input_size, start:end].transpose(0,1).unsqueeze(1)
			train_label = full_data[0:input_size, end:end+1].transpose(0,1)

			train_batch = torch.div(60*target, train_batch)
			train_label = torch.div(60*target, train_label)
			yield train_batch, train_label
		'''
		#38*24개 데이터 추출, label 38*4
		div = int(col_num / (seq_len*batch_size))
		for i in range(0, div):
			start = int(i*seq_len*batch_size)#e.g., 0, 24, 48
			end = int((i+1)*seq_len*batch_size)#e.g., 24, 48, ..
			
			if end + 1 > col_num:
				#임시 : 마지막 데이터 사용하지 않음
				raise StopIteration
			train_batch = full_data[0:input_size,start:end].reshape(seq_len, batch_size, input_size)
			#print(train_batch.size())
			train_label = full_data[0:input_size,start+seq_len:start+col_chunk+1:seq_len].reshape(batch_size, input_size)
			#print(train_label.size())
			yield train_batch, train_label'''
	'''
	#full data : tensor 1*n
	#batch size는 짝수로 6:2(144 : 24)
	t_size = input_size*batch_size
	col_num = full_data.size()[1]
	#mod = col_num % t_size
	if True:
		div = int((col_num - input_size) / (batch_size))# e.g., 24 --> 24000 / 12
		for i in range(0, div):
			start = int(i*(batch_size))#정확히는 batch_size가 아니라 label size 만큼 : 현재 - 6*24 : 24
			end = int(i*(batch_size) + t_size)
			if end + int(batch_size) >= col_num:
				raise StopIteration#stop generator
			train_batch = full_data[0][start:end].reshape(batch_size, input_size).unsqueeze(0)#1 * 6 * 24
			train_label = full_data[0][end:end+int(batch_size)].unsqueeze(1)#24 * 1
			yield train_batch, train_label
	'''
def batch_generator2(full_data, input_size, seq_len, batch_size):
	total_size = input_size * batch_size
	#chunk_size = input_size * seq_len
	col_chunk = seq_len*batch_size
	col_num = full_data.size()[1]

	if True:
		'''
		div = int(col_num / (seq_len))
		for i in range(0, div):
			start = int(i*seq_len)
			end = int((i+1)*seq_len)

			if end + 1 > col_num:
				raise StopIteration
			train_batch = full_data[0:input_size, start:end].transpose(0,1).unsqueeze(1)
			train_label = full_data[0:input_size, end:end+1].transpose(0,1)

			train_batch = torch.div(60*way_distance, train_batch)
			train_label = torch.div(60*way_distance, train_label)
			yield train_batch, train_label'''
		#38*24개 데이터 추출, label 38*4
		div = int(col_num / (seq_len*batch_size))
		for i in range(0, div):
			start = int(i*seq_len*batch_size)#e.g., 0, 24, 48
			end = int((i+1)*seq_len*batch_size)#e.g., 24, 48, ..
			
			if end + 1 > col_num:
				#임시 : 마지막 데이터 사용하지 않음
				raise StopIteration
			train_batch = full_data[0:input_size,start:end].transpose(0,1).reshape(seq_len, batch_size, input_size)
			#print(train_batch.size())
			train_label = full_data[0:input_size,start+seq_len:start+col_chunk+1:seq_len].transpose(0,1).reshape(1, batch_size, input_size)
			#print(train_label.size())
			train_batch = torch.div(60*way_distance, train_batch)
			train_label = torch.div(60*way_distance, train_label)
			yield train_batch, train_label

def random_generator(full_data, input_size, seq_len, batch_size):
	total_size = input_size * batch_size
	#chunk_size = input_size * seq_len
	col_chunk = seq_len*batch_size
	col_num = full_data.size()[1]

	if True:
		#38*24개 데이터 추출, label 38*4
		div = int(col_num / (seq_len*batch_size))
		for i in random.sample(range(0, div-1), div-1):
			random_interval = random.randint(0,col_chunk-1)
			start = int(i*seq_len*batch_size) + random_interval#e.g., 0, 24, 48
			end = int((i+1)*seq_len*batch_size) + random_interval#e.g., 24, 48, ..
			
			if end + 1 > col_num:
				#임시 : 마지막 데이터 사용하지 않음
				raise StopIteration
			train_batch = full_data[0:input_size,start:end].transpose(0,1).reshape(seq_len, batch_size, input_size)
			#print(train_batch.size())
			train_label = full_data[0:input_size,start+seq_len:start+col_chunk+1:seq_len].transpose(0,1).reshape(1, batch_size, input_size)
			#print(train_label.size())
			train_batch = torch.div(60*way_distance, train_batch)
			train_label = torch.div(60*way_distance, train_label)
			yield train_batch, train_label, start#start는 time을 뽑아내기 위해

def date_generator(seq_len, batch_size):
	date_data = read_date()
	col_chunk = seq_len*batch_size
	div = int(date_data.size()[1] / col_chunk)

	for i in range(0, div):
		start = int(i*col_chunk)
		end = int((i+1)*col_chunk)
		#print(start, end)

		if end > date_data.size()[1]:
			raise StopIteration
		target = date_data[0:, start:end].reshape(1, -1)
		#target = target.reshape(seq_len, batch_size, -1)
		yield target

def get_date(date_data, seq_len, batch_size, start):
	chunk = seq_len*batch_size
	end = start+chunk
	target = date_data[0:, start:end].reshape(1, -1)
	return target

def holiday_vector(date, hol_list, time_list):
	day = int(date[-2:])
	vec = []
	for i in range(0,5):
		adj_day = str(day+(i-2))
		if len(adj_day) != 2:
			adj_day = '0'+adj_day
		if (date[:-2] + adj_day) in hol_list:
			if i == 0 or i == 4:
				vec.append(1)
			elif i == 1 or i == 3:
				vec.append(3)
			else:
				vec.append(2)
		else:
			vec.append(0)
	all_vec = []
	for i in time_list:
		v = vec[:]
		v.append(i)
		all_vec.append(v)
	return all_vec

if __name__ == '__main__':
	x = read_date()
	print(x.size())
	#read_data('./data/1000/E/traffic_1000_0.csv')
	'''
	data = read_all('1000')
	print(data.size())
	idx = 0
	for i, j in batch_generator(data, 38, 6, 4):
		if idx == 5:
			break
		print(i, j)
		idx += 1'''

	