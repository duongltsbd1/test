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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
path.append('mynet\\info')
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
        file="info/"+ip+".txt"
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
    open("info/sta_list.txt","w").write("")
    open("info/vers_list.txt","w").write("")
    open("info/modul_list.txt","w").write("")
    for i in range(len(sta)):
        open("info/sta_list.txt","a").write(str(sta[i])+"\n")
        open("info/vers_list.txt","a").write(str(vers[i])+"\n")
        open("info/modul_list.txt","a").write(str(modu[i])+"\n")
    return sta,vers,modu
def get_score(str1,list_str,list_md):
    list_score=[]
    for i_1 in list_str:    
        if str1.startswith("WS-C"):
            if str1[4:8] in i_1:
                score=1000
            else:
                score=0
        else:
            score=0
        dup=0
        for i_2 in range(len(str1)):
            up=1
            add_sc=1
            check=str1[i_2] in i_1
            if check:
                dup+=1
            while check:
                up+=1
                add_sc+=1
                check=str1[i_2:i_2+up] in i_1
                if i_2+up > len(str1):
                    check=False
            score+=add_sc
        list_score.append(score*dup)
    max=list_score[0]
    index_max=0
    for i in range(len(list_str)):
        if list_score[i]>max:
            max=list_score[i]
            index_max=i
    return list_score[index_max],list_md[index_max]
def get_recom_ver(modu_list):
    recom_vers=[]
    router=open("info/router_concept.txt","r").read().split("\n")
    router_md=open("info/router_ID.txt","r").read().split("\n")
    switch=open("info/switch_concept.txt","r").read().split("\n")
    switch_md=open("info/switch_ID.txt","r").read().split("\n")
    for i_1 in modu_list:
        if i_1 !="":
            router_sc,mdfId_r=get_score(i_1,router,router_md)
            sw_sc,mdfId_s=get_score(i_1,switch,switch_md)
            if router_sc > sw_sc:
                mdfId=mdfId_r
            else:
                mdfId=mdfId_s
            driver = webdriver.Chrome()
            url_ver="https://software.cisco.com/download/home/"+mdfId+"/type/280805680"
            driver.get(url_ver)
            time.sleep(2)
            content_get=driver.find_element(By.CSS_SELECTOR, 'span.selectedRelease')
            recom_vers.append(content_get.text)
        else:
            recom_vers.append("")
    return recom_vers
st.title('dashboard')
hide=st.empty()
device_list=open("info/device_list.txt","r").read().split("\n")
device_list.remove("")
ip_list=open("info/ip_list.txt","r").read().split("\n")
ip_list.remove("")
total=len(device_list)
up_de=int(open("info/up_de.txt","r").read())
hide.metric("total device:", total, up_de)
sta_l=open("info/sta_list.txt","r").read().split("\n")
del(sta_l[-1])
sta=[]
for i in sta_l:
    if i == 'True':
        sta.append(True)
    else:
        sta.append(False)
vers=open("info/vers_list.txt","r").read().split("\n")
del(vers[-1])
modu=open("info/modul_list.txt","r").read().split("\n")
del(modu[-1])
recom_ver=get_recom_ver(modu)
try:
    df = pd.DataFrame(
        {
           "name": device_list,
            "ip": ip_list,
            "status": sta,
            "version": vers,
            "module": modu,
            "recom_ver": recom_ver
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
            "module": modu,
            "recom_ver": recom_ver
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
        "module": "module",
        "recom_ver": "recommend version"
    },
    disabled=df.columns
)
sta,vers,modu=take_info_device(ip_list)
while True:
    up_de_new=check_heathy(ip_list)
    if up_de != up_de_new:
        open("info/up_de.txt","w").write(str(up_de_new))
        up_de=up_de_new
        hide.empty()
        hide.metric("total device:", total, up_de)
    time.sleep(60)
