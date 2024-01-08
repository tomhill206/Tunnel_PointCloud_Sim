import copy
import numpy as np
import random as rd

def generate_corners(num_segs, len_seg, r, wid_joi, dep_joi, key_stone_small_arc, key_stone_large_arc):

    ang_joi = wid_joi / r # small angle approx

    # subtract average keystone arc and divide by remaining segs
    standard_seg_arc = (2 * np.pi - (key_stone_large_arc + key_stone_small_arc) / 2) / (num_segs - 1)

    # Initalise dictionary representation of pc
    segment_vectors = {
        f"seg{i}": {
            "corners": [], 
            "s_edges": [], 
            "c_edges": [],
            **{f"seg{i}_joi{j}": {"corners": [], "s_edges": [], "c_edges": []} for j in range(4)}
        } for i in range(num_segs)
    }

    # Add segment information
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

        all_angles = []
        
        for outerisTrue in [True, False]:
            # reset angle list
            angles = [ang1, ang2, ang3, ang4]

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
                
                # Update angle in list
                angles[j] = ang

                # Save point
                p = [rr * np.sin(ang), y, rr * np.cos(ang)]
                segment_vectors[f"seg{i}"]["corners"].append(p)
            
            # Add the current 4 angles to the list
            all_angles.extend(angles)
         
        segment_vectors[f"seg{i}"] = add_joint_information(segment_vectors[f"seg{i}"], all_angles, i, dep_joi, wid_joi, len_seg)

    return segment_vectors

def modification(ang):
    thickness = 0.01

    return np.array([thickness * np.sin(ang), 0, thickness * np.cos(ang)])


def add_joint_information(segment_data, all_angles, seg_no, dep_joi, wid_joi, len_seg):

    # Add joint information
    for i in range(4):
        key = f"seg{seg_no}_joi{i}"

        if i == 0:

            corners = [
                segment_data["corners"][2],
                segment_data["corners"][0],
                segment_data["corners"][6],
                segment_data["corners"][4],
                segment_data["corners"][2] + modification(all_angles[2]),
                segment_data["corners"][0] + modification(all_angles[0]),
                segment_data["corners"][6] + modification(all_angles[6]),
                segment_data["corners"][4] + modification(all_angles[4])
            ]

            straight_edges = [
                (0, 1), (2, 3), (4, 5), (6, 7),
                (0, 2), (1, 3), (4, 6), (5, 7), 
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]

            segment_data[key]["corners"].extend(corners)
            segment_data[key]["s_edges"].extend(straight_edges)

        elif i == 1:

            corners = [
                segment_data["corners"][1],
                segment_data["corners"][3],
                segment_data["corners"][5],
                segment_data["corners"][7],
                segment_data["corners"][1] + modification(all_angles[1]),
                segment_data["corners"][3] + modification(all_angles[3]),
                segment_data["corners"][5] + modification(all_angles[5]),
                segment_data["corners"][7] + modification(all_angles[7])
            ]

            straight_edges = [
                (0, 1), (2, 3), (4, 5), (6, 7),
                (0, 2), (1, 3), (4, 6), (5, 7), 
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]

            segment_data[key]["corners"].extend(corners)
            segment_data[key]["s_edges"].extend(straight_edges)
        
        elif i == 2:

            corners = [
                segment_data["corners"][0],
                segment_data["corners"][1],
                segment_data["corners"][4],
                segment_data["corners"][5],
                segment_data["corners"][0] + modification(all_angles[0]),
                segment_data["corners"][1] + modification(all_angles[1]),
                segment_data["corners"][4] + modification(all_angles[4]),
                segment_data["corners"][5] + modification(all_angles[5])
            ]

            straight_edges = [
                (0, 2), (1, 3), (4, 6), (5, 7), 
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]

            edge_01 = [(0, 1), r + dep_joi, (0, -len_seg/2, 0)]
            edge_23 = [(2, 3), r, (0, len_seg/2, 0)]
            edge_45 = [(4, 5), r + dep_joi - 0.01 , (0, -len_seg/2 + wid_joi/2, 0)]
            edge_67 = [(6, 7), r - 0.01, (0, len_seg/2 - wid_joi/2, 0)]

            circular_edges = [edge_01, edge_23, edge_45, edge_67]

            segment_data[key]["corners"].extend(corners)
            segment_data[key]["s_edges"].extend(straight_edges)
            segment_data[key]["c_edges"].extend(circular_edges)


        elif i == 3:

            corners = [
                segment_data["corners"][3],
                segment_data["corners"][2],
                segment_data["corners"][7],
                segment_data["corners"][6],
                segment_data["corners"][3] + modification(all_angles[3]),
                segment_data["corners"][2] + modification(all_angles[2]),
                segment_data["corners"][7] + modification(all_angles[7]),
                segment_data["corners"][6] + modification(all_angles[6])
            ]

            straight_edges = [
                (0, 2), (1, 3), (4, 6), (5, 7), 
                (0, 4), (1, 5), (2, 6), (3, 7)
            ]

            edge_01 = [(0, 1), r + dep_joi, (0, -len_seg/2, 0)]
            edge_23 = [(2, 3), r, (0, len_seg/2, 0)]
            edge_45 = [(4, 5), r + dep_joi - 0.01 , (0, -len_seg/2 + wid_joi/2, 0)]
            edge_67 = [(6, 7), r - 0.01, (0, len_seg/2 - wid_joi/2, 0)]

            circular_edges = [edge_01, edge_23, edge_45, edge_67]

            segment_data[key]["corners"].extend(corners)
            segment_data[key]["s_edges"].extend(straight_edges)
            segment_data[key]["c_edges"].extend(circular_edges)
        
    return segment_data

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

