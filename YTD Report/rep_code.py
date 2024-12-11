
import pandas as pd
from pld import filter_pld
from cibc import filter_cibc
from dealer import clear_and_update_sheet

def find_rep_codes_from_ivra(file_path):
    # file_path = 'IVRAUM003-BO-20241210-0900am.xls'
    # Read the specific sheet
    ivra = pd.read_excel(file_path)
    columns_to_keep = [36,39,40,45,48]

    # Filter the DataFrame using .iloc
    filtered_ivra = ivra.iloc[:, columns_to_keep]
    # Keep only rows with unique Rep Code values
    unique_rep_codes_df = filtered_ivra.drop_duplicates(subset=["REP CODE"])
    # unique_rep_codes_df["FULL NAME"] =  unique_rep_codes_df["REP FIRST NAME"] + " " + unique_rep_codes_df["REP LAST NAME"]

    unique_rep_codes_df["FULL NAME"] = (
        unique_rep_codes_df["REP FIRST NAME"].fillna("") + " " + unique_rep_codes_df["REP LAST NAME"].fillna("")
    )
    print('rep codes from ivra generated:',len(unique_rep_codes_df))
    unique_rep_codes_df.columns = unique_rep_codes_df.columns.str.strip()
    # unique_rep_codes_df.to_csv('ivra_rep_codes.csv', index=False)
    return unique_rep_codes_df

def find_rep_codes_from_pld(file_path):
    # file_path = 'PLD_Cumulative_Fund_Orders_Buy_Sells_12-06-2024.xls'
    # sheet_name = 'DEC'  # Replace with your desired sheet name

    # Read the specific sheet
    pld = pd.read_excel(file_path)
    columns_to_keep = [9, 10, 11]

    # Filter the DataFrame using .iloc
    filtered_pld = pld.iloc[:, columns_to_keep]

    # Optionally, set column names for visualization purposes
    filtered_pld.columns = [
        "REP FIRST NAME",
        "REP LAST NAME",
        "REP CODE",
        # "Account Name",
        # "Contact Address 1",
        # "Contact Address 2",
        # "REP CITY",
        # "Post/Zip Code",
        # "REP PROVINCE",
        # "Country"
    ]
    
    # Keep only rows with unique Rep Code values
    unique_rep_codes_df = filtered_pld.drop_duplicates(subset=["REP CODE"])
    unique_rep_codes_df["FULL NAME"] = unique_rep_codes_df["REP FIRST NAME"].fillna("") + " " + unique_rep_codes_df["REP LAST NAME"].fillna("")
    print('rep codes from pld generated:',len(unique_rep_codes_df))
    unique_rep_codes_df.columns = unique_rep_codes_df.columns.str.strip()
    return unique_rep_codes_df
    # unique_rep_codes_df.to_csv("pld_rep_codes.csv", index=False)

# @deprecated method
def combine_rep_codes(file_paths):
    # get the rep codes from the two files
    df_ivra = find_rep_codes_from_ivra(file_paths.ivra_path)

    df_pld = find_rep_codes_from_pld(file_paths.pld_path)
 
    # Read the specific sheet
    df = pd.read_excel(file_paths.Transaction_file_path, sheet_name=file_paths.old_sheet)
    
    # Keep only the specified columns from df_pld and df_ivra
    df_pld = df_pld[['REP CODE', 'FULL NAME']]
    df_ivra = df_ivra[['REP CODE', 'FULL NAME', 'REP CITY', 'REP PROVINCE']]

    concatenated_df = pd.concat([df, df_ivra,df_pld], axis=0)
    print('combined rep codes:',len(concatenated_df))
 
    unique_rep_codes_df = concatenated_df.drop_duplicates(subset=["REP CODE"])
    # Load the existing Excel file
    try:
        with pd.ExcelWriter(file_paths.Transaction_file_path, engine='openpyxl', mode='a') as writer:
            # Write the DataFrame to a new sheet
            unique_rep_codes_df.to_excel(writer, sheet_name=file_paths.new_sheet, index=False)
    except:
        print('can not create the sheet in the file, so creating a csv file')
        unique_rep_codes_df.to_csv(f'{file_paths.new_sheet}.csv', index=False)
    else:
        print(f'created {file_paths.new_sheet} sheet')

