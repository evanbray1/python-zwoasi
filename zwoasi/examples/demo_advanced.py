"""
Advanced demo script for ZWO ASI camera control using python-zwoasi.

This script demonstrates:
- Printing detailed camera specifications  
- Changing gamma, binning, brightness, and image modes (MONO8 vs MONO16)
- Using video mode and demonstrating its advantages
- Auto-exposure functionality and comparison with manual exposure

Recommended to run this script from an IDE.
"""

import matplotlib.pyplot as plt
import time
import zwoasi as asi
from matplotlib import use
use('TkAgg')  # Set an interactive backend. Might need to be changed depending on your system

# ==============================================================================
# CAMERA INITIALIZATION AND DETAILED SPECIFICATIONS
# ==============================================================================

# Close any existing plots
plt.close('all')

# Find and connect to the first available camera
asi.init()
cameras = asi.list_cameras()
if not cameras:
    raise RuntimeError('No ZWO ASI cameras found.')
else:
    print(f'Found {len(cameras)} camera(s): {cameras}')
camera = asi.Camera(0)

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

# Check if gamma control is available
has_gamma = 'Gamma' in controls
if has_gamma:
    orig_gamma = camera.get_control_value(asi.ASI_GAMMA)[0]

# Check if brightness control is available  
has_brightness = 'Brightness' in controls
if has_brightness:
    orig_brightness = camera.get_control_value(asi.ASI_BRIGHTNESS)[0]

print('\nOriginal Settings:')
print(f'  Exposure: {orig_exposure}')
print(f'  Gain: {orig_gain}')
if has_gamma:
    print(f'  Gamma: {orig_gamma}')
if has_brightness:
    print(f'  Brightness: {orig_brightness}')
print(f'  ROI: {orig_roi}')
print(f'  Current binning: {camera.get_bin()}')

# ==============================================================================
# GAMMA DEMONSTRATION
# ==============================================================================

if has_gamma:
    print('\n' + '=' * 30)
    print('GAMMA DEMONSTRATION')
    print('=' * 30)

    # Capture baseline image
    image_original = camera.capture()

    # Change gamma
    print(f'Original gamma: {orig_gamma}')
    new_gamma = min(orig_gamma + 20, controls['Gamma']['MaxValue'])
    camera.set_control_value(asi.ASI_GAMMA, new_gamma)
    image_gamma = camera.capture()

    # Restore original gamma
    camera.set_control_value(asi.ASI_GAMMA, orig_gamma)

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

# ==============================================================================
# BINNING DEMONSTRATION
# ==============================================================================

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

    # Capture with the next supported binning mode
    camera.set_roi(bins=supported_bins[1])  # Set to second supported binning mode
    image_bin = camera.capture()
    print(f'Captured image with binning=2, size: {image_bin.shape}')

    # Plot before/after for binning
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im0 = axes[0].imshow(image_no_bin, cmap='gray')
    axes[0].set_title(f'No Binning (1×1)\nSize: {image_no_bin.shape}')
    axes[0].axis('off')
    plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
    im1 = axes[1].imshow(image_bin, cmap='gray')
    axes[1].set_title(f'{supported_bins[1]}x{supported_bins[1]} Binning\nSize: {image_bin.shape}')
    axes[1].axis('off')
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    plt.suptitle('Effects of Binning', fontsize=14)
    fig.tight_layout()
    plt.show(block=False)

    # Restore original binning
    camera.set_roi(bins=1)
else:
    print('Only one binning mode supported. Skipping binning demo.')

# ==============================================================================
# BRIGHTNESS DEMONSTRATION
# ==============================================================================

if has_brightness:
    print('\n' + '=' * 30)
    print('BRIGHTNESS DEMONSTRATION')  
    print('=' * 30)

    # Capture baseline image
    image_original = camera.capture()

    # Change brightness
    print(f'Original brightness: {orig_brightness}')
    new_brightness = min(orig_brightness + 30, controls['Brightness']['MaxValue'])
    camera.set_control_value(asi.ASI_BRIGHTNESS, new_brightness)
    image_brightness = camera.capture()

    # Restore original brightness
    camera.set_control_value(asi.ASI_BRIGHTNESS, orig_brightness)

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

# ==============================================================================
# IMAGE MODE DEMONSTRATION (MONO8 vs MONO16)
# ==============================================================================

print('\n' + '=' * 30)
print('IMAGE MODE DEMONSTRATION')
print('=' * 30)

# Capture in 16-bit mode (current mode)
image_16bit = camera.capture()
print(f'Captured image in 16-bit mode, min: {image_16bit.min()}, max: {image_16bit.max()}')

# Switch to 8-bit mode
camera.set_image_type(asi.ASI_IMG_RAW8)
image_8bit = camera.capture()
print(f'Captured image in 8-bit mode, min: {image_8bit.min()}, max: {image_8bit.max()}')

# Plot comparison of 8-bit vs 16-bit
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
im0 = axes[0].imshow(image_8bit, cmap='gray')
axes[0].set_title('8-bit Mode (RAW8)')
axes[0].axis('off')
plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

