import copy
import numpy as np
import random as rd

def generate_corners(num_segs, len_seg, r, wid_joi, dep_joi, key_stone_small_arc, key_stone_large_arc):

    ang_joi = wid_joi / r # small angle approx

    # subtract average keystone arc and divide by remaining segs
    standard_seg_arc = (2 * np.pi - (key_stone_large_arc + key_stone_small_arc) / 2) / (num_segs - 1)

    # Initialize the segment_vectors dictionary with empty lists for each key
    segment_vectors = {
        **{f"seg{i}": {"corners": [], "s_edges": [], "c_edges": []} for i in range(0, num_segs)}
    }

    for i in range(num_segs):

        key = f"seg{i}"

        # KEYSTONE
        if i == 0:
            # Angles on long side of keystone
            ang1 = 0
            ang2 = key_stone_large_arc

            # Angles on short side of keystone 
            ang3 = (key_stone_large_arc - key_stone_small_arc) / 2
            ang4 = key_stone_large_arc / 2 + key_stone_small_arc / 2

        elif i == 1:
            # Angles on long side of keystone
            ang1 = key_stone_large_arc
            ang2 = key_stone_large_arc - (key_stone_large_arc - key_stone_small_arc) / 4 + standard_seg_arc

            # Angles on short side of keystone 
            ang3 = key_stone_large_arc / 2 + key_stone_small_arc / 2
            ang4 = ang2
        
        elif i == num_segs - 1:
            # Angles on long side of keystone
            ang1 = key_stone_large_arc - (key_stone_large_arc - key_stone_small_arc) / 4 + (i - 1) * standard_seg_arc
            ang2 = 0

            # Angles on short side of keystone 
            ang3 = ang1
            ang4 = (key_stone_large_arc - key_stone_small_arc) / 2
        else:
            # Angles on long side of keystone
            ang1 = key_stone_large_arc - (key_stone_large_arc - key_stone_small_arc) / 4 + (i - 1) * standard_seg_arc
            ang2 = ang1 + standard_seg_arc

            # Angles on short side of keystone 
            ang3 = ang1
            ang4 = ang2
        
        angles = [ang1, ang2, ang3, ang4]

        for outerisTrue in [True, False]:

            for j, ang in enumerate(angles):
                
                # If on inside, the points are pushed towards the x-axis
                if j <= 1:
                    y = -len_seg / 2
                    if not outerisTrue:
                        y += wid_joi / 2
                else:
                    y = len_seg / 2
                    if not outerisTrue:
                        y -= wid_joi / 2

                if outerisTrue:
                    rr = r + dep_joi
                    corner_num = j + 1
                else:
                    rr = r
                    corner_num = j + 5                    
                    
                    # bring corners towards eachother
                    if j%2 == 0:
                        ang += ang_joi / 2
                    else:
                        ang -= ang_joi / 2

                p = (rr * np.sin(ang), y, rr * np.cos(ang))
                segment_vectors[f"seg{i}"]["corners"].append(p)

    return segment_vectors

def generate_circular_edges(segment_vectors, r, dep_joi, wid_joi, len_seg):

    num_segs = len(segment_vectors.keys())

    # indices of connected points, radius, normal vector
    edge_01 = [(0, 1), r + dep_joi, (0, -len_seg/2, 0)]
    edge_23 = [(2, 3), r + dep_joi, (0, len_seg/2, 0)]
    edge_45 = [(4, 5), r, (0, -len_seg/2 + wid_joi/2, 0)]
    edge_67 = [(6, 7), r, (0, len_seg/2 - wid_joi/2, 0)]

    circular_edges = [edge_01, edge_23, edge_45, edge_67]

    for i in range(num_segs):
        for edge in circular_edges:
            segment_vectors[f"seg{i}"]["c_edges"].append(edge)

    return segment_vectors

def generate_straight_edges(segment_vectors):

    num_segs = len(segment_vectors.keys())

    # add all long edges
    long_straight_edges = [(0, 2), (1, 3), (4, 6), (5, 7)]
    for i in range(num_segs):
        segment_vectors[f"seg{i}"]["s_edges"].extend(long_straight_edges)

    # add all small edges 
    short_straight_edges = [(0, 4), (1, 5), (2, 6), (3, 7)]
    for i in range(num_segs):
        segment_vectors[f"seg{i}"]["s_edges"].extend(short_straight_edges)

    return segment_vectors


def get_all_corners(segment_vectors):
    all_corners = []
    for key in segment_vectors:
        all_corners.extend([inner_list for inner_list in segment_vectors[key].values()][0])
        #breakpoint()
    return all_corners

def generate_pc(num_segs, len_seg, r, wid_joi, dep_joi, key_stone_small_arc, key_stone_large_arc):

    segment_vectors = generate_corners(num_segs, len_seg, r, wid_joi, dep_joi, key_stone_small_arc, key_stone_large_arc)
    segment_vectors = generate_straight_edges(segment_vectors)
    segment_vectors = generate_circular_edges(segment_vectors, r, dep_joi, wid_joi, len_seg)
    
    return segment_vectors


if __name__ == '__main__':

    segment_vectors = generate_pc(6, 1.5, 2.75, 0.1, 0.05, 20 * np.pi/180, 25 * np.pi/180)
    print(segment_vectors["seg0"])

