import pandas as pd
import numpy as np
import tkinter.filedialog
import re
import random
import os
import csv
from datetime import datetime, timedelta
from tkinter import messagebox

def replace_special_character(text):
    if pd.isnull(text):
        return '""'
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    text = text.strip()
    return f'"{text}"'

def convert_date_format(date_str):
    # Try parsing the date using different possible formats
    # This list can be extended with other date formats if needed
    possible_formats = [
        "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%m-%d-%Y",
        "%Y/%m/%d", "%d %b %Y", "%b %d, %Y", "%Y.%m.%d", "%d.%m.%Y"
    ]
    for date_format in possible_formats:
        try:
            # Try to parse the date string
#             date_obj = datetime.strptime(date_str, date_format)
            # If successful, return the date in yyyy-mm-dd format
            return date_str.strftime("%Y-%m-%d")
        except ValueError:
            # If the format doesn't match, try the next one
            continue
    
    # If no format matches, raise an exception
    raise ValueError("Unrecognized date format")
    
def main():
    #get filepath
    filepath=tkinter.filedialog.askopenfilename()
    file_location = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    #read in the file
    if filepath.endswith('xls') or filepath.endswith('xlsx'):
        df=pd.read_excel(filepath)
    elif filepath.endswith('csv'):
        df=pd.read_csv(filepath)
    
    #get string and date column
    
    string_columns = list(df.select_dtypes(include='object').columns)
    datetime_columns = list(df.select_dtypes(include='datetime').columns)
    numeric_columns = list(df.select_dtypes(include='number').columns)
    
    #clean up these column
    for cols in string_columns:
        try:
            pd.to_datetime(df[cols], format="%Y-%m-%d")
            datetime_columns.append(cols)
        except:
            df[cols] = df[cols].astype('string').fillna('')
            df[cols] = df[cols].apply(replace_special_character)
    for cols in datetime_columns:
         df[cols] = pd.to_datetime(df[cols])
         df[cols] = df[cols].apply(convert_date_format)
    for cols in numeric_columns:
         df[cols] = pd.to_numeric(df[cols])
    
    #output result
    output_name = filename[:filename.find('.')]+'_cleaned.csv'
    output_path = file_location+'/'+output_name
    df.to_csv(path_or_buf = output_path,sep='|',index=False,quoting=csv.QUOTE_NONE)
    
    messagebox.showinfo('Info',f'file successfully stored at {output_path}.')
          
main()
