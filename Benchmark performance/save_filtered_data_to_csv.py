import pandas as pd
from filtering_data_functions import get_data_from_file
def save_the_result_to_excel(df1,df2,file_name):
    # df1 is benchmark file
    # df2 is the file with the data to be added to the benchmark file
    # Convert the 'Calculation Date' from YYYYMMDD to YYYY-MM-DD HH:MM:SS format
    # df2['Calculation Date'] = df2['Calculation Date'].str.strip()
    # df2['Calculation Date'] = pd.to_datetime(df2['Calculation Date'], format='%Y%m%d').dt.strftime('%Y-%m-%d %H:%M:%S')

    # Add a new row after row 2 (after the row with 'DATE')
    new_row = {col: None for col in df1.columns}

    # Set the date for the new row based on dataframe 2 (now in correct format)
    new_row['Unnamed: 0'] = df2['Calculation Date'][0]  # Taking the formatted date from df2

    # Dynamically match the MSCI Index Codes from df2 with the columns in df1's 0th and 1st rows (for code and currency)
    for index, row in df2.iterrows():
        msci_code = row['MSCI Index Code']
        index_currency = row['Index Currency']

        # Find the column in df1 where both the 0th row matches the MSCI Index Code and the 1st row matches the Index Currency
        matching_column = df1.columns[(df1.iloc[0] == int(msci_code)) & (df1.iloc[1] == index_currency)].tolist()

        # If a matching column is found, fill in the new row with DTR Index Level [net]
        if matching_column:
            column_name = matching_column[0]  # Take the first match
            new_row[column_name] = row['DTR Index Level [net]']

    if (df1.loc[0] == 700750).any():
        # checking for the missing data point
        matching_column = df1.columns[(df1.iloc[0] == int(700750))].tolist()
        # store the data from file to the new row
        try:
            new_row[matching_column[0]] = list(get_data_from_file(file_name).values())[0]
        except Exception as e:
            print("Can not save the additional Datapoint to benchmark file because of the following error: ",e)
        print(new_row)
    
    # Insert the new row into df1 after the row with 'DATE' (which is index 2)
    df_final = pd.concat([df1.iloc[:3], pd.DataFrame([new_row]), df1.iloc[3:]]).reset_index(drop=True)

    # Display the updated dataframe
    df_final.head()
    df_final.to_csv('Benchmark Performance Updated.csv', index=False)
