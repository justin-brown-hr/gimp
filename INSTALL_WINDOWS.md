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

Your screenshot confirmed the `Scripts` side, but for `Plug-ins` the client should use the exact folder shown in:

- `Edit > Preferences > Folders > Plug-ins`

Depending on how GIMP was installed, people report either:

- `C:\Users\mark\AppData\Roaming\GIMP\3.2\plug-ins`
- or `C:\Users\mark\AppData\Roaming\GIMP\3.0\plug-ins`

For `Scripts`, the screenshot showed:

- `C:\Users\mark\AppData\Roaming\GIMP\3.2\scripts`

For GIMP 3 Python plug-ins, each `.py` file must live in its own same-named subfolder inside whichever `Plug-ins` folder GIMP lists in Preferences.

Use this layout:

```text
<Plug-ins folder shown by GIMP>\
├─ test_plugin\
│  └─ test_plugin.py
└─ montage_overlay\
   └─ montage_overlay.py

C:\Users\mark\AppData\Roaming\GIMP\3.2\scripts\
└─ montage-overlay.scm
```

## Install Steps

1. Close GIMP.
2. Open `Edit > Preferences > Folders > Plug-ins` and note the writable user plug-ins folder GIMP is actually scanning.
3. Create these folders there if they do not already exist:
   - `<that folder>\test_plugin`
   - `<that folder>\montage_overlay`
4. Copy:
   - `test_plugin.py` into `...\test_plugin\`
   - `montage_overlay.py` into `...\montage_overlay\`
5. If you still want the legacy Scheme version, copy `montage-overlay.scm` into:
   - `C:\Users\mark\AppData\Roaming\GIMP\3.2\scripts`
6. Start GIMP again.

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
