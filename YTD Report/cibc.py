import pandas as pd

def filter_cibc(file_paths):
    # file_path = 'CIBC BPO Reporting of Unitholder Activity 2024.xlsx'
    # cibc_save_file_name = 'final_cibc.csv'
    # O:\Products\Fund Oversight\Unitrax Transaction Listings\2024
    cibc = pd.read_excel(file_paths.cibc_path)

    cibc['TRADE DATE'] = pd.to_datetime(cibc['TRADE DATE'], format='%Y%m%d')

    # Adjust the index to start from 2
    cibc.index = pd.Index(cibc.index + 2)


    filtered_df = cibc[(cibc['TRADE DATE'].dt.year == 2024) & (cibc['UNIT AMT'] > 0)]

    final_cibc = filtered_df[filtered_df['TRANS TYPE'].isin(['BUY', 'SEL', 'INC'])]
    # final_cibc.to_csv('temp.csv', index=True)
    if file_paths.save_intermediate_files:
        final_cibc.to_csv(file_paths.cibc_save_file_name, index=True)
        print(f'created filtered CIBC {len(final_cibc)}')
    
    return final_cibc