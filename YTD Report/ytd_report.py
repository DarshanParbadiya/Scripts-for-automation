
import pandas as pd
from rep_code import combine_rep_codes,map_the_rep_codes
from dealer import map_dealer_codes
def generate_YTD_report(file_paths):
    # # Read the specific sheet
    # df = pd.read_excel(file_paths.Transaction_file_path, sheet_name=file_paths.new_sheet)
    # cibc = pd.read_csv(file_paths.cibc_with_rep_code_file_name)
    # pld = pd.read_csv(file_paths.pld_with_rep_code_file_name)
    cibc,pld = map_the_rep_codes(file_paths)
    cibc.columns = cibc.columns.str.upper()
    pld.columns =  pld.columns.str.upper()

    # cibc, pld = map_the_rep_codes(file_paths)
    # columns_to_keep_pld = ['FULL NAME', 'REP CITY', 'REP PROVINCE', 'GROSS AMT', 'NET AMT', 'FUND NAME', 'TRANS TYPE']
    columns_to_keep_pld = [0,2,5,7,13,38,39,40]

    # # Filter the DataFrame using .iloc
    filtered_pld = pld.iloc[:, columns_to_keep_pld]
    filtered_pld.columns = ['FUND NAME', 'FUND TRANSACTION TYPE', 'GROSS AMOUNT', 'NET AMOUNT','DEALER CODE', 'FULL NAME', 'REP CITY', 'REP PROVINCE']

    columns_to_keep_cibc = ['FULL NAME', 'REP CITY', 'REP PROVINCE', 'GROSS AMT', 'NET AMT', 'FUND NAME', 'TRANS TYPE','DEALER CODE']

    # Select the columns from the cibc DataFrame
    filtered_cibc = cibc[columns_to_keep_cibc]


    # Rename columns in 'filtered_pld' to match 'filtered_cibc'
    filtered_pld.rename(columns={
        'FUND TRANSACTION TYPE': 'TRANS TYPE',
        'GROSS AMOUNT': 'GROSS AMT',
        'NET AMOUNT': 'NET AMT'
    }, inplace=True)

    print('CIBC:',len(filtered_cibc))
    print('PLD:',len(filtered_pld))
    
    # if file_paths.save_intermediate_files:
    #     filtered_cibc.to_csv(file_paths.save_intermediate_files_path+'/temp_cibc.csv', index=False)
    #     filtered_pld.to_csv(file_paths.save_intermediate_files_path+'/temp_pld.csv', index=False)
    
    combined_df = pd.concat([filtered_cibc, filtered_pld], ignore_index=True)
    
    combined_df = map_dealer_codes(file_paths,combined_df)
    
    combined_df['PVT Header'] = (combined_df['FULL NAME'].fillna('') + file_paths.PVT_Header_delimiter +
                                combined_df['REP CITY'].fillna('') + file_paths.PVT_Header_delimiter +
                                combined_df['REP PROVINCE'].fillna('')+ file_paths.PVT_Header_delimiter +
                                combined_df['DEALER NAME'].fillna('')).str.upper()
                                
                        
    combined_df.to_excel(file_paths.report_file_name, index=False, engine='openpyxl')
    print('YTD report generated:',len(combined_df))