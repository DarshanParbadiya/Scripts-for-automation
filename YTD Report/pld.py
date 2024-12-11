import pandas as pd

def filter_pld(file_paths):
    # file_path = 'PLD_Cumulative_Fund_Orders_Buy_Sells_12-06-2024.xls'
    # pld_save_file_name = 'final_pld.csv'
    pld = pd.read_excel(file_paths.pld_path)
    pld.columns = pld.columns.str.replace('\n', ' ').str.strip()
    pld['Enter Date'] = pd.to_datetime(pld['Enter Date'])
    # Filter rows based on the year 2022
    filtered_pld = pld[pld['Enter Date'].dt.year == 2024]
    columns = filtered_pld.columns
    # filtered_pld[columns[2]].unique()
    final_pld = filtered_pld[filtered_pld[columns[2]].isin(['Buy', 'Sell'])]
    if file_paths.save_intermediate_files:
        final_pld.to_csv(file_paths.pld_save_file_name, index=True)
        print(f'created filtered PLD file {len(final_pld)}')
        
    return final_pld