import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_folder = 'csv/'

# Get a list of CSV files in the folder
csv_files = glob.glob(csv_folder + '*.csv')
dfs=[]

# Check if any CSV files are found
if csv_files:
    for file in csv_files:
        # Load the CSV data into a pandas DataFrame
        df = pd.read_csv(file, skiprows=1)

        head_x = df['head'][1:].astype(float)  # Remove the first element and convert to float for plotting
        head_y = df['head.1'][1:].astype(float)  # Remove the first element and convert to float for plotting

        nose_x = df['nose'][1:].astype(float)  # Remove the first element and convert to float for plotting
        nose_y = df['nose.1'][1:].astype(float)  # Remove the first element and convert to float for plotting

        spine1_x = df['spine1'][1:].astype(float)  # Remove the first element and convert to float for plotting
        spine1_y = df['spine1.1'][1:].astype(float)  # Remove the first element and convert to float for plotting

        spine2_x = df['spine2'][1:].astype(float)  # Remove the first element and convert to float for plotting
        spine2_y = df['spine2.1'][1:].astype(float)  # Remove the first element and convert to float for plotting

        spine3_x = df['spine3'][1:].astype(float)  # Remove the first element and convert to float for plotting
        spine3_y = df['spine3.1'][1:].astype(float)  # Remove the first element and convert to float for plotting

        spine4_x = df['spine4'][1:].astype(float)  # Remove the first element and convert to float for plotting
        spine4_y = df['spine4.1'][1:].astype(float)  # Remove the first element and convert to float for plotting

        # Construct a dictionary with body parts coordinates
        bodyparts = {
            'head_x': head_x,
            'head_y': head_y,
            'nose_x': nose_x,
            'nose_y': nose_y,
            'spine1_x': spine1_x,
            'spine1_y': spine1_y,
            'spine2_x': spine2_x,
            'spine2_y': spine2_y,
            'spine3_x': spine3_x,
            'spine3_y': spine3_y,
            'spine4_x': spine4_x,
            'spine4_y': spine4_y,
        }
        
        # Perform additional processing or modification here
        filename = os.path.basename(file)
        
        # Split the string based on the underscore character
        parts = filename.split('.csv')[0].split('_')

        # Access the values at index 0 and 1
        name = parts[0]
        odorant = parts[1].split('DLC')[0]
    
        
        # Construct the object
        data_object = {
            'name': name,
            'odorant': odorant,
            'bodyparts': bodyparts
        }
        dfs.append(data_object)
        
# Dictionary to store grouped data objects
grouped_objects = {}

# Group data objects by odorant field
for df in dfs:
    odorant = df['odorant']
    if odorant not in grouped_objects:
        grouped_objects[odorant] = []
    grouped_objects[odorant].append(df)

##################################################
########## Populate Bodyparts Names Set ##########
##################################################

bp_names_set = set()  # Create an empty set

first_key = next(iter(grouped_objects))  # Get the first key
for bodypart in grouped_objects[first_key][0]['bodyparts']:
    common_name = bodypart[:-2]  # Extract common name by removing '_x' or '_y'
    bp_names_set.add(common_name)  # Add common name to the set

bp_names_set = sorted(bp_names_set)  # Sort the unique common names


#######################################################
########## Truncate based on FPS and minutes ##########
#######################################################

fps_count = 30
minutes = 3
max_size = fps_count*minutes*60

def truncate_series(series):
    '''
    if(len(series) < max_size):
        print(series.name)
        print('before ' + str(len(series)))
        print('after ' + str(len(series)))
    '''
    if len(series) > max_size:
        series = series.iloc[:max_size]  # Truncate the series
    return series

# Create a new dictionary to store truncated data objects grouped by odorant
truncated_grouped_objects = {}

