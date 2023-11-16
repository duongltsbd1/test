import streamlit as st
import numpy as np
import pandas as pd
import os
import time
import json
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
device_list=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_list.txt","r").read().split("\n")
device_list.remove("")
ip_list=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/ip_list.txt","r").read().split("\n")
ip_list.remove("")
st.title('Device manager')
h=st.empty()
k=st.empty()
def dataframe_with_selections(df,device_list):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    global h
    edited_df = h.data_editor(
        df_with_selections,
        use_container_width= True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=True),
            "name": "Device Name",
            "ip": "ip"
        },
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    check= True
    i=0
    dli=[]
    ili=[]
    while check:
        try:
            dli.append(selected_rows["name"][i])
            ili.append(selected_rows["ip"][i])
        except:
            i+=1
            if i>len(device_list):
                check =False
            continue
        i+=1
        if i > len(device_list):
            check = False
    return selected_rows.drop('Select', axis=1),dli,ili
def delete_fu(dli,ili):
    global device_list,ip_list
    for i in dli:
        device_list.remove(i)
    for i in ili:
        ip_list.remove(i)
        cmd="del info\\"+i+".txt"
        os.system(cmd)
    device_lis=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_list.txt","w")
    for i in device_list:
        device_lis.write("\n")
        device_lis.write(i)
    device_lis.close()
    ip_lis=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/ip_list.txt","w")
    for i in ip_list:
        ip_lis.write("\n")
        ip_lis.write(i)
    ip_lis.close()
    st.toast("delete successful!:heavy_check_mark:")
    time.sleep(1)
    st.rerun()
    
    return None
def take_info(file):
    device_str=open(file,"r").read()
    device_str_p=device_str.replace("'","\"")
    device_dir=json.loads(device_str_p)
    return device_dir
def add_device(file,name,ip,dtype,user,passw):
    f=open(file,mode = 'w')
    device={
        "device": {"device_type": dtype,"host": ip,"username": user,"password": passw},
        "name": name
    }
    f.write(str(device))
    f.close()
def s_edit():
    if st.session_state.username =="" or st.session_state.passw =="":
        st.error("miss info!")
        device_type_l=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_type.txt","r").read().split("\n")
        device_type_l.remove(device["device"]["device_type"])
        device_type_l.insert(0,device["device"]["device_type"])
        device_type=tuple(device_type_l)
        with st.form("add_device"):
            st.text("Device name:")
            st.text(device["name"])
            st.text("ip:")
            st.text(device["device"]["host"])
            device_t = st.selectbox(
                'device type',
                device_type,
                key="device_t"
            )
            st.text_input("username:",device["device"]["username"], key="username")
            st.text_input("password:",device["device"]["password"], key="passw")
            co1,co2 = st.columns(2)
            with co1:
                submitted = st.form_submit_button("Submit",on_click= s_edit)
            with co2:
                cancel = st.form_submit_button("Cancel",type="secondary")
        st.stop()
    else:
        cmd="del info\\"+device["device"]["host"]+".txt"
        os.system(cmd)
        file="C:\\Users\\Admin\\Desktop\\python\\mynet\\info/"+str(device["device"]["host"])+".txt"
        try:
            add_device(file,str(device["name"]),str(device["device"]["host"]),st.session_state.device_t,st.session_state.username,st.session_state.passw)
        except:
            st.write(device_t_l)
        st.toast("successful!:heavy_check_mark:")
    return None
def edit_info(device):
    device_type_l=open("C:\\Users\\Admin\\Desktop\\python\\mynet\\info/device_type.txt","r").read().split("\n")
    device_type_l.remove(device["device"]["device_type"])
    device_type_l.insert(0,device["device"]["device_type"])
    device_type=tuple(device_type_l)
    with st.form("add_device"):
        st.text("Device name:")
        st.text(device["name"])
        st.text("ip:")
        st.text(device["device"]["host"])
        device_t = st.selectbox(
            'device type',
            device_type,
            key="device_t"
        )
        st.text_input("username:",device["device"]["username"], key="username")
        st.text_input("password:",device["device"]["password"], key="passw")
        co1,co2 = st.columns(2)
        with co1:
            submitted = st.form_submit_button("Submit",on_click= s_edit)
        with co2:
            cancel = st.form_submit_button("Cancel",type="secondary")
st.write("st should be here")
df = pd.DataFrame(
    {
        "name": device_list,
        "ip": ip_list,
        #"status": sta
    }
)
selection,dli,ili = dataframe_with_selections(df,device_list)
with k.form("my form"):
    col1, col2 ,col3, col4, col5, col6 ,col7, col8 = st.columns(8)
    with col1:
        if len(dli)!=0:
            delete = st.form_submit_button(":red[delete]")
        else:
            delete = st.form_submit_button("delete",disabled=True)
    with col2:
        if len(dli)==1:
            edit = st.form_submit_button("edit")
        else:
            edit = st.form_submit_button("edit",disabled=True)
if delete:
    delete_fu(dli,ili)
if edit:
    k.empty()
    h.empty()
    hea="edit: " + dli[0] + "/" + ili[0]
    st.header(hea)
    file="C:\\Users\\Admin\\Desktop\\python\\mynet\\info/"+ili[0]+".txt"
    device=take_info(file)
    edit_info(device)
    st.stop()