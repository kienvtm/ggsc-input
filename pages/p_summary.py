import streamlit as st
import duckdb
import pandas as pd
import datetime
from pathlib import Path
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
st.set_page_config(layout="wide")

# data folder path
cwd = Path(__file__).parent.parent

# daily file
dta_daily_path = cwd.joinpath('data.parquet')


db = duckdb.connect()
db.execute(f"CREATE or replace temp VIEW data_daily AS SELECT * FROM'{dta_daily_path}'")
# db.execute(f"CREATE or replace temp VIEW data_weekly AS SELECT * FROM '{dta_weekly_path}'")
# db.execute(f"CREATE or replace temp VIEW calendar AS SELECT * FROM '{calendar_path}'")

@st.cache_data
def get_data_daily():
    query = rf'''
        SELECT 
            *
        FROM data_daily 
        '''
    # st.write(query)
    df_data = db.execute(query).fetch_df()
    return df_data


# User authentication (simple version for demonstration)
@st.cache_data
def authenticate(username, password):
    user_data = {
        'ggghn': 'password1',
    }
    if username in user_data and user_data[username] == password:
        return True
    return False

# Function to manage the login process
def login():
    st.title('Summary')

    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')

    if st.sidebar.button('Login'):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f'Welcome, {username}!')
            st.rerun()
        else:
            st.error('Invalid username or password')


# Check if the user is already logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
    # st.rerun()
else:
    st.success(f'Logged in as {st.session_state["username"]}')
    # Logout button
    if st.sidebar.button('Logout'):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        st.rerun()

    data = get_data_daily()
    st.dataframe(data)