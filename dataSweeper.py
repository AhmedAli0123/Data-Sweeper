import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Streamlit Page Config
st.set_page_config(page_title='Data Sweeper', layout='wide')
st.title('📊 Data Sweeper Created By Ahmed Ali')

st.write('Upload your CSV or Excel files for quick analysis, visualization, and conversion!')

# File Uploader
uploaded_files = st.file_uploader('Upload your files:', type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1].lower()  # Extract file extension
        
        # Load Data Based on File Type
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error(f'Unsupported file type: {file_ext}')
            continue
        
        # Display File Info
        st.subheader(f'📂 {file.name}')
        st.write(f'**Size:** {file.size / 1024:.2f} KB')
        
        # Show Data in a Table with Filters
        st.subheader('🔍 Data Preview')
        st.dataframe(df)  # Display the data
        
        # Add Search Bar for Filtering
        search_query = st.text_input(f'Search in {file.name}:')
        if search_query:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.dataframe(filtered_df)
        
        # Convert Data Format
        st.subheader('🔄 Convert File Format')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)
        
        if st.button(f'Convert {file.name}'):  # Conversion Button
            new_file_name = file.name.rsplit('.', 1)[0]  # Remove original extension
            buffer = BytesIO()
            
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                new_file_name += '.csv'
                mime_type = 'text/csv'
            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False, engine='openpyxl')
                new_file_name += '.xlsx'
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            buffer.seek(0)  # Reset Buffer Position
            
            st.download_button(
                label=f'⬇ Download {new_file_name}',
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

st.success('✅ Ready to clean and convert your data!')
