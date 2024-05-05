import pandas as pd
import glob
import os

# Path to the CSV subfolder
csv_folder = 'csv/'

def pandas():
    # List all CSV files in the subfolder
    csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))

    processed_dfs = []

    for file in csv_files:
        df = pd.read_csv(file)
        
        # Perform additional processing or modification here
        filename = os.path.basename(file)
        
        # Split the string based on the underscore character
        parts = filename.split('.csv')[0].split('_')

        # Access the values at index 0 and 1
        name = parts[0]
        odorant = parts[1].split('DLC')[0]
        
        df['Name'] = name # Add name as a new column
        df['Odorant'] = odorant # Add odorant as a new column
        
        processed_dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    merged_df = pd.concat(processed_dfs, ignore_index=True)

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv('merged_file.csv', index=True)
    
pandas()