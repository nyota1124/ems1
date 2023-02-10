from time import sleep
import json
import requests
import streamlit as st

import sys 
import pandas as pd
import sqlite3 
import hashlib
import folium
import numpy as np
from st_on_hover_tabs import on_hover_tabs
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
import mpl_gauge,plotly_gauge

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

    # lottie_url_hello = "./car-ani.json"
    # lottie_hello = load_lottieurl(lottie_url_hello)
def main():
	m=st.markdown('<style>' + open('./css/style.css').read() + '</style>', unsafe_allow_html=True)
	
	with st.spinner(text='In progress'):sleep(2)
	st.balloons()
	
	file_path = "./lotties/car-ani.json"
	with open(file_path, 'r') as file:lottie_hello  = json.load(file)

	with st.sidebar:
		st_lottie(lottie_hello)
		tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], 
							iconName=['dashboard', 'money', 'economy'], default_choice=0)

	colored_header(
		label=format(tabs),
		description = " ",
		color_name="violet-70",
	)
	with st.container():
		col1,col2,col3,col4,col5 = st.columns(5)
		col1.metric(label="Gain", value=5000, delta=1000)
		col2.metric(label="Loss", value=5000, delta=-1000)
		col3.metric(label="No Change", value=11111, delta=0)
		col4.metric(label="No Change", value=4567, delta=60)
		col5.metric(label="No Change", value=1234, delta=-80)  
		style_metric_cards(background_color="black-70")
	
	with st.container():
		colu1,colu2=st.columns(2)
		with colu1:
			gauge_plot = mpl_gauge.gauge(labels=['Very Low','Low','Medium','High','Very High'],colors=['#2FCC71','#1F8449','#F4D03F','#F5B041','#C03A2B'],arrow=2, title='100 Kwh')
			st.pyplot(gauge_plot)
		with colu2:
			bullet_plot = plotly_gauge.plotly_bullet(3)
			bullet_plot.update_layout(height = 250)
			st.plotly_chart(bullet_plot, use_container_width=True, height=500)
		












if __name__ == '__main__' :
    main()