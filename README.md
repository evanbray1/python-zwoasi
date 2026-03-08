# python-zwoasi

Python wrapper for the ZWO ASI v2 camera SDK, enabling control and image capture from ZWO USB cameras. This version includes a much more user-friendly wrapper, and improved documentation across the board.

For a version of the manufacturer's repo with ONLY improved documentation (no updated functionality), refer to the branch titled "Improved-documentation-only".

## User-friendly vs original syntax

This fork adds convenience methods so common operations read naturally:

```python
# User-friendly syntax (this fork)
camera.set_exposure(1000)          # microseconds
camera.set_gain(50)
print(camera.get_exposure())       # 1000
print(camera.get_temperature())    # 22.3  (°C, auto-converted to sensible units)

# Original / advanced syntax (still fully supported)
camera.set_control_value(asi.ASI_EXPOSURE, 1000)
camera.set_control_value(asi.ASI_GAIN, 50)
print(camera.get_control_value(asi.ASI_EXPOSURE)[0])  # 1000
```

See `examples/demo_basic.py` for the friendly style and
`examples/demo_advanced.py` for the original style with full SDK access.

## Features

- Simple, object-oriented API
- Capture images and video, adjust common parameters (exposure, gain, gamma, ROI, etc.)
- Clear documentation with step-by-step basic/advanced demos.
- Advanced features such as video mode, auto-exposure, and buffer optimization.

## Quickstart

1. **Install dependencies:**
   - Requires the ZWO ASI SDK
     - V1.39 of the Windows SDK is included here for reference, in case the user doesn't already have it installed in a system-level path.
   - Python 3.6+
   - Common modules such as `numpy`, `Pillow`, `astropy`

2. **Install python-zwoasi:**

   ```bash
   pip install .
   ```

3. **Set up the SDK library:**
   - Set the `ZWO_ASI_LIB` environment variable to the path of your ASICamera2.dll/.so/.dylib, or pass it as an argument to `asi.init()`.

4. **Basic usage:**

   ```python
   import zwoasi as asi
   asi.init()
   cameras = asi.list_cameras()
   if not cameras:
       raise RuntimeError('No cameras found')
   camera = asi.Camera(0)
   img = camera.capture()
   ```

5. **Try the example scripts:**
   - `examples/demo_basic.py` – Minimal example showing most commonly-used features
   - `examples/demo_advanced.py` – Advanced features such as video mode, binning, auto-exposure, and detailed parameter inspection

## Directory Structure

| Path | Description |
|------|-------------|
| `zwoasi/` | Main Python package, all camera logic in `__init__.py` |
| `zwoasi/examples/` | Example scripts demonstrating camera usage |
| `docs/` | Sphinx documentation sources |
| `pyproject.toml` | Build and install configuration |

## Troubleshooting

- Make sure the ZWO ASI SDK library is accessible.
- If you get errors about missing DLL/SO/DYLIB, check the `ZWO_ASI_LIB` path for your system.
- For matplotlib issues, try changing the backend at the top of the demo scripts.
- For more details, see ZWO's official documentation.

## License

MIT License. See `LICENSE` file.
