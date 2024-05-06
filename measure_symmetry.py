import os
import json
import math

def determine_quadrant(element_center_x, element_center_y, center_x, center_y):
    if element_center_x < center_x and element_center_y < center_y:
        return 'UL'  # Upper-Left
    elif element_center_x >= center_x and element_center_y < center_y:
        return 'UR'  # Upper-Right
    elif element_center_x < center_x and element_center_y >= center_y:
        return 'LL'  # Lower-Left
    elif element_center_x >= center_x and element_center_y >= center_y:
        return 'LR'  # Lower-Right

def calculate_element_properties(bounds):
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    center_x = bounds[0] + width / 2
    center_y = bounds[1] + height / 2
    return center_x, center_y, width, height

def extract_ui_elements(data, parent_bounds=None):
    elements = []
    bounds = data.get('bounds', parent_bounds)
    if 'children' not in data or not data['children']:
        return [{'class': data['class'], 'bounds': bounds}]
    for child in data['children']:
        elements.extend(extract_ui_elements(child, bounds))
    return elements

# Function to calculate the symmetry score of a single UI screen
def calculate_symmetry(data):
    screen_bounds = data['bounds']
    screen_center_x = (screen_bounds[2] + screen_bounds[0]) / 2
    screen_center_y = (screen_bounds[3] + screen_bounds[1]) / 2

    # Extract UI elements
    ui_elements = extract_ui_elements(data)

    # Organize elements by quadrant
    quadrants = {'UL': [], 'UR': [], 'LL': [], 'LR': []}
    for element in ui_elements:
        center_x, center_y, width, height = calculate_element_properties(element['bounds'])
        quadrant = determine_quadrant(center_x, center_y, screen_center_x, screen_center_y)
        quadrants[quadrant].append({
            'center_x': center_x,
            'center_y': center_y,
            'width': width,
            'height': height
        })

    # Calculate averages for each quadrant
    quadrant_sums = {key: {'x_sum': 0, 'y_sum': 0, 'width_sum': 0, 'height_sum': 0, 'count': 0}
                     for key in quadrants.keys()}

    for quadrant, elements in quadrants.items():
        for element in elements:
            quadrant_sums[quadrant]['x_sum'] += element['center_x']
            quadrant_sums[quadrant]['y_sum'] += element['center_y']
            quadrant_sums[quadrant]['width_sum'] += element['width']
            quadrant_sums[quadrant]['height_sum'] += element['height']
            quadrant_sums[quadrant]['count'] += 1

    quadrant_averages = {}
    for quadrant, sums in quadrant_sums.items():
        count = sums['count']
        if count > 0:
            quadrant_averages[quadrant] = {
                'avg_center_x': sums['x_sum'] / count,
                'avg_center_y': sums['y_sum'] / count,
                'avg_width': sums['width_sum'] / count,
                'avg_height': sums['height_sum'] / count
            }
        else:
            quadrant_averages[quadrant] = None

    # Calculate symmetry values for vertical, horizontal
    symmetry_values = {'SYM_vertical': 0, 'SYM_horizontal': 0, 'SYM_radial': 0}
    if quadrant_averages['UL'] and quadrant_averages['UR']:
        symmetry_values['SYM_vertical'] = 1 - (
            abs(quadrant_averages['UL']['avg_center_x'] - quadrant_averages['UR']['avg_center_x']) /
            screen_center_x
        )

    if quadrant_averages['UL'] and quadrant_averages['LR']:
        symmetry_values['SYM_horizontal'] = 1 - (
            abs(quadrant_averages['UL']['avg_center_y'] - quadrant_averages['LR']['avg_center_y']) /
            screen_center_y
        )

    # Since we might not have elements in all quadrants, use available symmetry values
    overall_symmetry = 0
    symmetry_count = 0
    for symmetry in symmetry_values.values():
        if symmetry > 0:
            overall_symmetry += symmetry
            symmetry_count += 1

    if symmetry_count > 0:
        overall_symmetry /= symmetry_count  # Average symmetry score

    return overall_symmetry


# Directory containing the .json files
directory_path = '/Users/shauryamann/Desktop/Plaksha/Semester 6/Deep Learning/Project/semantic_annotations'

# Dictionary to store the overall symmetry scores for each file
symmetry_scores = {}

# Iterate over each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Calculate the symmetry score for this UI screen
        symmetry_score = calculate_symmetry(data)
        symmetry_scores[filename] = symmetry_score

# Print or return the symmetry scores
# print(symmetry_scores)
for key, value in symmetry_scores.items():
    if value < 0 or value > 1:
        print(key, value)