# Loop through each data object
for obj in dfs:
    name = obj['name']
    odorant = obj['odorant']
    bodyparts = obj['bodyparts']
    
    # Create a new dictionary for the truncated data object
    truncated_obj = {
        'name': name,
        'odorant': odorant,
        'bodyparts': {}
    }
    
    # Truncate each series and store it in the new dictionary
    for key, value in bodyparts.items():
        truncated_obj['bodyparts'][key] = truncate_series(value)

    # Check if the odorant key exists in the new dictionary
    if odorant not in truncated_grouped_objects:
        truncated_grouped_objects[odorant] = []

    # Append the truncated data object to the list under the odorant key
    truncated_grouped_objects[odorant].append(truncated_obj)

grouped_objects = truncated_grouped_objects

################################
########## Strip NaNs ##########
################################

i = 0
for odorant, objects in grouped_objects.items():
    for obj in objects:
        for bp_name in bp_names_set:
            series_x = obj['bodyparts'][f"{bp_name}_x"]
            series_y = obj['bodyparts'][f"{bp_name}_y"]
            
            # print(str(len(series_x))+ ' ' + str(len(series_y)))
            
            nan_indices_x = series_x.index[series_x.isnull()]
            nan_indices_y = series_y.index[series_y.isnull()]
            # Indices in nan_indices_x that are not in nan_indices_y
            indices_only_in_x = nan_indices_x.difference(nan_indices_y)
            
            # Indices in nan_indices_y that are not in nan_indices_x
            indices_only_in_y = nan_indices_y.difference(nan_indices_x)
            
            # print("Indices in nan_indices_x not in nan_indices_y:", indices_only_in_x)
            # print("Indices in nan_indices_y not in nan_indices_x:", indices_only_in_y)
            
            #unique_indexes = set(nan_indices_x + nan_indices_y)
            
            # Combine unique indices from both x and y
            unique_indexes = set(nan_indices_x).union(nan_indices_y)
            
            # Ensure unique_indexes exist in series_x and series_y
            unique_indexes_x = unique_indexes.intersection(series_x.index)
            unique_indexes_y = unique_indexes.intersection(series_y.index)
            
            # Remove indexes in unique_indexes_x and unique_indexes_y from series_x and series_y
            cleaned_series_x = series_x.drop(index=unique_indexes_x)
            cleaned_series_y = series_y.drop(index=unique_indexes_y)
            
            # print(str(len(cleaned_series_x))+ ' ' + str(len(cleaned_series_y)))

            obj['bodyparts'][f"{bp_name}_x"] = cleaned_series_x
            obj['bodyparts'][f"{bp_name}_y"] = cleaned_series_y

            i = i + 1
            
####################################################
########## Outilier removal using z-score ##########
####################################################

def is_outlier(value, mean, std, threshold=3):
    z_score = np.abs((value - mean) / std)
    return z_score > threshold

i = 0
for odorant, objects in grouped_objects.items():
    for obj in objects:
        for bp_name in bp_names_set:
            series_x = pd.Series(obj['bodyparts'][f"{bp_name}_x"])
            series_y = pd.Series(obj['bodyparts'][f"{bp_name}_y"])
            mean_x = np.mean(series_x)
            mean_y = np.mean(series_y)
            std_x = np.std(series_x)
            std_y = np.std(series_y)
            
            # Ensure both series have the same length
            min_len = min(len(series_x), len(series_y))
            series_x = series_x[:min_len]
            series_y = series_y[:min_len]
            
            # Remove outliers
            mask = ~(series_x.apply(lambda x: is_outlier(x, mean_x, std_x)) | series_y.apply(lambda y: is_outlier(y, mean_y, std_y)))
            cleaned_series_x = series_x[mask]
            cleaned_series_y = series_y[mask]
            
            if len(cleaned_series_x) != len(cleaned_series_y):
                print(f"Length mismatch after outlier removal for obj {i}")
            
            obj['bodyparts'][f"{bp_name}_x"] = cleaned_series_x
            obj['bodyparts'][f"{bp_name}_y"] = cleaned_series_y
            i += 1