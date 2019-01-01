import torch
import torch.nn as nn
from torch.autograd import Variable

class LSTMproto(nn.Module):
	def __init__(self, input_size, hidden_size, output_size, batch_size, num_layer):
		super(LSTMproto, self).__init__()
		self.input_size = input_size
		self.hidden_size = hidden_size
		self.output_size = output_size
		self.batch_size = batch_size
		self.num_layer = num_layer

		if torch.cuda.is_available():
			self.lstm_layer = nn.LSTM(self.input_size, self.hidden_size, self.num_layer).cuda()
			self.fc_layer = nn.Linear(self.hidden_size, self.output_size).cuda()
		else:
			self.lstm_layer = nn.LSTM(self.input_size, self.hidden_size, self.num_layer)
			self.fc_layer = nn.Linear(self.hidden_size, self.output_size)


	def forward(self, inp, hidden, cell):
		#print(inp.size())
		lstm_output, (hidden, cell) = self.lstm_layer(inp, (hidden, cell))
		lstm_output = lstm_output.squeeze(1)
		fc_output = self.fc_layer(lstm_output[-1].unsqueeze(0))
		return fc_output, hidden, cell

	def init_hidden(self):
		hidden = Variable(torch.zeros(self.num_layer, self.batch_size, self.hidden_size))
		return hidden

#정체정보나 시간 등 짬봉해서 1차원으로 바꾼 후 해볼 생각
class LSTMproto2(nn.Module):
	def __init__(self, input_size, hidden_size, output_size, batch_size, num_layer):
		super(LSTMproto2, self).__init__()
		self.input_size = input_size + 8#date 추가
		self.hidden_size = hidden_size
		self.output_size = output_size
		self.batch_size = batch_size
		self.num_layer = num_layer

		if torch.cuda.is_available():
			self.lstm_layer = nn.LSTM(self.input_size, self.hidden_size, self.num_layer).cuda()
			self.fc_layer = nn.Linear(self.hidden_size, self.output_size).cuda()
			self.date_embedding = nn.Linear(6*6*self.batch_size, 8*6*self.batch_size).cuda()
		else:
			self.lstm_layer = nn.LSTM(self.input_size, self.hidden_size, self.num_layer)
			self.fc_layer = nn.Linear(self.hidden_size, self.output_size)
			self.date_embedding = nn.Linear(6*6*self.batch_size, 8*6*self.batch_size)#6*시간(6 or 24(batch 고려))

	def forward(self, inp, hidden, cell, d_inp):
		#print(inp.size())
		date_info = self.date_embedding(d_inp).reshape(6, self.batch_size, 8)
		inp = torch.cat((inp, date_info), dim=2)#합치기
		lstm_output, (hidden, cell) = self.lstm_layer(inp, (hidden, cell))
		#lstm_output = lstm_output.squeeze(1)#흠...?
		fc_output = self.fc_layer(lstm_output[-1].unsqueeze(0))
		return fc_output, hidden, cell

	def init_hidden(self):
		hidden = Variable(torch.zeros(self.num_layer, self.batch_size, self.hidden_size))
		return hidden	

#5일간 공휴일 유무, 시간, 분, 
class Regressor(nn.Module):
	def __init__(self):
		super(Regressor, self).__init__()

	def forward(self):
		pass