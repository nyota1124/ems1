


import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta 
from ast import Constant, Num, Str
import time
from traceback import print_tb
from warnings import catch_warnings
import requests # HTTP 요청을 보내는 모듈
import json # json 파일 파싱하여 데이터 읽는 모듈
# 현재 날짜 외의 날짜 구하기 위한 모듈
import boto3
import os # 파일이 있는지 확인하는거 
import shutil # 파일 복사 모듈
import schedule

import pymysql # 오라클 접속 
import platform





# 본인이 접속할 오라클 클라우드 DB 사용자이름, 비밀번호, dsn을 넣어준다.

os_name =  platform.system()
second_save = 0
minute_save = 0 
bucket_name ='ef-ems-01'
wheather_temp = 0.0 
wheather_state =''
if (os_name == 'Windows'):
   
    
    if (os.path.isdir('/ems-164001-geumak/') == False ) :
        os.mkdir('/ems-164010-jiyeong/01_realtime')
# elif(os_name == 'Linux'):
#     cx_Oracle.init_oracle_client(lib_dir="/home/ubuntu/opt/oracle/instantclient_21_6/") 
#     if (os.path.isdir('/home/ubuntu/ems-164001-geumak/') == False ) :
#         os.mkdir('/home/ubuntu/ems-164001-geumak/')
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
        print(payload)
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

