from os import chdir, lstat

import pandas as pd
from pandas import DataFrame, read_excel
import os
import openpyxl
from openpyxl import load_workbook
from configparser import ConfigParser

# os.chdir(r'/input_files/')
# config = ConfigParser("PHM01_Test_New.ini")
# os.getcwd()

# def report_var(parameters):
# #     # config.read('PHM01_Test_New.ini')
input_var = f'/Users/reinaldoburgos/sources/My_Space/my_projects/PHM01_Test/input_files' #"file_input_path"
input_file_path: str=f'{input_var}/PHM01_Report_filled_20251229_040547.xlsx'
output_var = "file_output_path"

print(input_var)
print(input_file_path)

#


#df_input = pd.read_excel(input_file_path)




