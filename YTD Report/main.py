import pandas as pd
from rep_code import combine_rep_codes,map_the_rep_codes,update_rep_codes_sheet
from ytd_report import generate_YTD_report
import os
from dealer import get_the_dealer_mapping_pld,map_dealer_codes
from verification import verify_files
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
    
class DynamicFileLocations():
    def __init__(self):
        
        self.Transaction_file_path = os.path.join(base_path,'Transaction Support Master file.xlsx')
        self.old_sheet = 'DEC'  # Replace with your desired sheet name
        self.new_sheet = 'Lastest'
         
        self.cibc_path = os.path.join(base_path,'CIBC BPO Reporting of Unitholder Activity 2024.xlsx')
        self.pld_path = os.path.join(base_path,'PLD_Cumulative_Fund_Orders_Buy_Sells.xls')
        self.save_intermediate_files_path = os.path.join(base_path,'Intermediate files')
        self.cibc_save_file_name = os.path.join(base_path,'Intermediate files','filtered_cibc.csv')
        self.pld_save_file_name = os.path.join(base_path,'Intermediate files','filtered_pld.csv')
        self.cibc_with_rep_code_file_name = os.path.join(base_path,'Intermediate files','filtered_cibc_with_rep_name.csv')
        self.pld_with_rep_code_file_name = os.path.join(base_path,'Intermediate files','filtered_pld_with_rep_name.csv')
        
        self.ivra_path = os.path.join(base_path,'IVRAUM003-BO-20241210-0900am.xls')
        self.report_file_name = os.path.join(base_path,'Final Report','final_report_YTD.xlsx')
        
        # intermediate files
        self.save_intermediate_files = True
        # dealer codes
        self.update_dealer_codes = False
        self.update_rep_codes = False
        self.dealer_codes_sheet_name = 'Dealer Codes'
        
        # formatting options 
        self.PVT_Header_delimiter = ', '
        
file_paths = DynamicFileLocations()

# combine_rep_codes(file_paths)
# generate_YTD_report(file_paths)
if __name__ == '__main__':
    
    is_verified = verify_files(
    file_paths.Transaction_file_path,
    file_paths.cibc_path,
    file_paths.pld_path,
    file_paths.ivra_path)

    if is_verified:
        if file_paths.update_dealer_codes:
            get_the_dealer_mapping_pld(file_paths)
        if file_paths.update_rep_codes:
            update_rep_codes_sheet(file_paths)
        try:
            generate_YTD_report(file_paths)
        except Exception as e:
            print('Error while generating YTD report:',e)
