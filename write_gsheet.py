import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Sheet1",
    ttl="10m",
)

# Print results.
st.dataframe(df)

if st.button("Update worksheet"):
    df = conn.update(
        worksheet="Example 1",
        data=df,
    )
    st.cache_data.clear()
    st.rerun()