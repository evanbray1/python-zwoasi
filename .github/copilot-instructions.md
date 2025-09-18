# Copilot Instructions for python-zwoasi

## Project Overview
- **Purpose:** Python bindings for the ZWO ASI v2 camera SDK, enabling control and image capture from ZWO USB cameras.
- **Origin:** Forked from [MPI-IS/camera_zwo_asi](https://github.com/MPI-IS/camera_zwo_asi). This repo may have less documentation but similar structure.

## Architecture & Key Components
- **Core logic:** All camera interaction is in `zwoasi/__init__.py`.
  - Wraps the ZWO C SDK using `ctypes`.
  - Exposes functions for camera enumeration, initialization, control, and image capture.
  - Custom exceptions: `ZWO_Error`, `ZWO_IOError`, `ZWO_CaptureError`.
- **Examples:**
  - `zwoasi/examples/zwoasi_demo.py`: End-to-end camera usage, initialization, and image capture.
  - `zwoasi/examples/binning_demo.py`: Demonstrates binning and video capture.

  - `zwoasi/examples/zwoasi_feature_demo.py`: Demonstrates camera parameter changes and image capture. Images are saved as FITS files using `astropy.io.fits` (not PNG/JPG). The variable name for image arrays is `image` throughout.

  - **Note:** To run the feature demo, install `astropy` (`pip install astropy`).

## Developer Workflows
- **Build/install:**
  - Standard Python build via `setuptools` (`setup.py`, `pyproject.toml`).
  - Install with `pip install .` from the repo root.
- **Running examples:**
  - Requires the ZWO ASI SDK shared library (DLL/SO/DYLIB).
  - Set the path via the `ZWO_ASI_LIB` environment variable or pass as a CLI argument.
  - Example: `python zwoasi/examples/zwoasi_demo.py /path/to/ASICamera2.dll`
- **Testing:**
  - No formal test suite included. Use example scripts for manual validation.
- **Docs:**
  - Sphinx docs in `docs/`. Build with `cd docs && make html` (Linux/macOS) or `make.bat html` (Windows).

## Project Conventions & Patterns
- **No submodules:** All logic is in `zwoasi/__init__.py`.
- **ctypes usage:** All SDK calls are wrapped with error checking and custom exceptions.
- **No type hints:** Code is written in classic Python style.
- **No test/CI folder:** Testing is manual via examples.
- **No package data:** Only Python code is packaged (see `pyproject.toml`).

## Integration & Dependencies
- **External:** Requires ZWO ASI SDK (not bundled).
- **Python:** Only dependency is `numpy` (see `pyproject.toml`).

## Quick Reference
- **Initialize SDK:** `asi.init('/path/to/ASICamera2.dll')`
- **List cameras:** `asi.list_cameras()`
- **Open camera:** `camera = asi.Camera(camera_id)`
- **Capture:** Use `camera.capture()` or video methods as in examples.

## See Also
- For more detailed docs or missing features, refer to the upstream [camera_zwo_asi](https://github.com/MPI-IS/camera_zwo_asi).
- For SDK details, see ZWO's official documentation.
