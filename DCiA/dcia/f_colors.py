#load colors for the nodes
import pandas as pd
import random
def interpolate_color(color1, color2, factor):
    """ Interpolate between two RGB colors """
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    return (r, g, b)

def number_to_rgb_gradient(number, min_val, max_val,csv):
    """ Convert number to RGB gradient """
    normalized_value = (number - min_val) / (max_val - min_val)
    if csv==1:
        color1 = (255,255,0)  # Lightest color (white)
        color2 = (255,0,0)  # Brightest color (red)

    if csv==2:
        color1 = (0,255,255) # Lightest color (blue)
        color2 = (0, 0, 110)  # Brightest color (dark blue)
    return interpolate_color(color1, color2, normalized_value)

def check_data_types(df):
    data_types = {}

    for column in df.columns:
        dtype = df[column].dtype
        if column !='Node_Size' and column !='index':
            # Check if the column contains categorical data
            if pd.api.types.is_categorical_dtype(dtype):
                if df[column].nunique()<3:
                    data_types[column] = 'Categorical'
            # Check if the column contains binary data
            elif df[column].nunique() == 2 and pd.api.types.is_numeric_dtype(dtype):
                data_types[column] = 'Binary'
            # Check if the column contains integer data
            elif pd.api.types.is_integer_dtype(dtype):
                if df[column].nunique()<3:
                    data_types[column] = 'Low_Integer'
                else:
                    data_types[column] = 'High_Integer'
            # Check if the column contains real (floating-point) data
            elif pd.api.types.is_float_dtype(dtype):
                    data_types[column] = 'Real'
            # If none of the above conditions are met, categorize the data type as 'Other'
            else:
                if df[column].nunique()<7:
                    data_types[column] = 'Other'

    return data_types

def get_colors(df,column,datatype):
    colourlist=  ['red','yellow','orange','black']
    if datatype=='Binary':
        df.loc[df[column].isin([0, 2]) , 'color'] = 'yellow'
        df.loc[df[column]==1 , 'color'] = 'red'
    elif datatype=='Other'or datatype=='Low_Integer' or datatype=='Categorical':
        color_mapping = {}
        unique_values = df[column].unique()
        for i, value in enumerate(unique_values):
            color_mapping[value] = colourlist[i % len(colourlist)]
        # Map colors to each row based on the 'Type' column
        df['color'] = df[column].map(color_mapping)
    
    elif datatype=='High_Integer' or datatype=='Real':
        min_val = min(df[column])
        max_val = max(df[column])
        rgb_gradients = [number_to_rgb_gradient(num, min_val, max_val,1) for num in df[column]]
        df['color'] = rgb_gradients
    return df

def get_colors2(df,column,datatype):
    colourlist=  ['cyan','purple''green','blue']
    if datatype=='Binary':
        df.loc[df[column].isin([0, 2]) , 'color'] = 'green'
        df.loc[df[column]==1 , 'color'] = 'cyan'
    elif datatype=='Other' or datatype=='Low_Integer' or datatype=='Categorical':
        color_mapping = {}
        unique_values = df[column].unique()
        for i, value in enumerate(unique_values):
            color_mapping[value] = colourlist[i % len(colourlist)]
        # Map colors to each row based on the 'Type' column
        df['color'] = df[column].map(color_mapping)
    
    elif datatype=='High_Integer' or datatype=='Real':
        min_val = min(df[column])
        max_val = max(df[column])
        rgb_gradients = [number_to_rgb_gradient(num, min_val, max_val,2) for num in df[column]]
        df['color'] = rgb_gradients
    return df
