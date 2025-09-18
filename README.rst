python-zwoasi
=============

Python bindings for the ZWO ASI v2 camera SDK, enabling control and image capture from ZWO USB cameras.

Features
--------
- Enumerate, initialize, and control ZWO ASI cameras from Python
- Capture images and video, adjust camera parameters (exposure, gain, gamma, ROI, etc.)
- Simple, object-oriented API

Quickstart
----------
1. **Install dependencies:**
	- Requires the ZWO ASI SDK (download from ZWO website)
	- Python 3.6+
	- `numpy`, `Pillow`, `astropy`

2. **Install python-zwoasi:**
	::
		pip install .

3. **Set up the SDK library:**
	- Set the `ZWO_ASI_LIB` environment variable to the path of your ASICamera2.dll/.so/.dylib, or pass it as an argument to `asi.init()`.

4. **Basic usage:**
	::
		import zwoasi as asi
		asi.init() 
		cameras = asi.list_cameras()
		if not cameras:
			 raise RuntimeError('No cameras found')
		camera = asi.Camera(0)
		img = camera.capture()

5. **See `examples/zwoasi_feature_demo.py` for a demo of fundamental camera operations.**
	- For example, how to connect to the camera, change the image type, and change common parameters like exposure length.

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
- If you get errors about missing DLL/SO/DYLIB, check the `ZWO_ASI_LIB` path.
- For more details, see ZWO's official documentation.

License
-------
MIT License. See `LICENSE` file.

