from cleaning_data_functions import MRC_data_parser
import pandas as pd

def get_relevant_data(df):
    # Select only the relevant columns
    df_final = df[['Calculation Date','DTR Index Level [net]']]
    df_final['Index Currency'] = df['Index Currency'].str.strip()
    df_final['MSCI Index Code'] = df['MSCI Index Code'].str.strip()
    return df_final

# Using msci_code and currency as input, find the index of the row
def find_index(df, msci_code, currency):
        # Boolean indexing to match the conditions
        condition = (df['MSCI Index Code'] == msci_code) & (df['Index Currency'] == currency)
        index_list = df.index[condition].tolist()
        return index_list if index_list else "No matching row found"

# This function takes in the index_arr, currency_arr, and the dataframe and returns the filtered rows from combined MRC files.
def get_result(index_arr, currency_arr,df):
    # Initialize an empty dataframe or list for results
    result = pd.DataFrame()  # Assuming you want to store rows in a dataframe
    output_index_list = []

    # Iterate over index and currency arrays
    for i in range(len(index_arr)):
        print("Index Code: ", index_arr[i])
        print("Currency: ", currency_arr[i])
        
        # Get the index using find_index function
        index_position = find_index(df, str(index_arr[i]), currency_arr[i])
        
        # Store the index in output_index_list
        output_index_list.append(index_position)
        
        # Check if a valid index was found
        if index_position != "No matching row found":
            # Retrieve the row and concatenate it to the result dataframe
            result = pd.concat([result, df.loc[index_position]], ignore_index=True)

    # Print the list of found indices
    print(output_index_list)
    result['Calculation Date'] = result['Calculation Date'].str.strip()
    result['Calculation Date'] = pd.to_datetime(result['Calculation Date'], format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')

    # Display the resulting dataframe
    return result


# function to get data for the 700750 index 
def get_data_from_file(file_path, start_index = 59, nrows = 3):
    df = pd.read_csv(file_path, delimiter = '|', skiprows=start_index,nrows=3, header=None)
    value = {str(df[1][1]).strip() : float(df[24][1])}
    return value


# usage
# index_arr  = [899902,984000,984000,106819,106805,700750]
# currency_arr = ['CAD','USD','CAD','CAD','CAD','CAD']
# df = MRC_data_parser('All Countries.MRC', 'All Funds.MRC')
# result = get_result(index_arr, currency_arr, get_relevent_data(df))
# result.head()