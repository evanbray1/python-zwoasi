"""
Bare minimum ZWO ASI camera demo

Assumes ZWO_ASI_LIB environment variable is already set.
Demonstrates basic camera control with minimal overhead.
"""

import os
import zwoasi as asi
import matplotlib.pyplot as plt
from matplotlib import use
use('QtAgg')  # Set an interactive backend. Might need to be changed depending on your system

# Initialize SDK
asi.init()
# asi.init('/path/to/ASICamera2.dll')  # Optionally specify the path to the DLL if it's not in system PATH

# Connect to first camera and set to 16-bit mode
camera = asi.Camera(0)
camera.set_image_type(asi.ASI_IMG_RAW16)

# Capture baseline image
image_baseline = camera.capture()

# Change exposure, gain, and ROI
camera.set_control_value(asi.ASI_EXPOSURE, 1000)  # microseconds
camera.set_control_value(asi.ASI_GAIN, 50)
camera.set_roi(start_x=100, start_y=100, width=200, height=200)
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
