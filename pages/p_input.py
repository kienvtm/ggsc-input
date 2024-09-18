import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

# Define initial columns for the table
columns = ["Date", "Item Code", "Item Name", "Price"]

# Initialize session state to store the rows
if "rows" not in st.session_state:
    st.session_state["rows"] = []


# Function to add new row
def add_row():
    st.session_state["rows"].append(
        {
            "MST":mst,
            "Date": datetime.now().date(), 
            "Item Code": "", 
            "Item Name": "", 
            "Price": 0
            }
        )

# Function to save the data to CSV
def save_to_csv():
    df = pd.DataFrame(st.session_state["rows"])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    df.to_parquet('data.parquet', index=False)
    # df.to_csv('data.csv', index=False)
    st.download_button(label="Download CSV", data=csv_buffer.getvalue(), file_name="data.csv", mime="text/csv")

# Display a button to add a new row
st.button("Add Row", on_click=add_row)

# Validation flag
validation_error = False

# If there are rows, display them as inputs
if st.session_state["rows"]:
    mst = st.text_input(label='Ma so thue')
    for idx, row in enumerate(st.session_state["rows"]):
        col1, col2, col3, col4 = st.columns(4)
        st.session_state["rows"][idx]["Date"] = col1.date_input(f"Date {idx+1}", value='today')
        st.session_state["rows"][idx]["Item Code"] = col2.text_input(f"Item Code {idx+1}", value=row["Item Code"])
        st.session_state["rows"][idx]["Item Name"] = col3.text_input(f"Item Name {idx+1}", value=row["Item Name"])
        st.session_state["rows"][idx]["Price"] = col4.number_input(f"Price {idx+1}", value=float(row["Price"] if row["Price"] else 0), min_value=0.0, step=1.0)
        st.session_state["rows"][idx]["MST"] = mst
        
        # Check if any field is blank
        if not st.session_state["rows"][idx]["Item Code"] or not st.session_state["rows"][idx]["Item Name"] or st.session_state["rows"][idx]["Price"] == 0 or not st.session_state["rows"][idx]["MST"]:
            validation_error = True

# Submit button to save data to CSV
if st.button("Submit"):
    if validation_error:
        st.warning("All fields must be filled in. Please check for blank values.")
    else:
        save_to_csv()
