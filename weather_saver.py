import schedule
import time
import pymysql # 오라클 접속 
import datetime
from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈
import requests


def get_weather(nx,ny,idx):
    try:
        now = datetime.now()
         # 기상청_동네 예보 조회 서비스 api 데이터 url 주소
        vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
        # 실황정보를 조회하기 위해 발표일자, 발표시각, 예보지점 X 좌표, 예보지점 Y 좌표의 조회 조건으로
        # 자료구분코드, 실황값, 발표일자, 발표시각, 예보지점 X 좌표, 예보지점 Y 좌표의 정보를 조회하는 기능

        # 발급 받은 인증키 (Encoding Key) - secret.json 파일에 저장한 key값 읽음

        service_key = "yWSCxNcRGzsAuowY8PlWhxol2Tkxi8eagSaABcf5%2B1gVLEsuZoxrkg3zIh7v%2B4hHgKxs6RtAfOr1UWrwNWHknQ%3D%3D"
        # 지역의 날씨 데이터 이용 (동네 좌표 값: nx, ny)
        # nx = "62" - 용인 기흥 위도 좌표
        # ny = "120" - 용인 기흥 경도 좌표

        # 오늘
        today = datetime.today() # 현재 지역 날짜 반환
        today_date = today.strftime("%Y%m%d") # 오늘의 날짜 (연도/월/일 반환)
        #print('오늘의 날짜는', today_date)
        #print(now.hour)
        # 어제
        yesterday = date.today() - timedelta(days=1)
        yesterday_date=yesterday.strftime('%Y%m%d')
        base_date = today_date
        #print('어제의 날짜는', yesterday_date)

        # 1일 총 8번 데이터가 업데이트 된다.(0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
        # 현재 api를 가져오려는 시점의 이전 시각에 업데이트된 데이터를 base_time, base_date로 설정
        if now.hour<2 or (now.hour==2 and now.minute<=10): # 0시~2시 10분 사이
            base_date=yesterday_date # 구하고자 하는 날짜가 어제의 날짜
            base_time="2300"
        elif now.hour<5 or (now.hour==5 and now.minute<=10): # 2시 11분~5시 10분 사이

            base_time="0200"
        elif now.hour<8 or (now.hour==8 and now.minute<=10): # 5시 11분~8시 10분 사이

            base_time="0500"
        elif now.hour<11 or (now.hour==11 and now.minute<=10): # 8시 11분~11시 10분 사이

            base_time="0800"
        elif now.hour<14 or (now.hour==14 and now.minute<=10): # 11시 11분~14시 10분 사이

            base_time="1100"
        elif now.hour<17 or (now.hour==17 and now.minute<=10): # 14시 11분~17시 10분 사이

            base_time="1400"
        elif now.hour<20 or (now.hour==20 and now.minute<=10): # 17시 11분~20시 10분 사이

            base_time="1700" 
        elif now.hour<23 or (now.hour==23 and now.minute<=10): # 20시 11분~23시 10분 사이

            base_time="2000"
        else: # 23시 11분~23시 59분

            base_time="2300"

        payload = "serviceKey=" + service_key + "&" +\
            "dataType=json" + "&" +\
            "base_date=" + base_date + "&" +\
            "base_time=" + base_time + "&" +\
            "nx=" + str(nx) + "&" +\
            "ny=" + str(ny)
        #print(payload)
        # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 )
        res = requests.get(vilage_weather_url + payload)

        items = res.json().get('response').get('body').get('items')
        #print(items)
        data = dict()
        data['date'] = base_date

        weather_data = dict()
        for item in items['item']:
            # 기온
            if item['category'] == 'TMP':
                weather_data['tmp'] = item['fcstValue']

            if item['category'] == 'SKY':
                weather_data['SKY'] = item['fcstValue']

            # 기상상태
            if item['category'] == 'PTY':
                
                weather_code = item['fcstValue']
                
                if weather_code == '1':
                    weather_state = '비'
                elif weather_code == '2':
                    weather_state = '비/눈'
                elif weather_code == '3':
                    weather_state = '눈'
                elif weather_code == '4':
                    weather_state = '소나기'
                elif weather_code == '0':
                    if weather_data['SKY'] == '3':
                        weather_state='구름 많음'
                    elif weather_data['SKY']=='4':  
                        weather_state='흐림'
                    elif weather_data['SKY']=='1':
                        weather_state='맑음'
                
                weather_data['code'] = weather_code
                weather_data['state'] = weather_state

        data['weather'] = weather_data

        print()
        for i in data:
            print(data[i])
        # ex) {'code': '0', 'state': '없음', 'tmp': '17'} # 17도 / 기상 이상 없음

        state=data['weather']['state']

        print(data['date'][0:4],'년', data['date'][4:6], '월', data['date'][6:8],'일', base_time, '시의 날씨 데이터입니다.')

        print("기온은", weather_data['tmp'], "도 입니다.")

        if state=='비':
            print('비가 와요. 우산을 꼭 챙겨주세요!')
        elif state=='비/눈':
            print('비 또는 눈이 와요. 쌀쌀하니 따뜻하게 입어요! 우산도 꼭 챙겨주세요!')
        elif state=='눈':
            print('눈이 와요. 장갑을 꼭 챙기세요!')
        elif state=='소나기':
            print('소나기가 와요. 비가 언제 올지 모르니, 우산을 꼭 챙겨주세요!')
        elif state=='흐림':
            print('날씨가 흐려요')
        elif state=='구름 많음':
            print('구름이 많아요')
        elif state=='맑음':
            print('날씨가 맑아요 :)')
            
        wheather_state = state 
        wheather_temp = weather_data['tmp']

        connection = pymysql.connect(host='152.67.209.139' , user='emsuser', password='1111', db='ems')    
    # 커서 생성
        cursor = connection.cursor()
        sql_query = "UPDATE weather_info SET SITE_WEATHER ='" + wheather_state
        sql_query = sql_query + "' ,SITE_TEMPERATURE = "+ wheather_temp
        sql_query = sql_query + " ,update_time = '"+ data['date'][0:4] + "-"+data['date'][4:6]+"-"+data['date'][6:8]+" "+base_time[0:2]+":00'"
        sql_query = sql_query +  " where IDX="+ str(idx) 
        #ytab 테이블 생성
        print(sql_query)
        cursor.execute(sql_query)
    # 변경사항 commit
        connection.commit()
    # 커서, connection 종료 
        cursor.close()
        connection.close()
        print("db save compelete     " + str(nx)+":"+str(ny)+":"+str(idx))
    
    except OSError as e:
        print (e)


#  nx="56" ny="125" 금악리
# get_weather(56,125,164010)
# get_weather(55,76,2)
# 남정수상
# 전남 장성군 삼서면 금산리 산 68-13
# x = 55 y = 76

schedule.every(10).seconds.do(get_weather,nx=56,ny=125,idx=164010)
# schedule.every(1).hours.do(get_weather,nx=55,ny=76,idx=2) 
while True:
    schedule.run_pending()
    time.sleep(1)
        