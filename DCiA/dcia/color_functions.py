#load colors for the nodes
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
        color1 = (255,255,204)  # Lightest color (white)
        color2 = (255,0,0)  # Brightest color (red)

    if csv==2:
        color1 = (240,248,255) # Lightest color (blue)
        color2 = (0, 2, 29)  # Brightest color (dark blue)
    return interpolate_color(color1, color2, normalized_value)

