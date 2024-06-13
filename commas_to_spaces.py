import os

def convert_comma_to_space_in_files(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print("Directory does not exist.")
        return
    
    # Loop through each file in the specified directory
    for filename in os.listdir(directory_path):
        # Check if the file is a .txt file
        if filename.endswith('.txt'):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)
            
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Replace commas with spaces
            new_content = content.replace(',', ' ')
            
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.write(new_content)
            
            print(f"Converted commas to spaces in: {filename}")

# Replace '/path/to/your/directory' with the actual path to the directory containing your .txt files
directory_path = 'data/pointclouds'
convert_comma_to_space_in_files(directory_path)