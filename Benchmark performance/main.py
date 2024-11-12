import pandas as pd
from cleaning_data_functions import MRC_data_parser,read_inputs
from filtering_data_functions import get_result,get_relevant_data
from save_filtered_data_to_csv import save_the_result_to_excel

# -------------------------Configuration--------------------------------
merged_dataframe = MRC_data_parser('All Countries.MRC', 'All Funds.MRC')
benchmark_excel_dataframe = pd.read_excel('Benchmark Performance.xlsx') 
additional_datapoints_file = 'file'


# get the row index 2 
index_arr = list(benchmark_excel_dataframe.iloc[0])[1:]
index_arr = [int(x) for x in index_arr]

# get the row index 3
currency_arr= list(benchmark_excel_dataframe.iloc[1])[1:]
currency_arr = [str(x).strip() for x in currency_arr if str(x) != 'nan']

print(index_arr)
print(currency_arr)
if len(index_arr) != len(currency_arr):
    print("Length of index array and currency array should be same")
    exit()
else:
    cleaned_data = get_relevant_data(merged_dataframe)
    filtered_data = get_result(index_arr,currency_arr,cleaned_data)
    print(filtered_data)
    try:
        save_the_result_to_excel(benchmark_excel_dataframe,filtered_data,additional_datapoints_file)
    except Exception as e:
        print("Error while saving the data to the benchmark file: ",e)
        exit()
