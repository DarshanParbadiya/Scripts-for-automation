import pandas as pd
def generate_sales_support(file_paths):
    try:
        pld = pd.read_excel(file_paths.pld_shareholder_file_path)
        # pld.columns = pld.columns.str.replace('\n', ' ').str.strip()
        pld_filtered = pld[['COMPANY_NAME','cost','nav_value','agent_external_code','dealer']]
        pld_filtered.columns = ['FUND NAME','BOOK VALUE','MARKET VALUE','REP CODE','DEALER NAME']
        codes = pd.read_excel(file_paths.Transaction_file_path, sheet_name=file_paths.new_sheet)
        merged_df = pd.merge(pld_filtered, codes[['REP CODE', 'FULL NAME']], on='REP CODE', how='left')
        merged_df['REP CODE'] = merged_df['REP CODE'].astype(str).str.strip().str.upper()
        merged_df.rename(columns={'FULL NAME':'REP FULL NAME'}, inplace=True)
        # SAVE THE SALES SUPPORT FILE
        merged_df.to_excel(file_paths.sales_support_file_name, index=False, engine='openpyxl')
        print('Sales Support file generated:',len(merged_df))
    except Exception as e:
        print('Error in generating Sales Support file:', e)
        return False