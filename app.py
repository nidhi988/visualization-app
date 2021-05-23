#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sweetviz as sv
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask,send_from_directory
import pandas as pd
from pywebio.input import file_upload
from pywebio.output import put_html,put_loading
from pywebio import start_server
import csv
import re
import argparse
import nest_asyncio
import os
nest_asyncio.apply()


# In[ ]:


app=Flask(__name__)

def apps():
    file=file_upload(label='Upload CSV file', accept='.csv')
    content=file['content'].decode('utf-8').splitlines()
    
    df=content_pandas(content)
    create_profile_info(df)
    
def create_profile_info(df: pd.DataFrame):
    with put_loading(shape='grow'):
        report=sv.analyze(df)
        report.show_html()
    with open('SWEETVIZ_REPORT.html','r')as f:
        html=f.read()
        put_html(html)

def content_pandas(content: list):
    with open("tmp.csv","w") as csv_file:
        writer=csv.writer(csv_file,delimiter='\t')
        for line in content:
            writer.writerow(re.split('\st',line))
        return pd.read_csv("tmp.csv")

#if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-p", "--port", type=int, default=8080)
    #args = parser.parse_args()
    
app.add_url_rule('/hello','webio_view',webio_view(apps),methods=['GET','POST','OPTIONS'])

#app.run(host='localhost',port=36535)
app.run(host='localhost',port=os.environ.get('PORT', '5000'))
    
#start_server(app,port=36535,debug=True)

