python-zwoasi
=============

Python wrapper for the ZWO ASI v2 camera SDK, enabling control and image capture from ZWO USB cameras.

Features
--------
- Simple, object-oriented API
- Capture images and video, adjust common parameters (exposure, gain, gamma, ROI, etc.)
- Clear documentation with step-by-step basic/advanced demos.
- Advanced features such as video mode, auto-exposure, and buffer optimization. 

Quickstart
----------
1. **Install dependencies:**
	- Requires the ZWO ASI SDK 
		- V1.39 of the Windows SDK is included here for reference, in case the user doesn't already have it installed in a system-level path. 
	- Python 3.6+
	- Common modules such as `numpy`, `Pillow`, `astropy`

2. **Install python-zwoasi:**

   .. code-block:: bash

      pip install .

3. **Set up the SDK library:**
	- Set the `ZWO_ASI_LIB` environment variable to the path of your ASICamera2.dll/.so/.dylib, or pass it as an argument to `asi.init()`.

4. **Basic usage:**

   .. code-block:: python

      import zwoasi as asi
      asi.init() 
      cameras = asi.list_cameras()
      if not cameras:
          raise RuntimeError('No cameras found')
      camera = asi.Camera(0)
      img = camera.capture()

5. **Try the example scripts:**
	- `examples/demo_basic.py` - Minimal example showing most commonly-used features
	- `examples/demo_advanced.py` - Advanced features such as video mode, binning, auto-exposure, and detailed parameter inspection

Directory Structure
-------------------

- `zwoasi/`           : Main Python package, all camera logic in `__init__.py`
- `zwoasi/examples/`  : Example scripts demonstrating camera usage
- `docs/`             : Sphinx documentation sources
- `misc/`             : Miscellaneous files (e.g., udev rules)
- `setup.py`, `pyproject.toml` : Build and install configuration

Troubleshooting
---------------
- Make sure the ZWO ASI SDK library is accessible.
- If you get errors about missing DLL/SO/DYLIB, check the `ZWO_ASI_LIB` path for your system.
- For matplotlib issues, try changing the backend at the top of the the demo scripts.
- For more details, see ZWO's official documentation.

License
-------
MIT License. See `LICENSE` file.

