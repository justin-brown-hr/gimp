# GIMP 3.2 Windows Install Notes

These files are prepared for GIMP `3.2.x` on Windows.

## Use These Files

- `test_plugin.py`
  A simple smoke-test plug-in that creates a red image.
- `montage_overlay.py`
  A GIMP 3 Python plug-in version of the montage workflow.
- `montage-overlay.scm`
  Legacy Script-Fu reference. Keep only if you still want the old Scheme script.

## Exact Install Paths

Your screenshot shows these user folders:

- Scripts: `C:\Users\mark\AppData\Roaming\GIMP\3.2\scripts`
- Plug-ins root: `C:\Users\mark\AppData\Roaming\GIMP\3.2\plug-ins`

For GIMP 3 Python plug-ins, each `.py` file must live in its own same-named subfolder.

Use this layout:

```text
C:\Users\mark\AppData\Roaming\GIMP\3.2\
├─ plug-ins\
│  ├─ test_plugin\
│  │  └─ test_plugin.py
│  └─ montage_overlay\
│     └─ montage_overlay.py
└─ scripts\
   └─ montage-overlay.scm
```

## Install Steps

1. Close GIMP.
2. Create these folders if they do not already exist:
   - `C:\Users\mark\AppData\Roaming\GIMP\3.2\plug-ins\test_plugin`
   - `C:\Users\mark\AppData\Roaming\GIMP\3.2\plug-ins\montage_overlay`
3. Copy:
   - `test_plugin.py` into `...\plug-ins\test_plugin\`
   - `montage_overlay.py` into `...\plug-ins\montage_overlay\`
4. If you still want the legacy Scheme version, copy `montage-overlay.scm` into:
   - `C:\Users\mark\AppData\Roaming\GIMP\3.2\scripts`
5. Start GIMP again.

## Where They Should Appear

After restart, look in:

- `Filters > Mark > Test Python Plugin`
- `Filters > Mark > Montage + Overlay`

If the old Scheme script is installed and still loads, it should also appear under:

- `Filters > Mark`

## Important Notes

- Python plug-ins usually require a full GIMP restart after copying them.
- The old `test_plugin.py` used `gimpfu`, which GIMP 3 does not load. The new file in this folder is already ported to the GIMP 3 API.
- `montage_overlay.py` accepts common raster formats in the input folder: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tif`, `.tiff`, and `.webp`.
- The Python montage plug-in ignores the selected overlay file if it happens to be inside the source folder, so it does not tile the overlay into the grid by mistake.
