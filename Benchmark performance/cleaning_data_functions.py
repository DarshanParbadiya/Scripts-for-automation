import pandas as pd

def read_inputs(file_name):
    # reading the inputs from the csv file
    inputs = pd.read_csv(file_name)
    index_arr = inputs['Index Code'].tolist()
    currency_arr = inputs['Currency'].tolist()
    return (index_arr,currency_arr)

# @EXPERIMENTAL
# This function tries to create the column names from the MRC file, But it is not accurate dut to missing commas in the file.
def get_column_names(file):
    with open(file, 'r') as file:
        lines = file.readlines()

    # Initialize an empty list to store the field names
    fields = []

    # Loop through the lines and extract field names
    for index,line in enumerate(lines):
        if index > 2 and index < 57:
            # Split the line by multiple spaces to get the field name
            parts = line.split("     ")
            # print(parts)
            # Check if line is non-empty and contains field information
            if len(parts) >= 2:
                # Add the field name (2nd or 3rd part) to the fields list
                field_name = " ".join(parts[0].split()[2:])
                fields.append(field_name)
    return fields
            


def clean_the_dataframe(data_frame):
    df1 = data_frame
    # Step 1: Convert current header to the first row
    df1.loc[-1] = df1.columns  # Add column names as a row at index -1
    df1.index = df1.index + 1  # Shift the index by 1
    df = df1.sort_index()  # Sort the index to place the new row at the top
    column_names = ['INDEX LEVEL FGN CURRENCY', 'Calculation Date', 'MSCI Index Code',
       'MSCI Index Name', 'Reserved 1', 'Reserved 2', 'ISO Country Symbol',
       'Region Code', 'Value Flag', 'Growth Flag', 'Small Cap Flag',
       'GICS Sector', 'GICS Industry Group', 'GICS Industry',
       'GICS Sub-industry', 'Number of Securities in Index', 'Index Currency',
       'Closing Mkt Cap in MM', 'Price Index Variant Type [std]',
       'Price Index Level [std]', 'DTR Index Variant Type [grs]',
       'DTR Index Level [grs]', 'DTR Index Variant Type [net]',
       'DTR Index Level [net]', 'Adjusted Mkt Cap in MM',
       'Initial Mkt Cap in MM', 'Initial Mkt Cap MM Next Day',
       'Index Divisor [std]', 'Index Divisor [std] Next Day',
       'Index Divisor [grs]', 'Index Divisor [grs] Next Day',
       'Index Divisor [net]', 'Index Divisor [net] Next Day',
       'Index Div Pts Final [grs/std]', 'Idx Div Pts ND Prel [grs/std]',
       'Index Div Pts Final [net/std]', 'Idx Div Pts ND Prel [net/std]',
       'Index Div Pts Final [grs/grs]', 'Idx Div Pts ND Prel [grs/grs]',
       'Index Div Pts Final [net/net]', 'Idx Div Pts ND Prel [net/net]',
       'Reserved 30', 'Reserved 31', 'Reserved 32', 'Reserved 33',
       'Reserved 34', 'Reserved 35', 'Reserved 36', 'Reserved 37',
       'Reserved 38', 'Reserved 39', 'Reserved 40', 'Reserved 41',
       'Reserved 42']
    names = ['INDEX LEVEL FGN CURRENCY', 'Calculation Date', 'MSCI Index Code', 
             'MSCI Index Name', 'Reserved 1', 'Reserved 2', 'ISO Country Symbol', 
             'Region Code', 'Value Flag', 'Growth Flag', 'Small Cap Flag', 
             'GICS Sector', 'GICS Industry Group', 'GICS Industry',
             'GICS Sub-industry', 'Number of Securities in Index', 'Index Currency', 
             'Closing Mkt Cap in MM', 'Price Index Variant Type [std] std_variant_type', 'Price Index Level [std]', 'DTR Index Variant Type [grs]', 'DTR Index Level [grs]', 'DTR Index Variant Type [net]', 'DTR Index Level [net]', 'Adjusted Mkt Cap in MM', 'Initial Mkt Cap in MM', 'Initial Mkt Cap MM Next Day', 'Index Divisor [std]', 'Index Divisor [std] Next Day', 'Index Divisor [grs]', 'Index Divisor [grs] Next Day', 'Index Divisor [net]', 'Index Divisor [net] Next Day', 'Index Div Pts Final [grs/std]', 'Idx Div Pts ND Prel [grs/std]', 'Index Div Pts Final [net/std]', 'Idx Div Pts ND Prel [net/std]', 'Index Div Pts Final [grs/grs]', 'Idx Div Pts ND Prel [grs/grs]', 'Index Div Pts Final [net/net]', 'Idx Div Pts ND Prel [net/net]', 'Reserved 30', 'Reserved 31', 'Reserved 32', 'Reserved 33', 'Reserved 34', 'Reserved 35', 'Reserved 36', 'Reserved 37', 'Reserved 38', 'Reserved 39', 'Reserved 40', 'Reserved 41', 'Reserved 42']

    # Step 2: Insert a new header
    new_header = column_names
    df1.columns = new_header

    # Verify the result
    return df1

def MRC_data_parser(file_path1, file_path2):
    # Specify the file path and line number of the header
    # file_path1 = "All Countries.MRC"
    # file_path2 = "All Funds.MRC"
    header_line = 60  # Since pandas uses zero-based indexing, header on line 58 means index 57

    # Read the file as a CSV
    df1 = pd.read_csv(file_path1, header=header_line,dtype=str)
    df2 = pd.read_csv(file_path2, header=header_line,dtype=str)
    df1_new = clean_the_dataframe(df1)
    df2_new = clean_the_dataframe(df2)
    final_df = pd.concat([df1_new, df2_new], axis=0,ignore_index=True)
    return final_df

