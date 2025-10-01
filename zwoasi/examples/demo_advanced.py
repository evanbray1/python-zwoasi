"""
Advanced demo script for ZWO ASI camera control using python-zwoasi.

This script demonstrates:
- Printing detailed camera specifications  
- Changing gamma, binning, brightness, and image modes (MONO8 vs MONO16)
- Using video mode and demonstrating its advantages
- Capturing and plotting before/after images for each change (side-by-side with colorbars)

Run this script from an IDE. Requires the ZWO ASI SDK shared library and a connected camera.
Requires matplotlib for plotting.
"""

import os
import sys
import matplotlib.pyplot as plt
import time

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

# %% Camera Initialization and Detailed Specifications

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

# Set the camera to RAW16 mode initially
camera.set_image_type(asi.ASI_IMG_RAW16)

# Print detailed camera specifications
print('\n' + '=' * 50)
print('DETAILED CAMERA SPECIFICATIONS')
print('=' * 50)

info = camera.get_camera_property()
print('\nCamera Properties:')
for k, v in info.items():
    print(f'  {k}: {v}')

print('\nAvailable Controls:')
controls = camera.get_controls()
for parameter, ctrl in controls.items():
    print(f'  {parameter}:')
    for key, value in ctrl.items():
        print(f'    {key}: {value}')

# %% Store Original Settings

# Get current camera control values
orig_exposure = camera.get_control_value(controls['Exposure']['ControlType'])[0]
orig_gain = camera.get_control_value(controls['Gain']['ControlType'])[0]
orig_roi = camera.get_roi()

# Check if gamma control is available
has_gamma = 'Gamma' in controls
if has_gamma:
    orig_gamma = camera.get_control_value(controls['Gamma']['ControlType'])[0]

# Check if brightness control is available  
has_brightness = 'Brightness' in controls
if has_brightness:
    orig_brightness = camera.get_control_value(controls['Brightness']['ControlType'])[0]

print(f'\nOriginal Settings:')
print(f'  Exposure: {orig_exposure}')
print(f'  Gain: {orig_gain}')
if has_gamma:
    print(f'  Gamma: {orig_gamma}')
if has_brightness:
    print(f'  Brightness: {orig_brightness}')
print(f'  ROI: {orig_roi}')
print(f'  Current binning: {camera.get_bin()}')

# %% Gamma Demonstration

if has_gamma:
    print('\n' + '=' * 30)
    print('GAMMA DEMONSTRATION')
    print('=' * 30)

    # Capture baseline image
    image_original = camera.capture()

    # Change gamma
    print(f'Original gamma: {orig_gamma}')
    new_gamma = min(orig_gamma + 20, controls['Gamma']['MaxValue'])
    camera.set_control_value(controls['Gamma']['ControlType'], new_gamma)
    image_gamma = camera.capture()

    # Restore original gamma
    camera.set_control_value(controls['Gamma']['ControlType'], orig_gamma)

    # Plot before/after for gamma
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im0 = axes[0].imshow(image_original, cmap='gray')
    axes[0].set_title(f'Original Gamma: {orig_gamma}')
    axes[0].axis('off')
    plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    im1 = axes[1].imshow(image_gamma, cmap='gray')
    axes[1].set_title(f'Increased Gamma: {new_gamma}')
    axes[1].axis('off')
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

    plt.suptitle('Effects of Changing Gamma', fontsize=14)
    fig.tight_layout()
    plt.show(block=False)
else:
    print('\nGamma control not available on this camera. Skipping gamma demo.')

# %% Binning Demonstration

print('\n' + '=' * 30)
print('BINNING DEMONSTRATION')
print('=' * 30)

# Get supported binning modes from camera info
supported_bins = [bin_val for bin_val in info['SupportedBins'] if bin_val > 0]
print(f'Supported binning modes: {supported_bins}')

if len(supported_bins) > 1:
    # Capture with binning 1 (no binning)
    camera.set_roi(bins=1)
    image_no_bin = camera.capture()
    print(f'Captured image with binning=1, size: {image_no_bin.shape}')

    # Capture with binning 2 (if supported)
    if 2 in supported_bins:
        camera.set_roi(bins=2)
        image_bin2 = camera.capture()
        print(f'Captured image with binning=2, size: {image_bin2.shape}')

        # Plot before/after for binning
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        im0 = axes[0].imshow(image_no_bin, cmap='gray')
        axes[0].set_title(f'No Binning (1×1)\nSize: {image_no_bin.shape}')
        axes[0].axis('off')
        plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

        im1 = axes[1].imshow(image_bin2, cmap='gray')
        axes[1].set_title(f'2×2 Binning\nSize: {image_bin2.shape}')
        axes[1].axis('off')
        plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

        plt.suptitle('Effects of Pixel Binning (improves sensitivity, reduces resolution)', fontsize=14)
        fig.tight_layout()
        plt.show(block=False)

    # Restore original binning
    camera.set_roi(bins=1)
else:
    print('Only one binning mode supported. Skipping binning demo.')

# %% Brightness Demonstration

