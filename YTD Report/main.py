import pandas as pd
from rep_code import combine_rep_codes,map_the_rep_codes,update_rep_codes_sheet
from ytd_report import generate_YTD_report
import os
from dealer import update_dealer_codes_sheet,map_dealer_codes
from verification import verify_files
from config import DynamicFileLocations
from sales_support import generate_sales_support
base_path = r'C:\Users\dparbadiya\OneDrive - AIC Global Holdings\Desktop\YTD Report Files'
def validate_paths(*args):
    for path in args:
        if not os.path.exists(path):
            print(f"Path {path} does not exist.")
            exit()
try:
    validate_paths(os.path.join(base_path,'Intermediate files'))
except:
    os.mkdir(os.path.join(base_path,'Intermediate files'))
try:
    validate_paths(os.path.join(base_path,'Final Report'))
except:
    os.mkdir(os.path.join(base_path,'Final Report'))
     
file_paths = DynamicFileLocations(base_path)

if __name__ == '__main__':
    
    is_verified = verify_files(
    file_paths.Transaction_file_path,
    file_paths.cibc_path,
    file_paths.pld_path,
    file_paths.ivra_path)

    if is_verified:
        if file_paths.update_dealer_codes:
            update_dealer_codes_sheet(file_paths)
        if file_paths.update_rep_codes:
            update_rep_codes_sheet(file_paths)
        try:
            generate_YTD_report(file_paths)
            generate_sales_support(file_paths)
        except Exception as e:
            print('Error while generating YTD report:',e)
