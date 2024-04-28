import pandas as pd
import yaml
import os
import csv

# Define the directory paths
h5_directory = 'h5'  # Directory containing HDF5 files
csv_directory = 'csv'  # Directory to save CSV files

# Create the CSV directory if it doesn't exist
os.makedirs(csv_directory, exist_ok=True)

# Body parts to rename
bodyparts_to_rename = [
    ('left_ear', 'left ear'),
    ('right_ear', 'right ear'),
    ('neck', 'spine1'),
    ('mouse_center', 'spine2'),
    ('mid_backend2', 'spine3'),
    ('tail_base', 'spine4'),
    ('tail_end', 'tail'),
    ('head_midpoint', 'head')
]

# Load the YAML file
file_paths = ['config.yaml', 'config.yml']

for file_path in file_paths:
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            break  # Break the loop if configuration is loaded successfully
    except FileNotFoundError:
        continue  # Continue to the next file if the current one doesn't exist
else:
    print("No configuration file found.")

# Extract body parts from the config
bodyparts = config['bodyparts']

# Cleanup CSV folder
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        os.remove(os.path.join(csv_directory, filename))

# Function to process a single HDF5 file
def process_h5_file(file_path):
    def rename_bodypart(bodypart):
        for original_name, new_name in bodyparts_to_rename:
            if bodypart == original_name:
                return new_name
        return bodypart
    
    # Read HDF5 file
    df = pd.read_hdf(file_path)
    
    # Rename body parts in the DataFrame columns
    new_index = [(scorer, rename_bodypart(bodypart), coords) for scorer, bodypart, coords in df.columns]
    new_columns = pd.MultiIndex.from_tuples(new_index, names=df.columns.names)
    df.columns = new_columns
    
    # Drop columns not in the bodyparts list
    for col in df.columns:
        if col[1] not in bodyparts:
            df.drop(columns=[col], inplace=True)
    
    # Extract file name and remove extension
    file_name = os.path.basename(file_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    
    # Construct new CSV file path
    new_csv_path = os.path.join(csv_directory, f'tmp_{file_name_no_ext}.csv')
    
    # Save DataFrame to CSV
    df.to_csv(new_csv_path, index=False)

def process_csv_files(file_path):
    def custom_key(item):
        second_value_index = bodyparts.index(item[1])
        third_value_index = order_third_value.index(item[2])
        return (second_value_index, third_value_index)

    def read_csv(filename):
        matrix = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # Read the header to get column names
            header = next(reader)
            # Initialize matrix with header names as the first value
            matrix = [[col] for col in header]
            
            # Read the rest of the rows
            for row in reader:
                for i, value in enumerate(row):
                    matrix[i].append(value)
        return matrix
    
    def write_csv(matrix, filename):
        new_csv_path = filename.replace("tmp_", "")
        # Write the sorted matrix to a CSV file
        with open(new_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            transposed_matrix = list(zip(*matrix))
            for row in transposed_matrix:
                    writer.writerow(row)

    def push_heading_row(matrix):
            # New array to add
            new_array = ['scorer', 'bodyparts', 'coords']
            # Get the maximum size of arrays
            max_size = max(len(row) for row in matrix) - 3
            # Iterate over max_size and construct strings
            for i in range(max_size):
                # Format the number with leading zeros
                frame_str = "frame{:04d}".format(i)
                # Append the formatted string to new_array
                new_array.append(frame_str)
            # Shift all elements down by one row
            matrix.insert(0, new_array)

    # Define the order for the third value
    order_third_value = ['x', 'y', 'likelihood']
    
    # Read the csv and store it in a matrix
    original_matrix = read_csv(file_path)
    
    # Sort the matrix using the custom key function
    sorted_matrix = sorted(original_matrix, key=custom_key)
    
    # Add as position 0 in the matrix an array containing keys 'scorer', 'bodyparts', 'coords' and the frame name    
    push_heading_row(sorted_matrix)
    
    # Write the matrix in a csv file by transposing the matrix    
    write_csv(sorted_matrix, file_path)
    
    # Remove tmp file
    os.remove(file_path)

# Iterate over HDF5 files in the directory
for filename in os.listdir(h5_directory):
    if filename.endswith('.h5'):
        h5_file_path = os.path.join(h5_directory, filename)
        process_h5_file(h5_file_path)
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(csv_directory, filename)
        process_csv_files(csv_file_path)