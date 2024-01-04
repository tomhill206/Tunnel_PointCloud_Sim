import pandas as pd


def process_csv(output_csv):
    # Read the CSV file into a DataFrame
    input_csv = '/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/csv/tunnel_frames_1_to_1.csv'
    df = pd.read_csv(input_csv, sep=';')

    # Define columns to keep
    columns_to_keep = [0, 1, 6, 7, 8]  # 0-indexed column numbers

    # Filter the DataFrame to keep only the specified columns
    df = df.iloc[:, columns_to_keep]

    # Rearrange columns - move first two columns to the end
    cols = df.columns.tolist()
    cols = cols[2:] + cols[:2]
    df = df[cols]

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

#process_csv('/Users/tomhill/Documents/Tunnel_PointCloud_Sim/data/pointclouds/tunnel1.csv')