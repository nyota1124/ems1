import platform
from time import sleep
import json
import time
import pandas as pd
import numpy as np
import requests
import streamlit as st
import pymysql
import os 
import streamlit as st
import base64

from PIL import Image
from streamlit_autorefresh import st_autorefresh
from st_on_hover_tabs import on_hover_tabs
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_echarts import st_echarts
from streamlit_extras.add_vertical_space import add_vertical_space

from streamlit_echarts import st_pyecharts
import pyecharts.options as opts
from pyecharts.charts import Gauge,Liquid
from streamlit_elements import elements, mui, html
st.set_page_config(layout="wide")


cities = [[37.566687, 126.978417,"서울",0],
          [35.179774, 129.075004,"부산",1],
          [37.455900, 126.705522,"인천",2],
          [35.871380, 128.601743,"대구",3],
          [36.350451, 127.384827,"대전",4],
          [35.160072, 126.851440,"광주",5]]

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
def load_data(idx:int):
    
    connection = pymysql.connect(host='152.67.209.139' , user='emsuser', password='1111', db='ems', charset='utf8mb4')
    cursor = connection.cursor()
    
    sql_query = "SELECT * from site_info where idx = "+str(idx)
    cursor.execute(sql_query)
    result = cursor.fetchall()
    
    sql_query = "SELECT * from weather_info where idx = "+str(idx)
    cursor.execute(sql_query)
    result_weather = cursor.fetchall()
    
    
    sql_query = "SELECT * from site_genday where site_idx = "+str(idx)+" AND day = DATE_FORMAT(now(), '%Y-%m-%d')"
    cursor.execute(sql_query)
    result_genday = cursor.fetchall()
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return result,result_weather,result_genday

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)
    