def get_most_recent_s3_object(bucket_name, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator( "list_objects_v2" )
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    latest = None
    for page in page_iterator:
        if "Contents" in page:
            latest = max(page['Contents'], key=lambda x: x['LastModified'])
            # if latest is None or latest2['LastModified'] > latest['LastModified']:
            #     latest = latest2
    return latest

def prefix_exits(bucket, path):
    s3_client = boto3.client('s3')
    res = s3_client.list_objects_v2(Bucket=bucket, Prefix=path, MaxKeys=1)
    return 'Contents' in res

def savefiletonow():
    try:


        now = datetime.now()
        print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")
 
        today00am = now.replace(hour=00, minute=4, second=0, microsecond=0)
        yesterday = date.today() - timedelta(1)

        if(now<today00am):
            if(os_name == 'Windows'):
                prefix = 'ems-164010-jiyeong/01_Realtime/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'
                prefix2 = '/ems-164010-jiyeong/01_Realtime/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(yesterday.strftime('%d'))+'/'    
            elif(os_name=='Linux'):
                prefix = 'ems-164010-jiyeong/01_Realtime/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'
                prefix2 = '/home/ubuntu/ems-164010-jiyeong/01_Realtime/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'
        else :
            if(os_name == 'Windows'):
                prefix = 'ems-164010-jiyeong/01_Realtime/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'
                prefix2 = '/ems-164010-jiyeong/'
            elif(os_name=='Linux'):
                prefix = 'ems-164010-jiyeong/01_Realtime/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'
                prefix2 = '/home/ubuntu/ems-164010-jiyeong/'
        
        

        if (os.path.isdir(prefix2) == False ) :
             os.mkdir(prefix2)
        s3_resource = boto3.resource('s3')    
        bucket = s3_resource.Bucket(name='ef-ems-01')
        
        latest = get_most_recent_s3_object(bucket_name, prefix)
        
        obj_file =  latest['Key']
        save_file= 'now-164010.json'
        # print(obj_file)
        prefix2 = prefix2 + save_file
        bucket.download_file(obj_file,prefix2)
        print(obj_file + "파일이 저장되었습니다.")
        
        # targettime = obj_file[-11:-5]
        # obj_file = ''

        # # if (targettime[2:4] == '00') :
        # #     save_time = Str(int(targettime[:2])-1) + '59'
        # # else : 
        # #     save_time = targettime[:2]+ Str(int(targettime[:2])-1)
        json_data=dict()

        with open(prefix2,'r') as site164010:
            json_data=json.load(site164010)
            time_get = json_data['pms'][0]['timeget']
            # print(json_data)
            me_a_power = json_data['meterList'][0]['me_a_power']
            # print(me_a_power)
            me_freq= json_data['meterList'][0]['me_freq']
            me_pf = json_data['meterList'][0]['me_pf']
            me_a_energy = json_data['meterList'][0]['me_a_energy_hi']
            
            pcs_dc_v = json_data['pcsList'][0]['pcs_dc_v']
            pcs_dc_v_link=json_data['pcsList'][0]['pcs_dc_v_link']
            pcs_dc_a=json_data['pcsList'][0]['pcs_dc_a']
            pcs_dc_w=json_data['pcsList'][0]['pcs_dc_w']
            pcs_freq=json_data['pcsList'][0]['pcs_freq']
            pcs_pf=json_data['pcsList'][0]['pcs_pf']
            pcs_a_p_power=json_data['pcsList'][0]['pcs_a_p_power']
            pcs_inter_temp_1=json_data['pcsList'][0]['pcs_inter_temp_1']
            
            bat_b_heart_beat=json_data['bbmsList'][0]['bat_b_heart_beat']
            bat_b_soc=json_data['bbmsList'][0]['bat_b_soc']
            bat_b_soh=json_data['bbmsList'][0]['bat_b_soh']
            bat_b_volte=json_data['bbmsList'][0]['bat_b_volte']
            bat_b_current=json_data['bbmsList'][0]['bat_b_current']
            bat_b_ch_pow_limit=json_data['bbmsList'][0]['bat_b_ch_pow_limit']
            bat_b_disch_pow_limit=json_data['bbmsList'][0]['bat_b_disch_pow_limit']
            bat_b_aver_temp=json_data['bbmsList'][0]['bat_b_aver_temp']
            
            imd_iso_v=json_data['imdList'][0]['imd_iso_v']
            imd_test_alarm =json_data['imdList'][0]['imd_test_alarm']
            
            imd_sensor_1 =json_data['tempList'][0]['imd_sensor_1']
            imd_sensor_2 =json_data['tempList'][0]['imd_sensor_2']



        
#>>> now < today8am
        #


        sql_query = "UPDATE site_info SET "
        sql_query = sql_query + "timeget =  '"+str(time_get)  +"'"
        sql_query = sql_query + ",me_A_POWER =  "+str(me_a_power)
        sql_query = sql_query + ",me_freq =  "+str(me_freq)
        sql_query = sql_query + ",me_pf =  "+str(me_pf)
        sql_query = sql_query + ",me_a_energy_hi =  '"+str(me_a_energy)+"'"
        sql_query = sql_query + ",pcs_dc_v =  "+str(pcs_dc_v)
        sql_query = sql_query + ",pcs_dc_v_link=  "+str(pcs_dc_v_link)
        sql_query = sql_query + ",pcs_dc_a =  "+str(pcs_dc_a)
        sql_query = sql_query + ",pcs_dc_w =  "+str(pcs_dc_w)
        sql_query = sql_query + ",pcs_freq =  "+str(pcs_freq)
        sql_query = sql_query + ",pcs_pf =  "+str(pcs_pf)
        sql_query = sql_query + ",pcs_a_p_power =  "+str(pcs_a_p_power)
        sql_query = sql_query + ",pcs_inter_temp_1 =  "+str(pcs_inter_temp_1)
        sql_query = sql_query + ",bat_b_heart_beat =  "+str(bat_b_heart_beat)
        sql_query = sql_query + ",bat_b_soc =  "+str(bat_b_soc)
        sql_query = sql_query + ",bat_b_soh =  "+str(bat_b_soh)
        sql_query = sql_query + ",bat_b_volte =  "+str(bat_b_volte)
        sql_query = sql_query + ",bat_b_current =  "+str(bat_b_current)
        sql_query = sql_query + ",bat_b_ch_pow_limit =  "+str(bat_b_ch_pow_limit)
        sql_query = sql_query + ",bat_b_disch_pow_limit =  "+str(bat_b_disch_pow_limit)
        sql_query = sql_query + ",bat_b_aver_temp =  "+str(bat_b_aver_temp)
        sql_query = sql_query + ",imd_iso_v =  "+str(imd_iso_v)
        sql_query = sql_query + ",imd_test_alarm =  "+str(imd_test_alarm)
        sql_query = sql_query + ",temp_imd_sensor_1 =  "+str(imd_sensor_1)
        sql_query = sql_query + ",temp_imd_sensor_2 =  "+str(imd_sensor_2)
        sql_query = sql_query +  " where idx=164010"
        print(sql_query)
    # # 본인이 Instant Client 넣어놓은 경로를 입력해준다
        connection = pymysql.connect(host='152.67.209.139' , user='emsuser', password='1111', db='ems', charset='utf8mb4')    
        # 커서 생성
        cursor = connection.cursor()

    #     # pytab 테이블 생성

        cursor.execute(sql_query)
        

    # # 변경사항 commit
        connection.commit()

    # # 커서, connection 종료 
        cursor.close()
        connection.close()
        print("DB 저장 성공")
  
    except OSError as e:
        print(e)



schedule.every(10).minutes.do(get_weather,nx=56,ny=125,idx=164010)
schedule.every(5).seconds.do(savefiletonow)

 
while True:
    schedule.run_pending()
    time.sleep(1)