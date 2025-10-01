# Copilot Instructions for python-zwoasi

## Project Purpose & Structure
- **Goal:** Python bindings for the ZWO ASI v2 camera SDK, enabling control and image capture from ZWO USB cameras.
- **Core logic:** All camera interaction is in `zwoasi/__init__.py` (single-module design, no submodules).
  - Uses `ctypes` to wrap the ZWO C SDK (DLL/SO/DYLIB).
  - Exposes camera enumeration, initialization, control, and image capture.
  - Custom exceptions: `ZWO_Error`, `ZWO_IOError`, `ZWO_CaptureError`.
- **Examples:**
  - `zwoasi/examples/zwoasi_demo.py` (deprecated): Basic camera usage and image capture.
  - `zwoasi/examples/binning_demo.py`: Demonstrates binning and video capture.
  - `zwoasi/examples/zwoasi_feature_demo.py`: Shows parameter changes and FITS image saving (requires `astropy`).

## Developer Workflows
- **Build/install:**
  - Use `pip install .` from the repo root (uses `setuptools`, see `setup.py`, `pyproject.toml`).
- **Running examples:**
  - Requires ZWO ASI SDK shared library (not bundled).
  - Set path via `ZWO_ASI_LIB` environment variable or pass as CLI argument.
  - Example: `python zwoasi/examples/zwoasi_demo.py /path/to/ASICamera2.dll`
- **Testing:**
  - No formal test suite. Validate via example scripts.
- **Docs:**
  - Sphinx docs in `docs/`. Build with `cd docs && make html` (Linux/macOS) or `make.bat html` (Windows).

## Key Patterns & Conventions
- **ctypes usage:** All SDK calls are wrapped with error checking and custom exceptions.
- **No type hints:** Classic Python style, no type annotations.
- **No test/CI folder:** Manual testing only.
- **No package data:** Only Python code is packaged (see `pyproject.toml`).
- **Image arrays:** Always named `image` in examples.
- **FITS output:** Images saved as FITS using `astropy.io.fits` (not PNG/JPG).

## Integration & Dependencies
- **External:** Requires ZWO ASI SDK (user must provide DLL/SO/DYLIB).
- **Python:** Only dependency is `numpy` (see `pyproject.toml`).
- **Optional:** `astropy` for FITS output in feature demo.

## Quick Reference
- **Initialize SDK:** `asi.init('/path/to/ASICamera2.dll')`
- **List cameras:** `asi.list_cameras()`
- **Open camera:** `camera = asi.Camera(camera_id)`
- **Capture:** Use `camera.capture()` or video methods as in examples.

## Upstream & Further Info
- For missing features, see [camera_zwo_asi](https://github.com/MPI-IS/camera_zwo_asi).
- For SDK details, see ZWO's official documentation.