def update_rep_codes_sheet(file_paths):
    try:
        excel_file = pd.ExcelFile(file_paths.Transaction_file_path)
        sheet_name = file_paths.new_sheet
        unique_rep_codes = get_new_rep_codes(file_paths)
        if sheet_name in excel_file.sheet_names:
            print(f"Sheet '{sheet_name}' exists in the Excel file.")
            # read the existing sheet
            existing_rep_codes = pd.read_excel(file_paths.Transaction_file_path, sheet_name=file_paths.old_sheet)
            print(f'existing rep codes in {file_paths.old_sheet}:',len(existing_rep_codes))
            # append newly created dealer codes with existing codes
            updated_rep_codes = pd.concat([existing_rep_codes,unique_rep_codes],axis=0)
            updated_rep_codes = updated_rep_codes.drop_duplicates(subset='REP CODE')
            print(f'updated rep codes in {file_paths.old_sheet} and new ones:',len(updated_rep_codes))
            # Drop duplicate rows based on the 'DEALER CODE' column
            clear_and_update_sheet(file_paths, sheet_name, updated_rep_codes)
        else:
            print(f"Sheet '{sheet_name}' does not exist in the Excel file.")
            try:
                with pd.ExcelWriter(file_paths.Transaction_file_path, engine='openpyxl', mode='a') as writer:
                    unique_rep_codes.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Sheet '{sheet_name}' created in the Excel file.")
            except:
                print('can not create the sheet in the file, so creating a csv file')
    except Exception as e:
        print('error:',e)
        print('can not update the rep codes sheet')
        

def get_new_rep_codes(file_paths):
    df_ivra = find_rep_codes_from_ivra(file_paths.ivra_path)
    df_pld = find_rep_codes_from_pld(file_paths.pld_path)
    
    # Keep only the specified columns from df_pld and df_ivra
    df_pld = df_pld[['REP CODE', 'FULL NAME']]
    df_ivra = df_ivra[['REP CODE', 'FULL NAME', 'REP CITY', 'REP PROVINCE']]
    concatenated_df = pd.concat([df_ivra,df_pld], axis=0)
    unique_rep_codes_df = concatenated_df.drop_duplicates(subset=["REP CODE"])
    return unique_rep_codes_df

# does the xlookup of the rep codes with the names
def map_the_rep_codes(file_paths):
    
    codes = pd.read_excel(file_paths.Transaction_file_path, sheet_name=file_paths.new_sheet)
    pld = filter_pld(file_paths)
    cibc = filter_cibc(file_paths)
    pld.rename(columns={'Rep  Code': 'REP CODE'}, inplace=True)
    # Merge the DataFrames on 'REP CODE' column
    cibc['REP CODE'] = cibc['REP CODE'].astype(str).str.strip().str.upper()
    pld['REP CODE'] = pld['REP CODE'].astype(str).str.strip().str.upper()
    codes['REP CODE'] = codes['REP CODE'].astype(str).str.strip().str.upper()
    
    merged_df_cibc = pd.merge(cibc, codes[['REP CODE', 'FULL NAME', 'REP CITY', 'REP PROVINCE']], on='REP CODE', how='left')
    merged_df_pld = pd.merge(pld, codes[['REP CODE', 'FULL NAME', 'REP CITY', 'REP PROVINCE']], on='REP CODE', how='left')

    if file_paths.save_intermediate_files:
        merged_df_cibc.to_csv(file_paths.cibc_with_rep_code_file_name, index=False)
        merged_df_pld.to_csv(file_paths.pld_with_rep_code_file_name, index=False)
        print('saved Files with REP names mapping')
    return merged_df_cibc,merged_df_pld