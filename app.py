import streamlit as st
import pandas as pd
import os
from io import BytesIO 

# Set up our app
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and formatting capabilities.")

upload_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for uploaded_file in upload_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()  # Fixed the error

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display info about the file
        st.write(f"File Name: {uploaded_file.name}")
        st.write(f"File Size: {uploaded_file.size / 1024:.2f} KB")

        # Show 5 rows of our df
        st.write("Preview the head of the dataframe")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {uploaded_file.name}"):
            # Cleaning options
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

            # Choose specific columns to keep or convert
            st.subheader("Select Columns to Convert")
            columns = st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Create some visualizations
            st.subheader("Data Visualization")
            if st.checkbox(f"Show Visualization for {uploaded_file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Convert the File -> CSV to Excel
            st.subheader("Conversion Options")
            conversion_type = st.radio(f"Convert {uploaded_file.name} to:", ["CSV", "Excel"], key=uploaded_file.name)
            if st.button(f"Convert {uploaded_file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = uploaded_file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                    
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = uploaded_file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                # Download button 
                st.download_button(
                    label=f"Download {file_name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type  
                )

st.success("All files processed")
