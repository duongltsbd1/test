import streamlit as st
from netmiko import ConnectHandler
import telnetlib
import socket
import pandas as pd
import numpy as np
import random
import requests
import time
import json
import re
from sys import path
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
path.append('C:\\Users\\Admin\\Desktop\\python\\mynet\\info')
def take_info(file):
    device_str=open(file,"r").read()
    device_str_p=device_str.replace("'","\"")
    device_dir=json.loads(device_str_p)
    return device_dir
def check_heathy(ip_list):
    up_de=0
    device_info_list=[]
    for ip in ip_list:
        try:
            tn = telnetlib.Telnet(ip,22,2)
            up_de+=1
        except socket.timeout:
            continue
        except:
            st.write("sts went wrong")
    return up_de
def take_info_device(ip_list):
    sta=[]
    vers=[]
    device_list=[]
    modu=[]
    for ip in ip_list:
        file="C:\\Users\\Admin\\Desktop\\python\\mynet\\info/"+ip+".txt"
        device= take_info(file)
        device_list.append(device["device"])
    for device in device_list:
        try:
            connection = ConnectHandler(**device)
            sta.append(True)
            show_ver=connection.send_command('show version',read_timeout=2)
            version = re.search(r"Version (\S+),", show_ver)[1]
            module = re.search(r"Model number                    : (\S+)\n", show_ver)[1]
            modu.append(module)
            vers.append(version)
            connection.disconnect()
        except:
            sta.append(False)
            vers.append("")
            modu.append("")
            connection.disconnect()
            continue
    open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/sta_list.txt","w").write("")
    open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/vers_list.txt","w").write("")
    open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/modul_list.txt","w").write("")
    for i in range(len(sta)):
        open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/sta_list.txt","a").write(str(sta[i])+"\n")
        open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/vers_list.txt","a").write(str(vers[i])+"\n")
        open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/modul_list.txt","a").write(str(modu[i])+"\n")
    return sta,vers,modu
st.title('dashboard')
hide=st.empty()
device_list=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_list.txt","r").read().split("\n")
device_list.remove("")
ip_list=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/ip_list.txt","r").read().split("\n")
ip_list.remove("")
total=len(device_list)
up_de=int(open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/up_de.txt","r").read())
hide.metric("total device:", total, up_de)
sta_l=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/sta_list.txt","r").read().split("\n")
del(sta_l[-1])
sta=[]
for i in sta_l:
    if i == 'True':
        sta.append(True)
    else:
        sta.append(False)
vers=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/vers_list.txt","r").read().split("\n")
del(vers[-1])
modu=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/modul_list.txt","r").read().split("\n")
del(modu[-1])
try:
    df = pd.DataFrame(
        {
           "name": device_list,
            "ip": ip_list,
            "status": sta,
            "version": vers,
            "module": modu
            #"recom_ver": recom
        }
    )
except:
    sta,vers,modu=take_info_device(ip_list)
    df = pd.DataFrame(
        {
           "name": device_list,
            "ip": ip_list,
            "status": sta,
            "version": vers,
            "module": modu
            #"recom_ver": recom
        }
    )
edited_df = st.data_editor(
    df,
    use_container_width= True,
    hide_index=True,
    column_config={
        "name": "Device Name",
        "ip": "ip",
        "status": "status",
        "version": "current version",
        "module": "module"
    },
    disabled=df.columns
)
sta,vers,modu=take_info_device(ip_list)
while True:
    up_de_new=check_heathy(ip_list)
    if up_de != up_de_new:
        open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/up_de.txt","w").write(str(up_de_new))
        up_de=up_de_new
        hide.empty()
        hide.metric("total device:", total, up_de)
    time.sleep(60)
