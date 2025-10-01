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

# %% Camera Initialization

# Close any existing plots
plt.close('all')

# Find and connect to the first available camera
cameras = asi.list_cameras()
if not cameras:
    raise RuntimeError('No ZWO ASI cameras found.')
else:
    print(f'Found {len(cameras)} camera(s): {cameras}')

camera_id = 0
camera = asi.Camera(camera_id)

# Set the camera to RAW16 mode for better dynamic range
camera.set_image_type(asi.ASI_IMG_RAW16)

# Print basic camera information
info = camera.get_camera_property()
print('\nCamera Info:')
for k, v in info.items():
    print(f'  {k}: {v}')

# %% Store Original Settings

# Get current camera control values
controls = camera.get_controls()
orig_exposure = camera.get_control_value(controls['Exposure']['ControlType'])[0]
orig_gain = camera.get_control_value(controls['Gain']['ControlType'])[0]
orig_roi = camera.get_roi()

print('\nOriginal Settings:')
print(f'  Exposure: {orig_exposure}')
print(f'  Gain: {orig_gain}')
print(f'  ROI: {orig_roi}')

# %% Baseline Image Capture

# Capture baseline image with original settings
print('\nCapturing baseline image...')
image_original = camera.capture()

# %% Exposure Demonstration

print('\nDemonstrating exposure change...')
print(f'Original exposure: {orig_exposure}')

# Change exposure to 10% of original (or minimum 1000 microseconds)
new_exposure = max(int(orig_exposure * 0.1), 1000)
camera.set_control_value(controls['Exposure']['ControlType'], new_exposure)
image_exposure = camera.capture()

# Restore original exposure
camera.set_control_value(controls['Exposure']['ControlType'], orig_exposure)

# Plot before/after for exposure
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'Original Exposure: {orig_exposure} μs')
axes[0].axis('off')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

im1 = axes[1].imshow(image_exposure, cmap='gray')
axes[1].set_title(f'Reduced Exposure: {new_exposure} μs')
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

plt.suptitle('Effects of Changing Exposure', fontsize=14)
fig.tight_layout()
plt.show(block=False)

# %% Gain Demonstration

print('\nDemonstrating gain change...')
print(f'Original gain: {orig_gain}')

# Increase gain by 50 units (or to maximum if that would exceed it)
max_gain = controls['Gain']['MaxValue']
new_gain = min(orig_gain + 50, max_gain)
camera.set_control_value(controls['Gain']['ControlType'], new_gain)
image_gain = camera.capture()

# Restore original gain
camera.set_control_value(controls['Gain']['ControlType'], orig_gain)

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

# %% Region of Interest (ROI) Demonstration

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

# %% Cleanup

print('\nDemo complete. All settings have been restored to original values.')
print('Close the camera when done.')
# Note: Camera will be automatically closed when the script ends