if has_brightness:
    print('\n' + '=' * 30)
    print('BRIGHTNESS DEMONSTRATION')  
    print('=' * 30)

    # Capture baseline image
    image_original = camera.capture()

    # Change brightness
    print(f'Original brightness: {orig_brightness}')
    new_brightness = min(orig_brightness + 30, controls['Brightness']['MaxValue'])
    camera.set_control_value(controls['Brightness']['ControlType'], new_brightness)
    image_brightness = camera.capture()

    # Restore original brightness
    camera.set_control_value(controls['Brightness']['ControlType'], orig_brightness)

    # Plot before/after for brightness
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im0 = axes[0].imshow(image_original, cmap='gray')
    axes[0].set_title(f'Original Brightness: {orig_brightness}')
    axes[0].axis('off')
    plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    im1 = axes[1].imshow(image_brightness, cmap='gray')
    axes[1].set_title(f'Increased Brightness: {new_brightness}')
    axes[1].axis('off')
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

    plt.suptitle('Effects of Changing Brightness', fontsize=14)
    fig.tight_layout()
    plt.show(block=False)
else:
    print('\nBrightness control not available on this camera. Skipping brightness demo.')

# %% Image Mode Demonstration (MONO8 vs MONO16)

print('\n' + '=' * 30)
print('IMAGE MODE DEMONSTRATION')
print('=' * 30)

# Capture in 16-bit mode (current mode)
image_16bit = camera.capture()
print(f'16-bit image - dtype: {image_16bit.dtype}, range: {image_16bit.min()}-{image_16bit.max()}')

# Switch to 8-bit mode
camera.set_image_type(asi.ASI_IMG_RAW8)
image_8bit = camera.capture()
print(f'8-bit image - dtype: {image_8bit.dtype}, range: {image_8bit.min()}-{image_8bit.max()}')

# Plot comparison of 8-bit vs 16-bit
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
im0 = axes[0].imshow(image_8bit, cmap='gray')
axes[0].set_title('8-bit Mode (RAW8)\nRange: 0-255')
axes[0].axis('off')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

im1 = axes[1].imshow(image_16bit, cmap='gray')
axes[1].set_title('16-bit Mode (RAW16)\nRange: 0-65535')
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

plt.suptitle('8-bit vs 16-bit Image Modes (16-bit offers better dynamic range)', fontsize=14)
fig.tight_layout()
plt.show(block=False)

# Restore to 16-bit mode
camera.set_image_type(asi.ASI_IMG_RAW16)

# %% Video Mode Demonstration

print('\n' + '=' * 30)
print('VIDEO MODE DEMONSTRATION')
print('=' * 30)

print('Video mode advantages:')
print('- Faster frame rates for live preview')
print('- Better for auto-exposure/auto-gain algorithms')  
print('- Continuous streaming capability')
print('- Lower latency between captures')

# Stop any ongoing exposure and start video mode
try:
    camera.stop_exposure()
except:
    pass

print('\nStarting video capture mode...')
camera.start_video_capture()

# Enable auto-exposure and auto-gain for demonstration
if 'Exposure' in controls and controls['Exposure']['IsAutoSupported']:
    print('Enabling auto-exposure...')
    camera.set_control_value(asi.ASI_EXPOSURE, controls['Exposure']['DefaultValue'], auto=True)

if 'Gain' in controls and controls['Gain']['IsAutoSupported']:
    print('Enabling auto-gain...')  
    camera.set_control_value(asi.ASI_GAIN, controls['Gain']['DefaultValue'], auto=True)

# Capture a series of video frames to show speed
print('\nCapturing video frames...')
frame_times = []
num_frames = 5

for i in range(num_frames):
    start_time = time.time()
    frame = camera.capture_video_frame()
    end_time = time.time()
    frame_time = end_time - start_time
    frame_times.append(frame_time)
    print(f'Frame {i+1}: {frame_time:.3f}s, size: {frame.shape}')

avg_frame_time = sum(frame_times) / len(frame_times)
fps = 1.0 / avg_frame_time
print(f'\nAverage frame capture time: {avg_frame_time:.3f}s')
print(f'Approximate frame rate: {fps:.1f} FPS')

# Capture final video frame for display
final_frame = camera.capture_video_frame()

# Stop video mode
camera.stop_video_capture()

# Show the final video frame
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
im = ax.imshow(final_frame, cmap='gray')
ax.set_title(f'Video Mode Frame\nAverage capture time: {avg_frame_time:.3f}s (~{fps:.1f} FPS)')
ax.axis('off')
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.show(block=False)

# %% Restore All Settings

print('\n' + '=' * 30)
print('RESTORING ORIGINAL SETTINGS')
print('=' * 30)

# Restore all original settings
camera.set_control_value(controls['Exposure']['ControlType'], orig_exposure)
camera.set_control_value(controls['Gain']['ControlType'], orig_gain)

if has_gamma:
    camera.set_control_value(controls['Gamma']['ControlType'], orig_gamma)

if has_brightness:
    camera.set_control_value(controls['Brightness']['ControlType'], orig_brightness)

# Restore original ROI
start_x, start_y, width, height = orig_roi
camera.set_roi(start_x=start_x, start_y=start_y, width=width, height=height)

print('All settings have been restored to their original values.')
print('\nAdvanced demo complete!')
print('Close the camera when done.')
# Note: Camera will be automatically closed when the script ends
