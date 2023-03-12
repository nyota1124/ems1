import streamlit as st
import pandas as pd
import sqlite3 
import hashlib
import folium
from time import sleep
from streamlit_folium import st_folium
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
st.set_page_config(initial_sidebar_state="collapsed")
with st.spinner(text='In progress'):
    sleep(2)


# m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)


# call to render Folium map in Streamlit

# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# 웹 대시보드 개발 라이브러리인 스트림릿은,
# main 함수가 있어야 한다.
# def create_user():
# 	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

# def add_user(username,password):
# 	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
# 	conn.commit()

# def login_user(username,password):
# 	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
# 	data = c.fetchall()
# 	return data
def loginfn(user_id,user_pwd):
    
    if (user_id == "" or user_pwd == "" ):
        return "아이디나 비밀번호를 입력해 주세요"
    elif (user_id == "1234"):
        return "3333"
    else:
        return user_id + user_pwd
    
def main():
	m = st.markdown("""
	<style>
		div[data-testid="stSidebarNav"] {display: none;}
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
	div.horizon {
		background-color:#ce1126;
	}
 	.css-uzfz7i {
        display: none;
    }

	</style>""", unsafe_allow_html=True)

  
	st.title("EF-EMS")
	with st.form(key='my_form',clear_on_submit=True):
		st.subheader(":blue[Login]")
		
		user_id = st.text_input("id 를 입력해 주세요",key='user_idk')
		user_pwd = st.text_input("pwd 입력 해 주세요",key='user_pwdk',type='password')
		col1, col2  = st.columns(2)	
		with col1:login_btn = st.form_submit_button(label="Login")
		with col2:reset_btn = st.form_submit_button(label="문의")
 
	if reset_btn:
		st.info("nyota1124@gmail.com")
		# st.experimental_rerun()

	if login_btn:
		if loginfn(user_id,user_pwd)=="3333":
			st.warning("succes")
			switch_page("loc")
		else :
			st.warning(loginfn(user_id,user_pwd))
	
  	
 	# user_id = st.text_input("ユーザー名を入力してください")
	# password = st.text_input("パスワードを入力してください",type='password')
	# fg = folium.FeatureGroup(name="State bounds")
 
	# fg.add_child(folium.features.)

	# capitals = STATE_DATA

	# for capital in capitals.itertuples():
	# 	fg.add_child(
	# 		folium.Marker(
	# 			location=[capital.latitude, capital.longitude],
	# 			popup=f"{capital.capital}, {capital.state}",
	# 			tooltip=f"{capital.capital}, {capital.state}",
	# 			icon=folium.Icon(color="green")
	# 			if capital.state == st.session_state["selected_state"]
	# 			else None,
	# 		)
	# 	)

	# out = st_folium(
	# 	m,
	# 	feature_group_to_add=fg,
	# 	center=center,
	# 	width=1200,
	# 	height=500,
	# )
		
# call to render Folium map in Streamlit

    
	# menu = ["ホーム","ログイン","サインアップ"]
    
	# choice = st.sidebar.selectbox("メニュー",menu)

	# if choice == "ホーム":
	# 	st.subheader("첫번째 화면")
		
	# elif choice == "ログイン":
	# 	st.subheader("ログイン画面です")

	# 	username = st.sidebar.text_input("ユーザー名を入力してください")
	# 	password = st.sidebar.text_input("パスワードを入力してください",type='password')
		# if st.sidebar.checkbox("ログイン"):
		# 	# create_user()
		# 	# hashed_pswd = make_hashes(password)

		# 	# result = login_user(username,check_hashes(password,hashed_pswd))
		# 	if result:

		# 		st.success("{}さんでログインしました".format(username))

		# 	else:
		# 		st.warning("ユーザー名かパスワードが間違っています")

	# elif choice == "サインアップ":
	# 	st.subheader("新しいアカウントを作成します")
	# 	new_user = st.text_input("ユーザー名を入力してください")
	# 	new_password = st.text_input("パスワードを入力してください",type='password')
  
  
   

		# if st.button("サインアップ"):
		# 	create_user()
		# 	add_user(new_user,make_hashes(new_password))
		# 	st.success("アカウントの作成に成功しました")
		# 	st.info("ログイン画面からログインしてください")
if __name__ == '__main__' :
    main()