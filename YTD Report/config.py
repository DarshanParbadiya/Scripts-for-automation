import os
from datetime import datetime
# Get today's date
today_date = datetime.now()
# Format the date
formatted_date = today_date.strftime("%B %d, %Y")
class DynamicFileLocations():
    def __init__(self,base_path):
        
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
        self.report_file_name = os.path.join(base_path,'Final Report',f'YTD Report as of {formatted_date}.xlsx')
        
        self.pld_shareholder_file_path = os.path.join(base_path,'PLD Shareholding for a shareholder.xls')
        self.sales_support_file_name = os.path.join(base_path,'Final Report',f'Sales Support as of {formatted_date}.xlsx')
        # intermediate files
        self.save_intermediate_files = True
        
        # dealer codes
        self.update_dealer_codes = False
        self.update_rep_codes = True
        self.dealer_codes_sheet_name = 'Dealer Codes'
        
        # formatting options 
        self.PVT_Header_delimiter = ', '