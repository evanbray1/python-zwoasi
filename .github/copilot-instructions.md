# Copilot Instructions for python-zwoasi

## Project Purpose & Structure
- **Goal:** Python bindings for the ZWO ASI v2 camera SDK, enabling control and image capture from ZWO USB cameras.
- **Core logic:** All camera interaction is in `zwoasi/__init__.py` (single-module design, no submodules).
  - Uses `ctypes` to wrap the ZWO C SDK (DLL/SO/DYLIB).
  - Exposes camera enumeration, initialization, control, and image capture.
  - Custom exceptions: `ZWO_Error`, `ZWO_IOError`, `ZWO_CaptureError`.
- **Examples (Updated Demo Suite):**
  - `zwoasi/examples/demo_basic.py`: Streamlined introduction with minimal setup and interactive plotting.
  - `zwoasi/examples/demo_advanced.py`: Comprehensive feature tour including video mode, buffer optimization, and auto-exposure.

## Developer Workflows
- **Build/install:**
  - Use `pip install .` from the repo root (uses `setuptools`, see `setup.py`, `pyproject.toml`).
- **Running examples:**
  - Requires ZWO ASI SDK shared library (Windows x64 DLL included in `zwoasi/lib/`).
  - Set path via `ZWO_ASI_LIB` environment variable or use auto-detection.
  - **New demo progression:** `demo_basic.py` → `demo_advanced.py` for comprehensive learning.
  - **Interactive features:** All demos use matplotlib with live plotting and user prompts.
- **Testing:**
  - No formal test suite. Validate via example scripts.
  - New demos include visual verification through side-by-side image comparisons.
- **Docs:**
  - Sphinx docs in `docs/`. Build with `cd docs && make html` (Linux/macOS) or `make.bat html` (Windows).

## Key Patterns & Conventions
- **ctypes usage:** All SDK calls are wrapped with error checking and custom exceptions.
- **No type hints:** Classic Python style, no type annotations.
- **No test/CI folder:** Manual testing only.
- **No package data:** Only Python code is packaged (see `pyproject.toml`).
- **Image arrays:** Always named `image` in examples.
- **FITS output:** Images saved as FITS using `astropy.io.fits` (not PNG/JPG).
- **Interactive demos:** New examples use `plt.ion()` for live plotting with `input()` prompts between sections.
- **Visual feedback:** Side-by-side comparisons with colorbars for parameter change demonstrations.

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
