################################# IMPORT PACKAGES ################################

import pandas as pd

################################# MAIN CODE ################################

def interpolate_color(color1, color2, factor):
    """
    Interpolate between two RGB colors based on a factor.

    Parameters:
        color1 (tuple): The first RGB color as a tuple (R, G, B).
        color2 (tuple): The second RGB color as a tuple (R, G, B).
        factor (float): The interpolation factor (0.0 to 1.0).

    Returns:
        str: A string representing the interpolated RGB color.
    """
    
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    return f'rgb({r}, {g}, {b})'

def number_to_rgb_gradient(number, min_val, max_val, csv):
    """
    Convert a numeric value to an RGB gradient.

    Parameters:
        number (float): The number to convert.
        min_val (float): The minimum value in the range for normalization.
        max_val (float): The maximum value in the range for normalization.
        csv (int): Indicator for selecting preset color gradients. '1' or '2'.

    Returns:
        str: RGB color string
    """
    
    normalized_value = (number - min_val) / (max_val - min_val)
    if csv==1:
        color1 = (255, 255,0)  # Lightest color (white)
        color2 = (255, 0, 0)  # Brightest color (red)

    if csv==2:
        color1 = (0, 255, 255) # Lightest color (blue)
        color2 = (0, 0, 110)  # Brightest color (dark blue)
    return interpolate_color(color1, color2, normalized_value)

def check_data_types(df):
    """
    Analyze a DataFrame to determine the data types of its columns.

    Parameters:
        df (DataFrame): The DataFrame to analyze.

    Returns:
        dict: A dictionary mapping each column name to its determined data type.
    """
    
    data_types = {}
    for column in df.columns:
        dtype = df[column].dtype
        if column != 'Node_Size' and column != 'index':
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

def get_colors(df, column, datatype):
    """
    Apply color coding to a DataFrame based on the specified data type of a column.

    Parameters:
        df (DataFrame): The DataFrame to modify.
        column (str): The column based on which colors are applied.
        datatype (str): The data type of the column which dictates the coloring strategy.

    Returns:
        DataFrame: The modified DataFrame with an extra colum called 'color'.
    """
    # Define a list of colors to use for mapping
    colourlist =  ['red','yellow','orange','black']
    
    # Handle binary data: Assign 'yellow' for values 0 or 2, and 'red' for value 1
    if datatype == 'Binary':
        df.loc[df[column].isin([0, 2]) , 'color'] = 'yellow'
        df.loc[df[column] == 1 , 'color'] = 'red'
        
    # Handle categorical, low integer, or categorical data types
    elif datatype == 'Other' or datatype == 'Low_Integer' or datatype == 'Categorical':
        # Create a mapping of unique values to colors, cycling through the color list
        color_mapping = {}
        unique_values = df[column].unique()
        for i, value in enumerate(unique_values):
            color_mapping[value] = colourlist[i % len(colourlist)]
        # Map colors to each row based on the 'Type' column
        df['color'] = df[column].map(color_mapping)
    
    # Handle high integer or real number data types
    elif datatype == 'High_Integer' or datatype == 'Real':
        # Calculate a color gradient for each value in the column
        min_val = min(df[column])
        max_val = max(df[column])
        rgb_gradients = [number_to_rgb_gradient(num, min_val, max_val,1) for num in df[column]]
        # Apply the calculated gradient colors to the DataFrame
        df['color'] = rgb_gradients
    return df

def get_colors2(df, column, datatype):
    """
    Apply an alternative color coding to a DataFrame based on the specified data type of a column.
    Similar to `get_colors` but uses a different set of colors.

    Parameters:
        df (DataFrame): The DataFrame to modify.
        column (str): The column based on which colors are applied.
        datatype (str): The data type of the column which dictates the coloring strategy.

    Returns:
        DataFrame: The modified DataFrame with an extra colum called 'color'.
    """
    
    # Define a list of colors to use for mapping
    colourlist = ['cyan','purple''green','blue']
    
    # Handle binary data: Assign 'green' for values 0 or 2, and 'cyan' for value 1
    if datatype == 'Binary':
        df.loc[df[column].isin([0, 2]) , 'color'] = 'green'
        df.loc[df[column] == 1 , 'color'] = 'cyan'
        
    # Handle categorical, low integer, or categorical data types
    elif datatype == 'Other' or datatype == 'Low_Integer' or datatype == 'Categorical':
        # Create a mapping of unique values to colors, cycling through the color list
        color_mapping = {}
        unique_values = df[column].unique()
        for i, value in enumerate(unique_values):
            color_mapping[value] = colourlist[i % len(colourlist)]
        # Map colors to each row based on the 'Type' column
        df['color'] = df[column].map(color_mapping)
    
    elif datatype == 'High_Integer' or datatype == 'Real':
        # Calculate a color gradient for each value in the column
        min_val = min(df[column])
        max_val = max(df[column])
        rgb_gradients = [number_to_rgb_gradient(num, min_val, max_val,2) for num in df[column]]
        # Apply the calculated gradient colors to the DataFrame
        df['color'] = rgb_gradients
    return df