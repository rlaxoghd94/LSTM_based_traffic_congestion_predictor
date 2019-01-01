# Traffic Congestion Prediction Semantic Web
## Konkuk University 2018 Fall Web Tech. Project
### Team Members: 김태홍, 서지원

### Project Purpose
Foretell the amount of time it takes to pass between sections within highways in South Korea by building a LSTM-based semantic web application.

### Handling Criteria
1. Flask (Python 3.x, JavaScript, HTML, CSS)
2. PyTorch (LSTM Neural Network)

### Priorities
1. Flask
 - [x] Flask 프로젝트 셋업
 - [x] yahoo! weather api 획득
 - [x] yahoo! weather client 활성화
 - [x] 현재 위도 경도 불러와서 'city code' 갱신
 - [x] chart.js 셋업
 - [x] PyTorch로 부터 받은 데이터로 chart.js 데이터 동적 관리
 - [x] Weather API를 openweathermap에서 yahoo! weather API로 변경
 - [x] HTML CSS JS 갈아 엎기

2. PyTorch
 - [x] 4개의 batch로 LSTM 구성
 - [x] 현 시각 기준 6시간 데이터를 활용해 현 시각 기준 +/- 2시간 데이터 추출

