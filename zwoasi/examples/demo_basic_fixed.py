"""
Bare minimum ZWO ASI camera demo with automatic SDK path configuration

Automatically sets the ZWO_ASI_LIB environment variable to the correct path
regardless of where the script is run from. Demonstrates basic camera control
with minimal overhead.
"""

import os
import sys
import zwoasi as asi
import matplotlib.pyplot as plt
from matplotlib import use
use('TkAgg')  # Set an interactive backend. Might need to be changed depending on your system

# Automatically locate and set the ASI SDK library path
def setup_sdk_path():
    # Try to find the library relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    
    # Look in several possible locations
    possible_paths = [
        os.path.join(script_dir, '..', 'lib', 'ASICamera2.dll'),  # If running from examples dir
        os.path.join(root_dir, 'zwoasi', 'lib', 'ASICamera2.dll'),  # If running from project root
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            os.environ['ZWO_ASI_LIB'] = os.path.abspath(path)
            print(f"Found ASI SDK library at: {os.environ['ZWO_ASI_LIB']}")
            return True
    
    print("ASICamera2.dll not found. Please set ZWO_ASI_LIB environment variable manually.")
    return False

# Setup SDK path before initializing
if 'ZWO_ASI_LIB' not in os.environ:
    if not setup_sdk_path():
        sys.exit(1)

# Initialize SDK
try:
    asi.init()
    print("ASI SDK initialized successfully")
except Exception as e:
    print(f"Error initializing ASI SDK: {e}")
    sys.exit(1)

try:
    # Connect to first camera and set to 16-bit mode
    camera = asi.Camera(0)
    camera.set_image_type(asi.ASI_IMG_RAW16)
    
    # Print some camera info
    cam_info = camera.get_camera_property()
    print(f"Connected to camera: {cam_info['Name']}")

    # Capture baseline image
    print("Capturing baseline image...")
    image_baseline = camera.capture()

    # Change exposure, gain, and ROI
    camera.set_control_value(asi.ASI_EXPOSURE, 1000)  # microseconds
    camera.set_control_value(asi.ASI_GAIN, 50)
    camera.set_roi(start_x=100, start_y=100, width=200, height=200)
    
    print("Capturing final image with modified settings...")
    image_final = camera.capture()

    # Plot the baseline and final image side-by-side
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    im0 = ax[0].imshow(image_baseline, cmap='gray')
    ax[0].set_title('Baseline Image')
    plt.colorbar(im0, ax=ax[0])
    im1 = ax[1].imshow(image_final, cmap='gray')
    ax[1].set_title('Final Image')
    plt.colorbar(im1, ax=ax[1])
    fig.tight_layout()
    plt.show(block=False)
    
    # Keep the plot open until user closes it
    print("Close the plot window to exit")
    plt.show()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()