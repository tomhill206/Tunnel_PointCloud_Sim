
# Tunnel Point Cloud Simulator

Simulate LiDAR scans of tunnels with parameterisable geometry. Currently only tested on Mac.




## Installation

Links:

blainder_scanner -> https://github.com/ln-12/blainder-range-scanner

Blender 3.3 LTS -> https://www.blender.org/download/lts/3-3/

1) Set up Blender
- Install Blender 3.3 LTS from the Blender website
- Open Blender application then close it.
- Clone blainder_scanner repository and copy the 'range_scanner' folder into:
```
/Applications/Blender.app/Contents/Resources/3.3/scripts/addons_contrib
```
- In terminal, cd into the range_scanner folder and execute:
```
/Applications/Blender.app/Contents/Resources/3.3/python/bin/python3.10 -m pip install -r requirements.txt
```
(edit for your python version)
- Open Blender again and navigate to Edit/Preferences/Add-ons/Testing and check the range_scanner box.
- Close Blender 

2) Set up Simulator
- Clone this repository
- Move 'scanner_script.py' into the range_scanner folder.
- Add information to the config file
- Change output_path in scanning_script.py to your own for data/csv
- Changing scanning resolution must be done inside scanner_script.py


    
## Usage

```
python3 main.py
```

