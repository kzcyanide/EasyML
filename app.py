import streamlit as st
import pandas as pd
import numpy as np

st.image("./assets/logo.png")
st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
def initSessionState():
    if 'df' not in st.session_state:
        st.session_state['df'] = None

initSessionState()

def nLine(n=1):
    for _ in range(n):
        st.write('\n')

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
            strategy = st.selectbox('Select Strategy For Filling',['Select', 'Drop Rows', 'Drop Columns', 'Fill with Mean', 'Fill with Median','Fill with Mode (Most Frequent)','Fill with ffill, bfill'], help='Select Missing Values Strategy')