def main():
	style_metric_cards(background_color="black-70")
	os_name =  platform.system()
	os_dir = os.getcwd()

	if os_name == "Linux":
		m=st.markdown('<style>' + open('CSS/style.css').read() + '</style>', unsafe_allow_html=True)
	elif os_name == "Windows":
		m=st.markdown('<style>' + open('./CSS/style.css').read() + '</style>', unsafe_allow_html=True)
	
	hide_default_format = """
		<style>
		#MainMenu {visibility: hidden; }
		footer {visibility: hidden;}
		</style>
		"""
	st.markdown(hide_default_format, unsafe_allow_html=True)
	hide_table_row_index = """
								<style>
								thead tr th:first-child {display:none}
								tbody th {display:none}
								</style>
								"""

					# Inject CSS with Markdown
	st.markdown(hide_table_row_index, unsafe_allow_html=True)
		

	result,result_weather,result_genday = load_data(164010)

	# st.write(result)
	# st.write(result_weather)
	# st.write(result_genday)
	# st.write(type(result)) 
	with st.sidebar:
		f = open("./lotties/sub-logo.svg", 'rt', encoding='UTF8')
		lines = f.readlines()	
		line_string=''.join(lines)

		render_svg(line_string)
		colored_header(
			label=" ",
			description = " ",
			color_name="violet-70",
		)
		tabs = on_hover_tabs(tabName=['Dashboard', 'Graph', 'ALARM','Location'], 
							iconName=['dashboard', 'money', 'alarm','reply'], default_choice=0)
	if tabs == 'Dashboard':
		count = st_autorefresh(interval=10000, key="fizzbuzzcounter")
		if count == 0:
			with st.spinner(text='In progress'):sleep(2 )
			st.balloons()
   
		coli1,coli2,coli3,coli4,coli5,coli6=st.columns([5,1,1,1,1,1])
		with coli1:
			st.title(str(result[0][1])+"  발전소" )
		with coli2:
			st.metric(label= "날씨" , value = result_weather[0][1] )
		with coli3:
			st.metric(label="온도(℃)", value=result_weather[0][2] )
		with coli4:
			st.metric(label="태양광", value=result[0][3] )
		with coli5:
			st.metric(label="PCS", value=result[0][13] )
		with coli6:
			st.metric(label="SOC", value=result[0][16] )
   
		colored_header(
			label=format(tabs),
			description = " ",
			color_name="violet-70",
		)
		with st.container():
			col1,col2,col3= st.columns(3)
			with col1:
				with elements("meter"):
						st.write("계측기 정보")
						gauge_option = {
								"tooltip":{"formatter": "{a} <br/>{b} : {c}"},
								"series": [{"name":"kw/H","type": "gauge","max":800,"pointer":{"icon":"path://M12.8,0.7l12,40.1H0.7L12.8,0.7z","length":"12%","width":20,"offsetCenter":[0,"-60%"],"itmestyle":{"color":"inherit"}},"progress":{"show": "true"},"detail":{"valueAnimation":"false","formmater":"{value}"},"data": [{"value":result[0][3],"name":"발전력"}],}]
							}
	
						df1 = pd.DataFrame(
							(("오늘의 발전량",result_genday[0][3]),("주파수",result[0][4]),("me_pf",result[0][5])),
							columns=("Name","Value"),
						)
						colu1,colu2 =st.columns(2)
						with colu1:
							st_echarts(gauge_option,key ="gauge1")
						with colu2:
							st.table(df1)

	# 			with st.container():
	# 				# gauge_view.empty()
	# 				# with st.spinner('Wait for it...'):
	# 				# 	time.sleep(1)
	# 				gauge_option = {
	# 						"tooltip":{"formatter": "{a} <br/>{b} : {c}"},
	# 						"series": [{"name":"kw/H","type": "gauge","max":800,"pointer":{"icon":"path://M12.8,0.7l12,40.1H0.7L12.8,0.7z","length":"12%","width":20,"offsetCenter":[0,"-60%"],"itmestyle":{"color":"inherit"}},"progress":{"show": "true"},"detail":{"valueAnimation":"false","formmater":"{value}"},"data": [{"value":result[0][3],"name":"발전력"}],}]
	# 					}
	# 				st_echarts(gauge_option)
	# 				# with open(weather_lottie_setfn(result_weather[0][1]), 'r') as file:lottie_weather  = json.load(file)
	# 				# st_lottie(lottie_weather,height="300")
	# 				# st.markdown('<div style="text-align: center;">'+result_weather[0][1]+'</div>', unsafe_allow_html=True)

	# 				st.write("계측기정보")
	# 				df1 = pd.DataFrame(
	# 					(("주파수",result[0][4]),("me_pf",result[0][5])),
	# 					columns=("Name","Value"),
	# 				)
	# # CSS to inject contained in a string
	# 				hide_table_row_index = """
	# 							<style>
	# 							thead tr th:first-child {display:none}
	# 							tbody th {display:none}
	# 							</style>
	# 							"""

	# 				# Inject CSS with Markdown
	# 				st.markdown(hide_table_row_index, unsafe_allow_html=True)
	# 				st.table(df1)


			with col2:
				with st.container():
					st.write("현황")
					collu1,collu2,collu3,collu4,collu5 =st.columns(5)
					with collu1:
						file_path_solar = "./lotties/dash_solar.json"
						with open(file_path_solar, 'r') as file:lottie_direction = json.load(file)
						st_lottie(lottie_direction,key="dash_solar")
						st.markdown('<div style="text-align: center;">'+str(result[0][3])+'</div>', unsafe_allow_html=True)
					with collu2:
						if result[0][3] > 0 :
							file_path_onright = "./lotties/dash_onright.json"
							with open(file_path_onright, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_onright")
					with collu3:
						if result[0][3] > 0 or result[0][13] != 0 :
							file_path_ongreen = "./lotties/dash_ongreen.json"
							with open(file_path_ongreen, 'r') as file:lottie_direction  = json.load(file)
							st_lottie(lottie_direction)
						else:
							file_path_onyellow = "./lotties/dash_onyellow.json"
							with open(file_path_onyellow, 'r') as file:lottie_direction  = json.load(file)
							st_lottie(lottie_direction)

						if result[0][13] > 0 :
							file_path_onup = "./lotties/dash_onup.json"
							with open(file_path_onup, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_onup")
						elif result[0][13] < 0 : 
							file_path_ondown = "./lotties/dash_ondown.json"
							with open(file_path_ondown, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_ondown")
						elif result[0][13] == 0 : 
							st.warning("대기중")
							# file_path_onsleep = "./lotties/dash_onsleep.json"
							# with open(file_path_onsleep, 'r') as file:lottie_direction = json.load(file)
							# st_lottie(lottie_direction,key="dash_onsleep")

						if result[0][13] > 0 :
							file_path_uncharging = "./lotties/dash_uncharging.json"
							with open(file_path_uncharging, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_uncharging")
						elif result[0][13] < 0 : 
							file_path_charging = "./lotties/dash_charging.json"
							with open(file_path_charging, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_charging")
						elif result[0][13] == 0 : 
							if result[0][16] > 10 : 
								file_path_charged = "./lotties/dash_charged.json"
								with open(file_path_charged, 'r') as file:lottie_direction = json.load(file)
								st_lottie(lottie_direction,key="dash_charged")
							else:
								file_path_uncharged = "./lotties/dash_uncharged.json"
								with open(file_path_uncharged, 'r') as file:lottie_direction = json.load(file)
								st_lottie(lottie_direction,key="dash_uncharged")
						st.markdown('<div style="text-align: center;">SOC : '+str(result[0][16])+'%</div>', unsafe_allow_html=True)
			
					with collu4:
						if result[0][13] == 0 and result[0][3] > 0  :
							file_path_onright = "./lotties/dash_onright.json"
							with open(file_path_onright, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_onright1")
							on_outputelec = True
						elif result[0][13] > 0 :
							file_path_onright = "./lotties/dash_onright.json"
							with open(file_path_onright, 'r') as file:lottie_direction = json.load(file)
							st_lottie(lottie_direction,key="dash_onright1")
							on_outputelec = True
						else:
							on_outputelec = False


					with collu5:
						file_path_trans = "./lotties/dash_trans.json"
						with open(file_path_trans, 'r') as file:lottie_direction = json.load(file)
						st_lottie(lottie_direction,key="dash_ontrans")
						if on_outputelec :
							st.markdown('<div style="text-align: center;"> 송전중 </div>', unsafe_allow_html=True)
						else:
							st.markdown('<div style="text-align: center;"> 대기중 </div>', unsafe_allow_html=True)

  
			with col3:
				with elements("pcs_info"):
					st.write("pcs정보")
					colu1,colu2 = st.columns(2)
					with colu1:
						gauge_option = {
							"tooltip":{"formatter": "{a} <br/>{b} : {c}"},
							"series": [{"name":"kw/H","type": "gauge","min":-800,"max":800,"pointer":{"icon":"path://M12.8,0.7l12,40.1H0.7L12.8,0.7z","length":"12%","width":20,"offsetCenter":[0,"-60%"],"itmestyle":{"color":"inherit"}},"progress":{"show": "true"},"detail":{"valueAnimation":"true","formmater":"{value}"},"data": [{"value":result[0][13],"name":"PCS_power"}],}]
						}
						st_echarts(gauge_option,key = "pcs")

						df1 = pd.DataFrame(
							(("DC_V",result[0][7]),("DC_V_LINK",result[0][8]),("DC_A",result[0][9]),("DC_W",result[0][10]),("freq",result[0][11]),("pf",result[0][12]),("Aver_temp",result[0][14])),
							columns=("Name","Value"),
						)
					with colu2:
						st.table(df1)
		with st.container():
			col1,col2,col3 = st.columns(3)
			with col1:
				with st.container():
					st.write("배터리정보")
					colu1,colu2 = st.columns(2)
					
					with colu1:
						liquidfill_option = {
							"series": [{"type": "liquidFill", "data": [result[0][16]/100, result[0][16]/100*0.8, result[0][16]/100*0.6, result[0][16]/100*0.4],"shape":"container"}]
						}
						st_echarts(liquidfill_option)
					with colu2:
						
						df = pd.DataFrame(
							(("Heartbeat",result[0][15]),
							("SOH",result[0][17]),
							("Volte",result[0][18]),
							("Current",result[0][19]),
							("Charge power limit",result[0][20]),
							("discharge power limit",result[0][21]),
							("Aver_Temp",result[0][22])),
							columns=("Name","Value"),
						)
		# CSS to inject contained in a string
						hide_table_row_index = """
									<style>
									thead tr th:first-child {display:none}
									tbody th {display:none}
									</style>
									"""

						# Inject CSS with Markdown
						st.markdown(hide_table_row_index, unsafe_allow_html=True)

						st.table(df)
			with col2:
				with st.container():
						st.write("5일간의 발전 정보") 
						options = {
							"xAxis": {
								"type": "category",
								"boundaryGap": False,
								"data": ["Mon", "Tue", "Wed", "Thu", "Fri"],
							},
							"yAxis": {"type": "value"},
							"series": [
								{
									"data": [820, 932, 901, 934, 1290],
									"type": "line",
									"areaStyle": {},
								}
							],
						}
						st_echarts(options=options)
			with col3:
				with st.container():
									st.write("imd")
									colu1,colu2 = st.columns(2)
									with colu1:
										st.metric(label="센서1 온도(℃)", value=result[0][25] )

										st.metric(label="센서2 온도(℃)", value=result[0][26] ) 
									with colu2:

										df = pd.DataFrame(
											(("iso_v",result[0][23]),
											("test_alarm",result[0][24])),
											columns=("Name","Value"),
										)
						# CSS to inject contained in a string
										st.table(df)
		# with st.container():
		# 	colored_header(
		# 		label="오늘의 발전량은 "+str(result_genday[0][3])+"kw 입니다.",
		# 		description=" ",
		# 		color_name="orange-80",
		# 	)
# 		with st.container():
# 			colu1,colu2=st.columns(2)
# 			with colu1:
# 				# gauge_view = st.empty()
# 				# with gauge_view ,st.spinner("Wait for it..."):
# 				# 	time.sleep(1)
# 				# # gauge_view.empty()
# 				# # with st.spinner('Wait for it...'):
# 				# # 	time.sleep(1)
# 				# 	gauge_option = {
# 				# 		"tooltip":{"formatter": "{a} <br/>{b} : {c}"},
# 				# 		"series": [{"name":"kw/H","type": "gauge","max":800,"pointer":{"icon":"path://M12.8,0.7l12,40.1H0.7L12.8,0.7z","length":"12%","width":20,"offsetCenter":[0,"-60%"],"itmestyle":{"color":"inherit"}},"progress":{"show": "true"},"detail":{"valueAnimation":"false","formmater":"{value}"},"data": [{"value":result[0][3],"name":"발전력"}],}]
# 				# 	}
# 				# gauge_view.empty()
# 				# with gauge_view : st_echarts(gauge_option)
# 			with colu2:
# 				st.write("계측기정보")
# 				df1 = pd.DataFrame(
# 					(("주파수",result[0][4]),("me_pf",result[0][5])),
# 					columns=("Name","Value"),
#      			)
# # CSS to inject contained in a string
# 				hide_table_row_index = """
# 							<style>
# 							thead tr th:first-child {display:none}
# 							tbody th {display:none}
# 							</style>
# 							"""

# 				# Inject CSS with Markdown
# 				st.markdown(hide_table_row_index, unsafe_allow_html=True)
# 				st.table(df1)
	elif tabs == 'Location':
		switch_page('loc')
	elif tabs == 'Graph':
		coli1,coli2,coli3,coli4,coli5,coli6=st.columns([5,1,1,1,1,1])
		with coli1:
			st.title(str(result[0][1])+"  발전소" )
		with coli2:
			st.metric(label= "날씨" , value = result_weather[0][1] )
		with coli3:
			st.metric(label="온도(℃)", value=result_weather[0][2] )
		with coli4:
			st.metric(label="태양광", value=result[0][3] )
		with coli5:
			st.metric(label="PCS", value=result[0][13] )
		with coli6:
			st.metric(label="SOC", value=result[0][16] )
   
		colored_header(
			label=format(tabs),
			description = " ",
			color_name="violet-70",
		)
	elif tabs == 'ALARM':
		coli1,coli2,coli3,coli4,coli5,coli6=st.columns([5,1,1,1,1,1])
		with coli1:
			st.title(str(result[0][1])+"  발전소" )
		with coli2:
			st.metric(label= "날씨" , value = result_weather[0][1] )
		with coli3:
			st.metric(label="온도(℃)", value=result_weather[0][2] )
		with coli4:
			st.metric(label="태양광", value=result[0][3] )
		with coli5:
			st.metric(label="PCS", value=result[0][13] )
		with coli6:
			st.metric(label="SOC", value=result[0][16] )
   
		colored_header(
			label=format(tabs),
			description = " ",
			color_name="violet-70",
		)

if __name__ == '__main__' :
    main()
