import streamlit as st
import pandas as pd
import numpy as np
import time

from sklearn.impute import SimpleImputer

st.image("./assets/logo.png")
st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
def initSessionState():
    if 'df' not in st.session_state:
        st.session_state['df'] = None
    if 'showDfButton' not in st.session_state:
        st.session_state['showDfButton'] = False 

initSessionState()

# Callbacks

def buttonClick():
    st.session_state['showDfButton'] = not st.session_state['showDfButton']

def nLine(n=1):
    for _ in range(n):
        st.write('\n')

def progressBar():
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.0002)
        my_bar.progress(percent_complete + 1)


@st.cache_data
def loadData(path):
    df = pd.read_csv(path)
    return df

# Upload file
# Load dataset
if st.session_state['df'] is None:
    uploadedFile = st.file_uploader("Upload your Dataset", type="csv")
    if uploadedFile:
        df = loadData(uploadedFile)
        st.session_state['df'] = df

        

# Initialize dataframe
if st.session_state['df'] is not None:
    df = st.session_state['df']

    st.divider()
    nLine()

    # EDA

    st.markdown('### 📊 Exploratory Data Analysis', unsafe_allow_html=True)
    nLine()

    with st.expander("Basic Information"):
        nLine()

        head = st.checkbox('Show 5 Samples ',value = False)
        if head:
            nLine()
            st.dataframe(df.sample(5), use_container_width=True)
        
        shape = st.checkbox('Show Shape',value=False)
        if shape:
            st.write(f'This Dataframe has **{df.shape[0]} rows** and **{df.shape[1]} columns**')

        numStats = st.checkbox('Discriptive Statistics **(Numerical)**')
        if numStats:
            nLine()
            st.dataframe(round(df.describe(),2),use_container_width=True)

        catStats = st.checkbox('Discriptive Statistics **(Categorical)**')
        if catStats:
            if df.select_dtypes(include=object).columns.tolist():
                nLine()
                st.dataframe(df.describe(include=['object']),use_container_width=True)
            else:
                st.write('This Dataframe has no **Categorical** Features')    

        missing = st.checkbox('Show Missing Values',value=False)
        if missing:

            st.markdown("<h6 align='center'> Null Values",unsafe_allow_html=True)
            st.dataframe(df.isnull().sum().sort_values(ascending=False),height=350, use_container_width=True)

        #TODO Duplicated values


    with st.expander("Show EDA"):
        st.write('TODO')

    nLine()

    # Missing Values

    st.markdown('### ⚠️ Handling Missing Values', unsafe_allow_html=True)
    nLine()

    with st.expander('Show Missing Values'):
        
        nLine()
        # Input box
        col1,col2 = st.columns(2)
        with col1:
            missingCols = df.columns[df.isnull().any()].to_list()
            if missingCols:
                opts = ['All Numerical Features','All Categorical Features']

            else:
                opts = []

            fillFeatures = st.multiselect('Select Features', missingCols + opts, help='Select Features')

        with col2:
            strategy = st.selectbox('Select Strategy For Filling',['Select', 'Drop Rows', 'Drop Columns', 'Fill with Mean', 'Fill with Median','Fill with Mode (Most Frequent)'], help='Select Missing Values Strategy')

        if fillFeatures and strategy != 'Select':
            nLine()

            col1,col2,col3 = st.columns([1,0.5,1])
            if col2.button('Apply',use_container_width=True, key='missing_apply', help='Apply Missing Value Strategy'):

                progressBar()

                # All Numerical Features
                if 'All Numerical Features' in fillFeatures:
                    fillFeatures.remove('All Numerical Features')
                    fillFeatures += df.select_dtypes(include=[int,float]).columns.to_list()

                # All Categorical Features
                if 'All Categorical Features' in fillFeatures:
                    fillFeatures.remove('All Categorical Features')
                    fillFeatures += df.select_dtypes(include=object).columns.to_list()

                # Drop Rows
                if strategy == 'Drop Rows':
                    df = df.dropna(subset=fillFeatures)
                    st.session_state['df'] = df
                    st.success(f'Missing values have been dropped from the DataFrame for **{fillFeatures}**.')
                
                # Drop Columns
                if strategy == 'Drop Columns':
                    df = df.drop(columns=fillFeatures,axis=1)
                    st.session_state['df'] = df
                    st.success(f'The Columns **{fillFeatures}** have been dropped from the dataframe.')

                # Fill with Mean    
                if strategy == 'Fill with Mean':
                    imputer = SimpleImputer(strategy='mean')
                    df[fillFeatures] = imputer.fit_transform(df[fillFeatures])
                    st.session_state['df'] = df
                    st.success(f'The Column **{fillFeatures}** missing values has been filled with the **Mean** value.')

                # Fill with Median    
                if strategy == 'Fill with Median':
                    imputer = SimpleImputer(strategy='median')
                    df[fillFeatures] = imputer.fit_transform(df[fillFeatures])
                    st.session_state['df'] = df
                    st.success(f'The Column **{fillFeatures}** missing values has been filled with **Median** value.')

                # Fill with Mean    
                if strategy == 'Fill with Mode (Most Frequent)':
                    imputer = SimpleImputer(strategy='most_frequent')
                    df[fillFeatures] = imputer.fit_transform(df[fillFeatures])
                    st.session_state['df'] = df
                    st.success(f'The Column **{fillFeatures}** missing values has been filled with **Mode** value.')
                    
                    

                #TODO Multivariate imputation of Null values



        col1,col2,col3 = st.columns([0.15,1,0.15])
        col2.divider()
        col1,col2,col3 = st.columns([0.9,0.6,1])
        with col2:
            st.button('Show Dataframe',on_click = buttonClick)
        if st.session_state['showDfButton']:
            st.dataframe(df, use_container_width=True)



