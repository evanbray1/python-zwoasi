"""
Basic demo script for ZWO ASI camera control using python-zwoasi.

This script demonstrates:
- Initializing the camera
- Changing exposure, gain, and region of interest (ROI)
- Capturing and plotting before/after images for each change (side-by-side with colorbars)

Run this script from an IDE. Requires the ZWO ASI SDK shared library and a connected camera.
Requires matplotlib for plotting.
"""

import os
import sys
import matplotlib.pyplot as plt
from matplotlib import use
use('TkAgg')  # Might need to be changed depending on your system

# Since this demo file is located within the repository itself, we have a try statement to determine 
# how to import the zwoasi module.
try:
    import zwoasi as asi
except ImportError:
    # Add the parent directory to sys.path and THEN try importing the zwoasi module
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    import zwoasi as asi

# Set path to ASICamera2.dll/.so/.dylib if not set in environment
SDK_PATH = os.environ.get('ZWO_ASI_LIB', None)
if SDK_PATH is None:
    # Check for the DLL in the lib subdirectory of the zwoasi package
    lib_path = os.path.join(os.path.dirname(asi.__file__), 'lib', 'ASICamera2.dll')
    if os.path.exists(lib_path):
        SDK_PATH = lib_path
    else:
        print('ASI SDK library not found. Please set ZWO_ASI_LIB environment variable.')
        print('Alternatively, place ASICamera2.dll in the zwoasi/lib/ directory.')
        sys.exit(1)

asi.init(SDK_PATH)

# ==============================================================================
# CAMERA INITIALIZATION
# ==============================================================================

# Close any existing plots
plt.close('all')

# Find and connect to the first available camera
cameras = asi.list_cameras()
if not cameras:
    raise RuntimeError('No ZWO ASI cameras found.')
else:
    print(f'Found {len(cameras)} camera(s): {cameras}')

camera = asi.Camera(0)  # Connect to the first camera

# Set the camera to RAW16 mode for better dynamic range
camera.set_image_type(asi.ASI_IMG_RAW16)

# Print basic camera information
info = camera.get_camera_property()
print('\nCamera Info:')
for key, value in info.items():
    print(f'  {key}: {value}')

# ==============================================================================
# DEFAULT CAMERA SETTINGS (MODIFY AS NEEDED)
# ==============================================================================

# Set default exposure and gain values for consistent demo behavior
# Modify these values based on your camera and lighting conditions
DEFAULT_EXPOSURE = 320  # microseconds 
DEFAULT_GAIN = 0        # gain value 

print('\nSetting default camera parameters for demo...')
print(f'  Setting exposure to: {DEFAULT_EXPOSURE} μs')
print(f'  Setting gain to: {DEFAULT_GAIN}')

# Apply default settings
camera.set_control_value(asi.ASI_EXPOSURE, DEFAULT_EXPOSURE)
camera.set_control_value(asi.ASI_GAIN, DEFAULT_GAIN)

# ==============================================================================
# STORE ORIGINAL SETTINGS
# ==============================================================================

# Get current camera control values using direct constants
orig_exposure = camera.get_control_value(asi.ASI_EXPOSURE)[0]
orig_gain = camera.get_control_value(asi.ASI_GAIN)[0]
orig_roi = camera.get_roi()

print('\nOriginal Settings:')
print(f'  Exposure: {orig_exposure}')
print(f'  Gain: {orig_gain}')
print(f'  ROI: {orig_roi}')

# ==============================================================================
# BASELINE IMAGE CAPTURE
# ==============================================================================

# Capture baseline image with original settings
print('\nCapturing baseline image...')
image_original = camera.capture()

# ==============================================================================
# EXPOSURE DEMONSTRATION
# ==============================================================================

print('\nDemonstrating exposure change...')
print(f'Original exposure: {orig_exposure}')

# Change exposure to 10% of original (or minimum 1000 microseconds)
new_exposure = max(int(orig_exposure * 0.1), 1000)
camera.set_control_value(asi.ASI_EXPOSURE, new_exposure)
image_exposure = camera.capture()

# Restore original exposure
camera.set_control_value(asi.ASI_EXPOSURE, orig_exposure)

# Plot before/after for exposure
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'Original Exposure: {orig_exposure} μs')
axes[0].axis('off')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_exposure, cmap='gray')
axes[1].set_title(f'Updated Exposure: {new_exposure} μs')
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Effects of Changing Exposure', fontsize=14)
fig.tight_layout()
plt.show(block=False)

# ==============================================================================
# GAIN DEMONSTRATION
# ==============================================================================

print('\nDemonstrating gain change...')
print(f'Original gain: {orig_gain}')

# Increase gain by 50 units (or to maximum if that would exceed it)
new_gain = min(orig_gain + 50, camera.get_controls()['Gain']['MaxValue'])
camera.set_control_value(asi.ASI_GAIN, new_gain)
image_gain = camera.capture()

# Restore original gain
camera.set_control_value(asi.ASI_GAIN, orig_gain)

# Plot before/after for gain
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'Original Gain: {orig_gain}')
axes[0].axis('off')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_gain, cmap='gray')
axes[1].set_title(f'Increased Gain: {new_gain}')
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Effects of Changing Gain', fontsize=14)
fig.tight_layout()
plt.show(block=False)

# ==============================================================================
# REGION OF INTEREST (ROI) DEMONSTRATION
# ==============================================================================

print('\nDemonstrating ROI change...')
print(f'Original ROI: {orig_roi}')

# Change ROI to a small central region
start_x, start_y, width, height = orig_roi
new_width = 128
new_height = 128
# Center the smaller ROI
new_start_x = max(0, (width - new_width) // 2)
new_start_y = max(0, (height - new_height) // 2)

camera.set_roi(start_x=new_start_x, start_y=new_start_y, width=new_width, height=new_height)
image_roi = camera.capture()

# Restore original ROI
camera.set_roi(start_x=start_x, start_y=start_y, width=width, height=height)

# Plot before/after for ROI
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'Full Frame: {width}×{height}')
axes[0].axis('off')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_roi, cmap='gray')
axes[1].set_title(f'ROI: {new_width}×{new_height}')
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Effects of Changing Region of Interest (ROI)', fontsize=14)
fig.tight_layout()
plt.show(block=False)

# ==============================================================================
# CLEANUP
# ==============================================================================

print('\nDemo complete. All settings have been restored to original values.')
print('Camera will automatically close when the script ends.')
