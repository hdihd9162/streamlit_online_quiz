import streamlit as st
from csv import writer
from datetime import datetime
from PIL import Image
import os

def page_setting():

    im = Image.open("icon.jpg")
    st.set_page_config(
        page_title="online exam",
        page_icon=im,
    )
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            p, div, input, label {
            unicode-bidi:bidi-override;
            direction: RTL;
            text-align: right;
            }
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def user(intro_quistion,multipleـchoice_quistion,descriptive_quistion,all_input_result):
    res_file = open( all_input_result, "r" )
    data4 = []
    for line in res_file:
        number_strings = line.split(",") 
        numbers = [str(n) for n in number_strings]
        data4.append(numbers) 
    st.metric(label="تعداد ثبت نام", value=len(data4))
    about = open( intro_quistion, "r" )
    data3 = []
    for line in about:
        data3.append(line)

    multipleـchoice = open( multipleـchoice_quistion, "r" )
    data = []
    for line in multipleـchoice:
        number_strings = line.split(",") 
        numbers = [str(n) for n in number_strings]
        data.append(numbers) 

    descriptive = open( descriptive_quistion, "r" )
    data2 = []
    for line in descriptive:
        data2.append(line)

    list_res=[]

    for i in range(len(data3)):
        res=st.text_input(data3[i])
        if res=="":
            res="خالی"
        list_res.append(res)

    for i in range(len(data)):
        
        res=st.radio(
        data[i][0],
        (data[i][1], data[i][2], data[i][3],data[i][4]))
        list_res.append(res)

    for i in range(len(data2)):
        res=st.text_area(data2[i])
        if res=="":
            res="خالی"
        list_res.append(res)


    flag_check_copy=1


    for i in range(len(data4)):
        if data4[i][0] == list_res[0] and data4[i][1] == list_res[1] and data4[i][2] == list_res[2] and data4[i][3] == list_res[3] : 
            print(1)
            flag_check_copy=0
            break
    if list_res[0]!="خالی" and list_res[1]!="خالی" and list_res[2]!="خالی" and list_res[3]!="خالی" and flag_check_copy==1:
        if st.button('ارسال جواب'):
            st.write('نتایج ذخیره شد ')
            now = datetime.now()
            list_res.append(now)
            with open(all_input_result, 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(list_res)
                f_object.close()
            map_dict = {'ا': '1', 'ب': '2', 'پ': '3','ت': '4', 'ث': '5', 'ج': '6','چ': '7', 'ح': '8', 'خ': '9','د': '0', 'ذ': '10', 'ر': '11','ز': '12', 'ژ': '13', 'ط': '14','ظ': '15', 'س': '16', 'ش': '17','ص': '18', 'ض': '19', 'ع': '20','غ': '21', 'ف': '22', 'ق': '23','ک': '24', 'گ': '25', 'ل': '26','م': '27', 'ن': '28', 'و': '29','ه': '30', 'ی': '31','۱': '32', '۲': '33', '۳': '34','۴': '1', '۵': '35', '۶': '36','۷': '37', '۸': '38', '۹': '39', '۰': '40'}
            tmp_name=str(list_res[0]+list_res[1]+list_res[2])
            tmp_name=''.join(idx if idx not in map_dict else map_dict[idx] for idx in tmp_name)
            print(tmp_name)
            with open(tmp_name+".csv", 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(list_res)
                f_object.close()

            with open(tmp_name+".csv", "rb") as file:
                st.download_button(
                    label="دانلود نتایج",
                    data=file,
                    file_name=tmp_name+'.csv',
                    mime='text/csv',
                )

def admin(multipleـchoice_quistion,descriptive_quistion,all_input_result):
    user=st.text_input("username")
    password=st.text_input("pass", type="password")
    if user=="admin" and password == "admin" :
        st.success('وارد شدید', icon="✅")
        now = datetime.now()
        with open(all_input_result, "rb") as file:
            st.download_button(
                label="دانلود نتایج",
                data=file,
                file_name='res'+str(now)+'.csv',
                mime='text/csv',
            )
        multipleـchoice_file=st.file_uploader("چهار گزینه ای")
        descriptive_file=st.file_uploader("تشریحی")
        if st.button('اعمال'):
            if multipleـchoice_file is not None:
                multipleـchoice_file_data=multipleـchoice_file.getvalue().decode('utf-8')
                with open(multipleـchoice_quistion, 'w') as f: 
                    f.write(multipleـchoice_file_data)
                    f.close()
            if descriptive_file is not None:
                descriptive_file_data=descriptive_file.getvalue().decode('utf-8')
                with open(descriptive_quistion, 'w') as f: 
                    f.write(descriptive_file_data)
                    f.close()

def check_file_exist(intro_quistion,multipleـchoice_quistion,descriptive_quistion,all_input_result):
    if not os.path.isfile(all_input_result):
        fp = open(all_input_result, 'w')
        fp.close()
    if not os.path.isfile(intro_quistion) or (not os.path.isfile(multipleـchoice_quistion) and not os.path.isfile(descriptive_quistion)):
        st.error('سوالات هنوز بارگذاری نشدند', icon="🚨")
        return 1
    if not os.path.isfile(multipleـchoice_quistion):
        fp = open(multipleـchoice_quistion, 'w')
        fp.close()
    if not os.path.isfile(descriptive_quistion):
        fp = open(descriptive_quistion, 'w')
        fp.close()
    return 0


page_setting()

intro_quistion="questions/q.csv"
multipleـchoice_quistion="questions/q1.csv"
descriptive_quistion="questions/q2.csv"
all_input_result="all_results/res.csv"

page=st.radio(
    "ورود مدیر سیستم یا کاربر عادی",
    ("کاربر عادی","مدیر سیستم"))
flag_empty= check_file_exist(intro_quistion,multipleـchoice_quistion,descriptive_quistion,all_input_result)


if page == "کاربر عادی" and flag_empty==0:
    user(intro_quistion,multipleـchoice_quistion,descriptive_quistion,all_input_result)
    
if page == "مدیر سیستم":
    admin(intro_quistion,multipleـchoice_quistion,descriptive_quistion,all_input_result)