im1 = axes[1].imshow(image_16bit, cmap='gray')
axes[1].set_title('16-bit Mode (RAW16)')
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

plt.suptitle('8-bit vs 16-bit Image Modes', fontsize=14)
fig.tight_layout()
plt.show(block=False)

# Restore to 16-bit mode
camera.set_image_type(asi.ASI_IMG_RAW16)

# ==============================================================================
# VIDEO MODE DEMONSTRATION
# ==============================================================================

print('\n' + '=' * 30)
print('VIDEO MODE DEMONSTRATION')
print('=' * 30)

print('Video mode advantages:')
print('- Faster frame rates for live preview')
print('- Continuous streaming capability')  
print('- Lower latency between captures')
print('- Required for auto-exposure/auto-gain features')

# Stop any ongoing exposure and start video mode
camera.stop_exposure()

print('\nStarting video capture mode...')
camera.start_video_capture()

# Capture a series of video frames to show speed
print('\nCapturing video frames...')
frame_times = []
num_frames = 10

start_time = time.time()
for i in range(num_frames):
    frame = camera.capture_video_frame()
end_time = time.time()

avg_frame_time = (end_time - start_time) / num_frames
fps = 1.0 / avg_frame_time
print(f'Approximate frame rate: {fps:.1f} FPS')

# Capture final video frame for display
final_frame = camera.capture_video_frame()

# Stop video mode
camera.stop_video_capture()

# ==============================================================================
# AUTO-EXPOSURE DEMONSTRATION
# ==============================================================================

print('\n' + '=' * 30)
print('AUTO-EXPOSURE DEMONSTRATION')
print('=' * 30)

print('Auto-exposure automatically adjusts exposure time based on image brightness.')
print('This is useful for changing lighting conditions or when you want optimal exposure.')
print('The auto-exposure logic is compiled into the ZWO SDK and cannot be adjusted here.')

# Check if auto-exposure is supported
if 'Exposure' in controls and controls['Exposure']['IsAutoSupported']:
    print('\nAuto-exposure is supported on this camera.')

    # Capture baseline image with manual exposure
    print('\nCapturing image with manual exposure...')
    manual_exposure_image = camera.capture()
    manual_exposure_value = camera.get_control_value(asi.ASI_EXPOSURE)[0]

    # Enable auto-exposure (requires video mode)
    print('Enabling auto-exposure...')
    camera.start_video_capture()
    camera.set_control_value(asi.ASI_EXPOSURE, controls['Exposure']['DefaultValue'], auto=True)

    # Capture several frames to see the adjustment process
    auto_exposure_values = []
    for i in range(10):
        frame = camera.capture_video_frame()
        current_exposure = camera.get_control_value(asi.ASI_EXPOSURE)[0]
        auto_exposure_values.append(current_exposure)
        print(f'Auto-exposure frame {i+1}: {current_exposure} μs')
    time.sleep(2)  # Allow time for auto-exposure to finalize in case it hadn't yet

    # Capture final auto-exposed image
    auto_exposure_image = camera.capture_video_frame()
    final_auto_exposure = camera.get_control_value(asi.ASI_EXPOSURE)[0]

    # Stop video mode
    camera.stop_video_capture()

    # Disable auto-exposure and restore manual control
    camera.set_control_value(asi.ASI_EXPOSURE, DEFAULT_EXPOSURE, auto=False)

    # Show comparison
    print('\nComparison:')
    print(f'  Manual exposure: {manual_exposure_value} μs')
    print(f'  Auto-exposure final: {final_auto_exposure} μs')

    # Plot before/after for auto-exposure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im0 = axes[0].imshow(manual_exposure_image, cmap='gray')
    axes[0].set_title(f'Manual Exposure\n{manual_exposure_value} μs')
    axes[0].axis('off')
    plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
    im1 = axes[1].imshow(auto_exposure_image, cmap='gray')
    axes[1].set_title(f'Auto-Exposure\n{final_auto_exposure} μs')
    axes[1].axis('off')
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    plt.suptitle('Manual vs Auto-Exposure Comparison', fontsize=14)
    plt.tight_layout()
    plt.show(block=False)

else:
    print('\nAuto-exposure is not supported on this camera. Skipping auto-exposure demo.')

# ==============================================================================
# RESTORE ALL SETTINGS
# ==============================================================================

print('\n' + '=' * 30)
print('RESTORING ORIGINAL SETTINGS')
print('=' * 30)

# Restore all original settings
camera.set_control_value(asi.ASI_EXPOSURE, orig_exposure)
camera.set_control_value(asi.ASI_GAIN, orig_gain)

if has_gamma:
    camera.set_control_value(asi.ASI_GAMMA, orig_gamma)

if has_brightness:
    camera.set_control_value(asi.ASI_BRIGHTNESS, orig_brightness)

# Restore original ROI
camera.set_roi(start_x=orig_roi[0], start_y=orig_roi[1], width=orig_roi[2], height=orig_roi[3])

print('All settings have been restored to their original values.')
print('\nAdvanced demo complete!')
