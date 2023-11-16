import streamlit as st
import pandas as pd
import numpy as np
import os
import time

st.set_page_config(
    page_title="MyNet",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# :rainbow[Made by me!] :sparkles:"
    }
)
def add_device(file,name,ip,dtype,user,passw):
    f=open(file,mode = 'w')
    device={
        "device": {"device_type": dtype,"host": ip,"username": user,"password": passw},
        "name": name
    }
    f.write(str(device))
    f.close()

from sys import path
path.append('C:\\Users\\Admin\\Desktop\\python\\mynet\\info')
device_type_l=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_type.txt","r").read().split("\n")
device_type=tuple(device_type_l)
st.title('Add device')
with st.form("add_device",clear_on_submit=True):
    st.text_input("Device name:", key="name")
    st.text_input("ip[x.x.x.x]:", key="ip")
    device_t = st.selectbox(
        'device type',
        device_type
    )
    st.text_input("username:", key="username")
    st.text_input("password:", key="passw")
    submitted = st.form_submit_button("Submit")
    if submitted and (st.session_state.name=="" or st.session_state.ip=="" or st.session_state.username=="" or st.session_state.passw==""):
        st.error("miss info!")
    elif submitted:
        device_list=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_list.txt","r").read().split("\n")
        ip_list=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/ip_list.txt","r").read().split("\n")
        if st.session_state.name not in device_list or st.session_state.ip not in ip_list:
            add=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_list.txt","a")
            add.write("\n")
            add.write(st.session_state.name)
            add.close()
            add=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/ip_list.txt","a")
            add.write("\n")
            add.write(st.session_state.ip)
            add.close()
            file="C:\\Users\\Admin\\Desktop\\python\\mynet\\info/"+str(st.session_state.ip)+".txt"
            add_device(file,st.session_state.name,st.session_state.ip,device_t,st.session_state.username,st.session_state.passw)
            st.toast("successful!:heavy_check_mark:")
            time.sleep(0.25)
        else:
            st.toast("this device already exist!:heavy_multiplication_x:")

        