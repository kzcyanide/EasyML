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

    st.markdown('### Exploratory Data Analysis')
    nLine()
    with st.expander("EDA"):
        nLine()

        head = st.checkbox('Show 5 Samples ',value = False)
        if head:
            nLine()
            st.dataframe(df.sample(5), use_container_width=True)
        shape = st.checkbox('Show Shape',value=False)
        if shape:
            st.write(f'This Dataframe has **{df.shape[0]} rows** and **{df.shape[1]} columns**')    

   


