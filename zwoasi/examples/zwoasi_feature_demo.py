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

# Add the parent directory to sys.path to use the local development version
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import zwoasi as asi

cameras = asi.list_cameras()
if not cameras:
    raise RuntimeError('No ZWO ASI cameras found.')

camera_id = 0
camera = asi.Camera(camera_id)

# Print camera specifications
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

orig_exposure = get_control_val(camera, 'Exposure')
orig_gain = get_control_val(camera, 'Gain')
orig_gamma = get_control_val(camera, 'Gamma')
orig_roi = camera.get_roi()

# 1. Capture baseline image
image_original = camera.capture()

# 2. Change exposure
print(f'Original exposure: {orig_exposure}')
set_control_val(camera, 'Exposure', int(orig_exposure * 0.1) or 1000)
image_exposure = camera.capture()
set_control_val(camera, 'Exposure', orig_exposure)
image_exposure_restored = camera.capture()

# Plot before/after for exposure
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title('Original Exposure')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_exposure, cmap='gray')
axes[1].set_title('Changed Exposure')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Exposure Change')
plt.show(block=False)

# 3. Change gain
print(f'Original gain: {orig_gain}')
set_control_val(camera, 'Gain', int(orig_gain + 10))
image_gain = camera.capture()
set_control_val(camera, 'Gain', orig_gain)
image_gain_restored = camera.capture()

# Plot before/after for gain
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title('Original Gain')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_gain, cmap='gray')
axes[1].set_title('Changed Gain')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Gain Change')
plt.show(block=False)

# 4. Change gamma
print(f'Original gamma: {orig_gamma}')
set_control_val(camera, 'Gamma', int(orig_gamma + 10))
image_gamma = camera.capture()
set_control_val(camera, 'Gamma', orig_gamma)
image_gamma_restored = camera.capture()

# Plot before/after for gamma
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title('Original Gamma')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_gamma, cmap='gray')
axes[1].set_title('Changed Gamma')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('Gamma Change')
plt.show(block=False)

# 5. Change ROI
print(f'Original ROI: {orig_roi}')
start_x, start_y, width, height = orig_roi
new_width = max(64, width // 2)
new_height = max(64, height // 2)
camera.set_roi(start_x=0, start_y=0, width=new_width, height=new_height)
image_roi = camera.capture()
camera.set_roi(start_x=start_x, start_y=start_y, width=width, height=height)
image_roi_restored = camera.capture()

# Plot before/after for ROI
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image_original, cmap='gray')
axes[0].set_title('Original ROI')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
im1 = axes[1].imshow(image_roi, cmap='gray')
axes[1].set_title('Changed ROI')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
plt.suptitle('ROI Change')
plt.show(block=False)

print('Demo complete. All settings restored.')