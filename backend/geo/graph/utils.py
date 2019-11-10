# TODO: geojson to graph with ijson


def get_lines_intersection_point(f_line, s_line):
    p1, p2 = f_line
    x1, y1 = p1
    x2, y2 = p2

    p3, p4 = s_line
    x3, y3 = p3
    x4, y4 = p4

    divider = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if divider == 0:
        return None  # Lines are parallel

    temp1 = x1 * y2 - y1 * x2
    temp2 = x3 * y4 - y3 * x4

    intersection_x = temp1 * (x3 - x4) - temp2 * (x1 - x2)
    intersection_y = temp1 * (y3 - y4) - temp2 * (y1 - y2)

    return intersection_x / divider, intersection_y / divider
