# import streamlit as st
# from streamlit_gsheets import GSheetsConnection

# # Create a connection object.
# conn = st.connection("gsheets", type=GSheetsConnection)

# df = conn.read(
#     worksheet="Sheet1",
#     ttl="10m",
# )

# # Print results.
# st.dataframe(df)

# if st.button("Update worksheet"):
#     df = conn.update(
#         worksheet="Example 1",
#         data=df,
#     )
#     st.cache_data.clear()
#     st.rerun()

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)


# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(key, sheet_name="Sheet1"):
    sh = client.open_by_key(key)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    return df

def update_data(worksheet, df):
    # Find the first non-blank row by checking the length of the sheet
    sh = client.open_by_key(key)
    worksheet = sh.worksheet(worksheet)
    str_list = list(filter(None, worksheet.col_values(1)))
    first_empty_row = len(str_list) + 1
    set_with_dataframe(worksheet, df, row=first_empty_row, col=1, include_index=False, include_column_header=False)

key = '1EDxslX9zP0UV2ntj0RE9fb-o6uZaSodkW_e9b0nV5uQ'
df = load_data(key, sheet_name='Sheet1')
st.dataframe(df)

sheet_name='Example 1'
if st.button("Update worksheet"):
    update_data(sheet_name, df)
    st.cache_data.clear()
    st.rerun()