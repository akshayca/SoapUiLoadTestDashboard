#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pymssql
import pandas as pd
import os
import csv
import glob
from functools import reduce
import matplotlib.pyplot as plt
import pandas_bokeh
import dash_bootstrap_components as dbc
import io
from base64 import b64encode

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


# Copy the all the statistics file paths

# In[14]:


path="C:/SoapUiLoadTest/TestResults/202110021159"
all_files = glob.glob(os.path.join(path, "*statistics.txt"))


# Create xlsx sheet where you want merge all the files

# In[44]:


excelfilename = 'LoadTestResults_'+"202110021159"+'.xlsx'
writer = pd.ExcelWriter(os.path.join(path,excelfilename), engine='xlsxwriter')


# Filter the data and archive save in database
# 

# Connect to Database

# In[45]:


conn = pymssql.connect(host = 'MSI', user='akshay', password='akshay', database = 'SoapUILoadTestResults')
cursor = conn.cursor()


# Few common methods

# In[46]:


tags =[path, '-statistics.txt','\\']


# In[7]:


def createTable(curr,trimedFilename):
    trimedFilenameQ="'"+trimedFilename+"'"
    create_table_statement = "IF NOT EXISTS ( SELECT [name] FROM sys.tables WHERE [name] = {})CREATE TABLE {} (TimeStamp VARCHAR(255), Test_Step VARCHAR(255) NOT NULL, min INTEGER NOT NULL, max INTEGER NOT NULL, avg INTEGER NOT NULL, last INTEGER NOT NULL,cnt INTEGER NOT NULL, tps INTEGER NOT NULL, bytes INTEGER NOT NULL, bps INTEGER NOT NULL)".format(trimedFilenameQ,trimedFilename)
    cursor.execute(create_table_statement)

def insert_into_table(curr,trimedFilename,TimeStamp,Test_Step,min,max,avg,last,cnt,tps,bytes,bps):
    Test_Step = "'"+Test_Step+"'"
    TimeStamp = "'"+TimeStamp+"'"
    insert_into_videos = insert_statement ="INSERT INTO {}(TimeStamp,Test_Step,min,max,avg,last,cnt,tps,bytes,bps)VALUES({},{},{},{},{},{},{},{},{},{})".format(trimedFilename,TimeStamp,Test_Step,min,max,avg,last,cnt,tps,bytes,bps)
    cursor.execute(insert_into_videos)

def append_from_df_to_db(curr,df):
    for i, row in df.iterrows():
        insert_into_table(curr, trimedFilename, row['TimeStamp'],row['Test_Step'], row['min'], row['max'], row['avg'], row['last'], row['cnt']
                          , row['tps'], row['bytes'], row['bps'])


def truncate_table(curr,trimedFilename):
    truncate_table ="TRUNCATE TABLE {}".format(trimedFilename)
    curr.execute(truncate_table)
       
def removeJunk(df):   
    df.drop(['rat','err'], axis = 'columns',inplace=True)   
    df.drop(df[df['Test Step'].str.contains('Groovy') |
           df['Test Step'].str.contains(r'\bProperties[a-zA-Z]*\b') |
           df['Test Step'].str.contains(r'\bTestCase[a-zA-Z]*\b')].index,inplace=True) 

    df.rename(columns = {'Test Step':'Test_Step'}, inplace = True)
    df.reset_index(drop=True, inplace=True)
    
def returnTables(curr):
    getTables = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES"
    curr.execute(getTables)
    tables=curr.fetchall()
    return tables


def getDataFrame(curr, tableName):
    getArchive = "SELECT * from {}".format(tableName)
    curr.execute(getArchive)
    data=cursor.fetchall()
    dfa = pd.DataFrame(data)
    dfa.columns =['TimeStamp','Test_Step','min','max','avg','last','cnt','tps','bytes','bps']
    return dfa

def generateGraphs(dfa):
    fig1 = px.line(dfa, x='TimeStamp', y='min', color='Test_Step', markers=True)
    fig2 = px.line(dfa, x='TimeStamp', y='max', color='Test_Step', markers=True)
    fig3 = px.line(dfa, x='TimeStamp', y='avg', color='Test_Step', markers=True)
    fig1.show()
    fig2.show()
    fig3.show()
    


# Archive the data to the database and to the excel sheet

# In[48]:


for f in all_files:
    df = pd.read_csv(f)
    removeJunk(df)
    
    trimedFilename = reduce(lambda a,b: a.replace(b, ''), tags, f)
    trimedSheetname= reduce(lambda a,b: a.replace(b, ''), tags, f)
    
    df.to_excel(writer, sheet_name=os.path.basename(trimedSheetname))  
   
    date= pd.to_datetime('now').date().isoformat()
    df.insert(0, 'TimeStamp', date)
    createTable(cursor,trimedFilename)
    append_from_df_to_db(cursor,df)
    
writer.save()


# Save the connection

# In[21]:


conn.commit()

cursor.close()

conn.close()


# Create the dash board using dash and plotly

# In[22]:


conn = pymssql.connect(host = 'MSI', user='akshay', password='akshay', database = 'SoapUILoadTestResults')
cursor = conn.cursor()


# Create the dropdown to select the table

# In[23]:


tables = returnTables(cursor)
tablelist =[]

for table in tables:
    tablelist.append({'label': table[0], 'value': table[0]})


# In[24]:


print(tables)


# In[25]:


# df1 = getDataFrame(cursor,tables[0][0])
# generateGraphs(df1)


# In[30]:


print(dcc.__version__) # 0.6.0 or above is required 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 
app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        dcc.Graph(id='avg_graph')
    ],className='nine columns'),

    html.Div([
        html.H1("SoapUi Load Test Results"),
        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Please choose a test from the dropdown:'],style={'font-weight': 'bold', "text-align": "center"}),
 
        dcc.Dropdown(id='my_dropdown',
            options=tablelist,
            optionHeight=40,                   
            value=tables[0][0],                   
            disabled=False,                   
            multi=False,                       
            searchable=True,                   
            search_value='',                   
            placeholder='Type search query here ...',    
            clearable=True,                    
            style={'width':"100%",'height':'100%'},            

            ),
    ],className='three columns'),

])


@app.callback(
    Output(component_id='avg_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

 

def build_graph_avg(column_chosen):

    dfa = getDataFrame(cursor,column_chosen)

    fig = px.line(dfa, x='TimeStamp', y='avg', color='Test_Step', markers=True,height=850)

    return fig

 
if __name__ == '__main__':

    app.run_server(debug=True)

 


# In[ ]:


conn.commit()
cursor.close()
conn.close()

