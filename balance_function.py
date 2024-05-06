def calculate_area(bounds):
    return (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])

def do_rectangles_overlap(rect1, rect2):
    return not (rect1[2] <= rect2[0] or rect1[0] >= rect2[2] or rect1[3] <= rect2[1] or rect1[1] >= rect2[3])

def merge_overlapping_objects(data):
    merged_objects = []

    if 'children' in data:
        for parent in data['children']:
            non_overlapping_children = []

            if 'children' in parent:
                for child in parent['children']:
                    overlapping = False
                    for merged_obj in merged_objects:
                        if do_rectangles_overlap(child['bounds'], merged_obj['bounds']):
                            overlapping = True
                            break

                    if not overlapping:
                        non_overlapping_children.append(child)

                merged_objects.extend(non_overlapping_children)

    return merged_objects

def calculate_density_measure(total_area, frame_area):
    if total_area > 0 and frame_area > 0:
        density_measure = 1 - 2 * abs(0.5 - total_area / frame_area)
        density_measure = max(0, min(1, density_measure))
    else:
        density_measure = 0

    return density_measure

def calculate_density(data):
    total_area = 0

    merged_objects = merge_overlapping_objects(data)

    for item in merged_objects:
        bounds = item.get('bounds')
        if bounds:
            area = calculate_area(bounds)
            total_area += area

    frame_bounds = data.get('bounds')
    if frame_bounds:
        frame_area = calculate_area(frame_bounds)

    density_measure = calculate_density_measure(total_area, frame_area)
    scaled_density_measure = 1 - (abs(density_measure - 0.5) * 2)

    return scaled_density_measure