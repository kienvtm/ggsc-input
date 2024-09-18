import streamlit as st
import pygsheets
import toml
import pandas as pd
from google.oauth2.service_account import Credentials
import json
import tempfile

# Load the credentials from the TOML file
with open('.streamlit\secrets.toml', 'r') as file:
    secrets = toml.load(file)

credentials = secrets['service_account']

def _google_creds_as_file():
    temp = tempfile.NamedTemporaryFile()
    temp.write(json.dumps({
    "type": credentials["type"],
    "project_id": credentials["project_id"],
    "private_key_id": credentials["private_key_id"],
    "private_key": credentials["private_key"].replace('\\n', '\n'),  # Correct newline formatting
    "client_email": credentials["client_email"],
    "client_id": credentials["client_id"],
    "auth_uri": credentials["auth_uri"],
    "token_uri": credentials["token_uri"],
    "auth_provider_x509_cert_url": credentials["auth_provider_x509_cert_url"],
    "client_x509_cert_url": credentials["client_x509_cert_url"]
        }
    ).encode('utf-8'))
    temp.flush()
    return temp

# Convert the credentials to match the format required for service account
# service_account_info = {
#     "type": credentials["type"],
#     "project_id": credentials["project_id"],
#     "private_key_id": credentials["private_key_id"],
#     "private_key": credentials["private_key"].replace('\\n', '\n'),  # Correct newline formatting
#     "client_email": credentials["client_email"],
#     "client_id": credentials["client_id"],
#     "auth_uri": credentials["auth_uri"],
#     "token_uri": credentials["token_uri"],
#     "auth_provider_x509_cert_url": credentials["auth_provider_x509_cert_url"],
#     "client_x509_cert_url": credentials["client_x509_cert_url"]
# }
# st.write(service_account_info)

creds_file = _google_creds_as_file()



# Create the credentials object manually using google.oauth2.service_account
# credentials = Credentials.from_service_account_info(service_account_info)
# creds = Credentials(**service_account_info)

# Authorize pygsheets using the credentials object
client = pygsheets.authorize(service_account_file=creds_file.name)

# Open a Google Sheet by name or URL
spreadsheet = client.open('Your Google Sheet Name')

# Select the first worksheet
worksheet = spreadsheet.sheet1

# Sample DataFrame
df = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Item Code': ['A001', 'A002'],
    'Item Name': ['Item 1', 'Item 2'],
    'Price': [100, 150]
})

# Write DataFrame to the Google Sheet
worksheet.set_dataframe(df, (1, 1))  # Start writing from the first cell