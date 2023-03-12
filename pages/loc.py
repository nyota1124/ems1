import streamlit as st
import pandas as pd
import sqlite3 
import hashlib
import folium
from time import sleep
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

cities = [[37.566687, 126.978417,"서울",0],
          [35.179774, 129.075004,"부산",1],
          [37.455900, 126.705522,"인천",2],
          [35.871380, 128.601743,"대구",3],
          [36.350451, 127.384827,"대전",4],
          [35.160072, 126.851440,"광주",5]]



def viewfn(select_code):
    select_code1 = select_code["last_object_clicked"]
    if type(select_code1) is dict:
        sc_lat = select_code1.get("lat",0)
        sc_lng = select_code1.get("lng",0)
        
        newlist=[(i,j) for i in range(6) for j in range(3) if cities[i][j]==sc_lat]
        index_code =newlist[0][0]
        
        # return_code= st.write(str(sc_lat) + "|" + str(sc_lng) + "$$$$$" +str(cities[index_code][2])) 
        return_code1 = st.button(label=str(cities[index_code][2]))
        # return_code1 = st.warning("1234")
        
    else:    
        return_code = st.warning("선택된 지역이 없습니다.")
        return_code1 = None
        # select_code1 = type(select_code1)
 
    return return_code1

def main():
	m = st.markdown("""
	<style>
		div.stButton > button:first-child {
	    background-color: #49B74E;
		color: white;
		height: 3em;
		width: 12em;
		border-radius:20px;
		border:1px solid #000000;
		font-size:20px;
		font-weight: bold;
		margin: auto;
		display: block;
	}
	div.stButton > button:hover {
		background:linear-gradient(to bottom, #ce1126 5%, #ff5a5a 100%);
		background-color:#ce1126;
	}
	div.stButton > button:active {
		position:relative;
		top:3px;
	}
 	.css-79elbk{
		display:none;
	}
 	.css-uzfz7i {
        display: none;
    }
    Button[kind="header"] {
        display: none;
    }
	.css-1vencpc {
    display:none;
}

	</style>""", unsafe_allow_html=True)

	
	

	st.title("EF-EMS에 오신걸 환영합니다. ")
	st.subheader("Site 를 선택 해 주세요")




	
	m = folium.Map( location=[36.577629, 127.770135], zoom_start=7)

	for i in range(len(cities)):

		html = """<b> """ 
		html = html + str(cities[i][2]) +" 발전소"
		html = html + "</b>"""
		iframe = folium.IFrame(html=html, width=200, height=100)
		
		folium.Marker(location=[cities[i][0],cities[i][1]],icon=folium.Icon(color='red',icon='ok'),tooltip=folium.Tooltip(iframe.render())).add_to(m)
	
	output=st_folium(m,width=1200, returned_objects=["last_object_clicked"])
	# st.write(output)
	output_btn=viewfn(output)
	if output_btn:
		switch_page("main")
		# output_btn.onclick = switch_page("main")
		# switch_page("main")

if __name__ == '__main__' :
    main()