"""
Demo script for ZWO ASI camera control using python-zwoasi.

This script demonstrates:
- Initializing the camera and printing specifications
- Changing exposure, gain, gamma, and region of interest (ROI)
- Capturing and plotting before/after images for each change (side-by-side with colorbars)
- Returning to the original settings

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
    
# Close any existing plots
plt.close('all')

# Grab the list of connected cameras and connect to the first one in the list
cameras = asi.list_cameras()
if not cameras:
    raise RuntimeError('No ZWO ASI cameras found.')
else:
    print(f'Found {len(cameras)} camera(s): {cameras}')
camera_id = 0
camera = asi.Camera(camera_id)

# Set the camera to RAW16 mode if it wasn't already
camera.set_image_type(asi.ASI_IMG_RAW16)

# Print current camera specifications
def print_camera_info(cam):
    info = cam.get_camera_property()
    print('\nCamera Info:')
    for k, v in info.items():
        print(f'  {k}: {v}')
    print('\nControls:')
    for parameter, ctrl in cam.get_controls().items():
        print(f'  {parameter}: {ctrl}')
print_camera_info(camera)

# Store original settings
def get_control_val(cam, parameter):
    ctrl = cam.get_controls()[parameter]
    return cam.get_control_value(ctrl['ControlType'])[0]

def set_control_val(cam, parameter, value):
    ctrl = cam.get_controls()[parameter]
    cam.set_control_value(ctrl['ControlType'], value)

# Establish original settings so we can return to them later
orig_exposure = get_control_val(camera, 'Exposure')
orig_gain = get_control_val(camera, 'Gain')
controls = camera.get_controls()
has_gamma = 'Gamma' in controls  # Since not all cameras will have a controllable gamma parameter
if has_gamma:
    orig_gamma = get_control_val(camera, 'Gamma')
else:
    orig_gamma = None
orig_roi = camera.get_roi()

# 1. Capture baseline image
image_original = camera.capture()

# 2. Change exposure
print(f'Original exposure: {orig_exposure}')
new_exposure = int(orig_exposure * 0.1) or 1000
set_control_val(camera, 'Exposure', new_exposure)
image_exposure = camera.capture()
set_control_val(camera, 'Exposure', orig_exposure)
image_exposure_restored = camera.capture()

# Plot before/after for exposure
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'Exposure: {orig_exposure}')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_exposure, cmap='gray')
axes[1].set_title(f'Exposure: {new_exposure}')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Effects of changing exposure')
fig.tight_layout()
plt.show(block=False)

# 3. Change gain
print(f'Original gain: {orig_gain}')
new_gain = int(orig_gain + 30)
set_control_val(camera, 'Gain', new_gain)
image_gain = camera.capture()
set_control_val(camera, 'Gain', orig_gain)
image_gain_restored = camera.capture()

# Plot before/after for gain
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'Gain: {orig_gain}')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_gain, cmap='gray')
axes[1].set_title(f'Gain: {new_gain}')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Effects of changing gain')
fig.tight_layout()
plt.show(block=False)

# 4. Change gamma (if available)
if has_gamma:
    print(f'Original gamma: {orig_gamma}')
    new_gamma = int(orig_gamma + 10)
    set_control_val(camera, 'Gamma', new_gamma)
    image_gamma = camera.capture()
    set_control_val(camera, 'Gamma', orig_gamma)
    image_gamma_restored = camera.capture()

    # Plot before/after for gamma
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    im0 = axes[0].imshow(image_original, cmap='gray')
    axes[0].set_title(f'Gamma: {orig_gamma}')
    plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
    im1 = axes[1].imshow(image_gamma, cmap='gray')
    axes[1].set_title(f'Gamma: {new_gamma}')
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    plt.suptitle('Effects of changing gamma')
    fig.tight_layout()
    plt.show(block=False)
else:
    print('Gamma control not available on this camera. Skipping gamma demo.')

# 5. Change ROI
print(f'Original ROI: {orig_roi}')
start_x, start_y, width, height = orig_roi
new_width = 64
new_height = 64
camera.set_roi(start_x=0, start_y=0, width=new_width, height=new_height)
image_roi = camera.capture()
camera.set_roi(start_x=start_x, start_y=start_y, width=width, height=height)
image_roi_restored = camera.capture()

# Plot before/after for ROI
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title(f'ROI: x={start_x}, y={start_y}, w={width}, h={height}')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_roi, cmap='gray')
axes[1].set_title(f'ROI: x=0, y=0, w={new_width}, h={new_height}')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Effects of changing ROI')
fig.tight_layout()
plt.show(block=False)

print('Demo complete. All settings restored.')
