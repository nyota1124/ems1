from ast import Constant, Num, Str
from opcode import opname
from traceback import print_tb
from warnings import catch_warnings
import requests # HTTP 요청을 보내는 모듈
import json # json 파일 파싱하여 데이터 읽는 모듈
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈
import boto3
import os # 파일이 있는지 확인하는거 
import shutil # 파일 복사 모듈
import schedule
import time
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
        os.mkdir('/ems-164001-geumak/')
# elif(os_name == 'Linux'):
#     cx_Oracle.init_oracle_client(lib_dir="/home/ubuntu/opt/oracle/instantclient_21_6/") 
#     if (os.path.isdir('/home/ubuntu/ems-164001-geumak/') == False ) :
#         os.mkdir('/home/ubuntu/ems-164001-geumak/')


def get_most_recent_s3_object(bucket_name, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator( "list_objects_v2" )
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    latest = None
    for page in page_iterator:
        if "Contents" in page:
            latest = max(page['Contents'], key=lambda x: x['LastModified'])
            # if latest is None or latest2['LastModified'] > latest['LastModified']:
        
    return latest

def prefix_exits(bucket, path):
    s3_client = boto3.client('s3')
    res = s3_client.list_objects_v2(Bucket=bucket, Prefix=path, MaxKeys=1)
    return 'Contents' in res

def onejsonsave():
    now = datetime.now()
    if(os_name == 'Windows'):
        prefix2 = '/ems-164001-geumak/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'
    # elif(os_name=='Linux'):
    #     prefix2 = '/home/ubuntu/ems-164001-geumak/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'

    try:
        if (os.path.isfile(prefix2+'one-geumak.json') == False ) :
            s3_resource = boto3.resource('s3')
            bucket = s3_resource.Bucket(name='ef-ems-01')
            obj_file = 'ems-164001-geumak/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))
            obj_file =  obj_file + '/EMS'+now.strftime('%Y%m%d')+'000004.json'
            save_file= 'one-geumak.json'
            #print(obj_file)
            bucket.download_file(obj_file,prefix2+save_file)
            obj_file=''
    except OSError as e : 
        print(e)

def savefiletonow():
    try:


        now = datetime.now()
        print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")

 


        # if(now<today00am):
        #     if(os_name == 'Windows'):
        #         prefix = 'ems-164001-geumak/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'
        #         prefix2 = '/ems-164001-geumak/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'    
        #     elif(os_name=='Linux'):
        #         prefix = 'ems-164001-geumak/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'
        #         prefix2 = '/home/ubuntu/ems-164001-geumak/'+str(now.year)+str(now.strftime('%m'))+str(yesterday.strftime('%d'))+'/'
        # else :
        #     if(os_name == 'Windows'):
        #         prefix = 'ems-164001-geumak/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'
        #         prefix2 = '/ems-164001-geumak/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'    
        #     elif(os_name=='Linux'):
        #         prefix = 'ems-164001-geumak/'+str(now.year)+'/'+str(now.strftime('%m'))+'/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'
        #         prefix2 = '/home/ubuntu/ems-164001-geumak/'+str(now.year)+str(now.strftime('%m'))+str(now.strftime('%d'))+'/'
        
        

        # if (os.path.isdir(prefix2) == False ) :
        #     os.mkdir(prefix2)
        # s3_resource = boto3.resource('s3')    
        # bucket = s3_resource.Bucket(name='ef-ems-01')
        # latest = get_most_recent_s3_object(bucket_name, prefix)
        # #print(latest)
        # obj_file =  latest['Key']
        # save_file= 'now-geumak.json'
        # bucket.download_file(obj_file,prefix2+save_file)
        # print(obj_file + "파일이 로딩되었습니다.")
        
        # targettime = obj_file[-11:-5]
        # obj_file = ''

        # # if (targettime[2:4] == '00') :
        # #     save_time = Str(int(targettime[:2])-1) + '59'
        # # else : 
        # #     save_time = targettime[:2]+ Str(int(targettime[:2])-1)
            
        


        # json_data=dict()

        # s_genkw=0.0
        # tensxt_energy=0
        

        # if minute_save == 0 :
        #     with open(prefix2+'now-geumak.json','r') as geumakjson:
        #         json_data=json.load(geumakjson)
                
                
                
                
        #         time_get = json.dumps(json_data['meterList5:'][0]['timeget'],indent="\t")
        #         s_genkw = round(float(json.dumps(json_data['meterList5:'][0]['me_a_power'],indent="\t")),2)
        #         #print(json.dumps(json_data['meterList5:'][0],indent="\t"))
        #         s_appower = float(json.dumps(json_data['pcsList5:'][0]['pcs_a_p_power'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_a_p_power'],indent="\t"))
        #         s_pcs_vo_r = float(json.dumps(json_data['pcsList5:'][0]['pcs_v_phease_r'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_v_phease_r'],indent="\t"))
        #         s_pcs_vo_s = float(json.dumps(json_data['pcsList5:'][0]['pcs_v_phease_s'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_v_phease_s'],indent="\t"))
        #         s_pcs_vo_t = float(json.dumps(json_data['pcsList5:'][0]['pcs_v_phease_t'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_v_phease_t'],indent="\t"))
        #         s_pcs_am_r = float(json.dumps(json_data['pcsList5:'][0]['pcs_a_phase_r'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_a_phase_r'],indent="\t"))
        #         s_pcs_am_s = float(json.dumps(json_data['pcsList5:'][0]['pcs_a_phase_s'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_a_phase_s'],indent="\t"))
        #         s_pcs_am_t = float(json.dumps(json_data['pcsList5:'][0]['pcs_a_phase_t'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_a_phase_t'],indent="\t"))

        #         s_pcs_vo_r = round((s_pcs_vo_r),2)
        #         s_pcs_vo_s = round((s_pcs_vo_s),2)
        #         s_pcs_vo_t = round((s_pcs_vo_t),2)
        #         s_pcs_am_r = round((s_pcs_am_r),2)
        #         s_pcs_am_s = round((s_pcs_am_s),2)
        #         s_pcs_am_t = round((s_pcs_am_t),2)
                
        #         if(s_appower == 0 ):
        #             s_appower = 0.0

        #         s_soc = round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_soc'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_soc'],indent="\t")))/2,2)
        #         s_iso_v = round((float(json.dumps(json_data['imdList5:'][0]['imd_iso_v'],indent="\t"))+float(json.dumps(json_data['imdList5:'][1]['imd_iso_v'],indent="\t")))/2,2)
        #         pcs_inter_temp = round((float(json.dumps(json_data['pcsList5:'][0]['pcs_inter_temp_1'],indent="\t"))+float(json.dumps(json_data['pcsList5:'][1]['pcs_inter_temp_1'],indent="\t")))/2,2)
        #         s_a_energy = round((float(json.dumps(json_data['meterList5:'][0]['me_a_energy_hi'],indent="\t"))+(float(json.dumps(json_data['meterList5:'][0]['me_a_energy_lo'],indent="\t"))*1000)),2)
        #         s_soh = round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_soh'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_soh'],indent="\t")))/2,2)
        #         bms_volte = round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_volte'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_volte'],indent="\t")))/2,2)
        #         bms_am = round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_current'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_current'],indent="\t")))/2,2)
        #         bms_temp = round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_aver_ambient_temp'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_aver_ambient_temp'],indent="\t")))/2,2)
        #         cell_volte_max=round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_max_r_vol'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_max_r_vol'],indent="\t")))/2,2)
        #         cell_volte_min=round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_min_r_v'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_min_r_v'],indent="\t")))/2,2)
        #         cell_temp_max=round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_max_amb_t'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_max_amb_t'],indent="\t")))/2,2)
        #         cell_temp_min=round((float(json.dumps(json_data['bbmsList5:'][0]['bat_b_min_amb_t'],indent="\t"))+float(json.dumps(json_data['bbmsList5:'][1]['bat_b_min_amb_t'],indent="\t")))/2,2)
        #         btr_now_temp=round(float(json.dumps(json_data['tempList5:'][0]['imd_sensor_1'],indent="\t")),2)
        #         btr_setting_temp=round((float(json.dumps(json_data['airList5:'][0]['air_desired_temp'],indent="\t"))+float(json.dumps(json_data['airList5:'][1]['air_desired_temp'],indent="\t")))/2,2)
        #         btr_now_wp =round(float(json.dumps(json_data['tempList5:'][0]['imd_sensor_2'],indent="\t")),2)


                #print(json.dumps(json_data['pcsList5:'][0]['pcs_a_p_power'],indent="\t"))
                #print(json.dumps(json_data['pcsList5:'][1]['pcs_a_p_power'],indent="\t"))

                #print(json.dumps(json_data['pcsList5:'][0],indent="\t"))
                #print(json.dumps(json_data['bbmsList5:'][0],indent="\t"))
                
                #print(json.dumps(json_data['imdList5:'][0],indent="\t"))
                #print(json.dumps(json_data['tempList5:'][0],indent="\t"))
                
                #print(json.dumps(json_data['switchList5:'][0],indent="\t"))
                #print(json.dumps(json_data['airList5:'][0],indent="\t"))


            

        
#>>> now < today8am
        #


    #     sql_query = "UPDATE SITE_LIVE SET "
    #     sql_query = sql_query + "timeget =  '"+str(time_get)  +"'"
    #     sql_query = sql_query + ",SITE_GEN_A_POWER =  "+str(s_genkw)  
    #     sql_query = sql_query + ",SITE_APPOWER="+str(s_appower)
    #     sql_query = sql_query + ",SITE_SOC="+str(s_soc)
    #     sql_query = sql_query + ",SITE_N_ENERGY="+str(oton_energy)
    #     sql_query = sql_query + ",SITE_SXTTEN_ENERGY="+str(tensxt_energy)
    #     sql_query = sql_query + ",PCS_VO_R="+str(s_pcs_vo_r)
    #     sql_query = sql_query + ",PCS_VO_S="+str(s_pcs_vo_s)
    #     sql_query = sql_query + ",PCS_VO_T="+str(s_pcs_vo_t)
    #     sql_query = sql_query + ",PCS_AM_R="+str(s_pcs_am_r)
    #     sql_query = sql_query + ",PCS_AM_S="+str(s_pcs_am_s)
    #     sql_query = sql_query + ",PCS_AM_T="+str(s_pcs_am_t)
    #     sql_query = sql_query + ",IMD_ISO_V="+str(s_iso_v)
    #     sql_query = sql_query + ",PCS_INTER_TEMP="+str(pcs_inter_temp)
    #     sql_query = sql_query + ",SITE_SOH="+str(s_soh)
    #     sql_query = sql_query + ",BMS_VOLTE="+str(bms_volte)
    #     sql_query = sql_query + ",BMS_AM="+str(bms_am)
    #     sql_query = sql_query + ",BMS_TEMP="+str(bms_temp)
    #     sql_query = sql_query + ",BMS_CELL_V_MAX="+str(cell_volte_max)
    #     sql_query = sql_query + ",BMS_CELL_MIN="+str(cell_volte_min)
    #     sql_query = sql_query + ",BMS_CELL_TEMP_MAX="+str(cell_temp_max)
    #     sql_query = sql_query + ",BMS_CELL_TEMP_MIN="+str(cell_temp_min)
    #     sql_query = sql_query + ",BTR_NOW_TEMP="+str(btr_now_temp)
    #     sql_query = sql_query + ",BTR_SET_TEMP="+str(btr_setting_temp)
    #     sql_query = sql_query + ",BTR_NOW_WP="+str(btr_now_wp)
    #     sql_query = sql_query +  " where IDX=1"
       
    # # 본인이 Instant Client 넣어놓은 경로를 입력해준다
    #     connection = pymysql.connect(host='3.39.130.51' , user='root', password='z1x2c3v4%', db='efems', charset='utf8mb4')    
    #     # 커서 생성
    #     cursor = connection.cursor()

    #     # pytab 테이블 생성

    #     cursor.execute(sql_query)
        

    # # 변경사항 commit
    #     connection.commit()

    # # 커서, connection 종료 
    #     cursor.close()
    #     connection.close()
    #     print("DB 저장 성공")
  
    except OSError as e:
        print(e)




schedule.every(15).seconds.do(savefiletonow)

 
while True:
    schedule.run_pending()
    time.sleep(1)