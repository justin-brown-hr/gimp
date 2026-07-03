#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

import gi

gi.require_version("Gimp", "3.0")

from gi.repository import Gio, GLib, Gimp, GObject

PLUGIN_NAME = "python-fu-montage-overlay"
SUPPORTED_EXTENSIONS = {
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


class MontageOverlayPlugin(Gimp.PlugIn):
    def do_query_procedures(self):
        return [PLUGIN_NAME]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.Procedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None,
            None,
        )

        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Montage + Overlay")
        procedure.add_menu_path("<Image>/Filters/Mark/")
        procedure.set_documentation(
            "Creates a montage from a folder of images and overlays another image.",
            "Builds a new montage image from source files, scales each one into a grid, "
            "adds the overlay on top, and opens the result in a new display.",
            name,
        )
        procedure.set_attribution("Mark's Copilot", "Mark's Copilot", "2026")
        procedure.add_file_argument(
            "input-folder",
            "Input Folder",
            "Folder containing the source images for the montage",
            Gimp.FileChooserAction.SELECT_FOLDER,
            False,
            None,
            GObject.ParamFlags.READWRITE,
        )
        procedure.add_file_argument(
            "overlay-image",
            "Overlay Image",
            "Image to place on top of the finished montage",
            Gimp.FileChooserAction.OPEN,
            False,
            None,
            GObject.ParamFlags.READWRITE,
        )
        procedure.add_int_argument(
            "cell-width",
            "Cell Width",
            "Width of each montage cell in pixels",
            1,
            20000,
            400,
            GObject.ParamFlags.READWRITE,
        )
        procedure.add_int_argument(
            "cell-height",
            "Cell Height",
            "Height of each montage cell in pixels",
            1,
            20000,
            600,
            GObject.ParamFlags.READWRITE,
        )
        procedure.add_int_argument(
            "columns",
            "Columns",
            "Number of columns in the montage grid",
            1,
            1000,
            10,
            GObject.ParamFlags.READWRITE,
        )
        procedure.add_int_argument(
            "overlay-opacity",
            "Overlay Opacity",
            "Overlay opacity as a percentage from 0 to 100",
            0,
            100,
            50,
            GObject.ParamFlags.READWRITE,
        )

        return procedure

    def _error(self, procedure, message, status=Gimp.PDBStatusType.EXECUTION_ERROR):
        return procedure.new_return_values(
            status,
            GLib.Error.new_literal(Gimp.PlugIn.error_quark(), message, 0),
        )

    def _resolve_path(self, file_arg):
        if file_arg is None:
            return None
        path = file_arg.get_path()
        if not path:
            return None
        return Path(path)

    def _collect_source_images(self, input_folder, overlay_path):
        overlay_real = overlay_path.resolve() if overlay_path else None
        images = []

        for candidate in sorted(input_folder.iterdir()):
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if overlay_real is not None and candidate.resolve() == overlay_real:
                continue
            images.append(candidate)

        return images

    def _insert_scaled_layer(self, montage, file_path, width, height, x, y, opacity=None):
        layers = Gimp.file_load_layers(
            Gimp.RunMode.NONINTERACTIVE,
            montage,
            Gio.File.new_for_path(str(file_path)),
        )
        if not layers:
            raise RuntimeError(f"Could not load '{file_path.name}' as a layer.")

        layer = layers[0]
        montage.insert_layer(layer, None, 0)
        layer.scale(width, height, True)
        layer.set_offsets(x, y)
        if opacity is not None:
            layer.set_opacity(float(opacity))
        return layer

    def run(self, procedure, config, *_run_data):
        input_folder = self._resolve_path(config.get_property("input-folder"))
        overlay_path = self._resolve_path(config.get_property("overlay-image"))
        cell_width = int(config.get_property("cell-width"))
        cell_height = int(config.get_property("cell-height"))
        columns = int(config.get_property("columns"))
        overlay_opacity = int(config.get_property("overlay-opacity"))

        if input_folder is None or not input_folder.is_dir():
            return self._error(
                procedure,
                "Input Folder must point to an existing folder.",
                Gimp.PDBStatusType.CALLING_ERROR,
            )

        if overlay_path is None or not overlay_path.is_file():
            return self._error(
                procedure,
                "Overlay Image must point to an existing image file.",
                Gimp.PDBStatusType.CALLING_ERROR,
            )

        if columns < 1 or cell_width < 1 or cell_height < 1:
            return self._error(
                procedure,
                "Cell size and column count must be greater than zero.",
                Gimp.PDBStatusType.CALLING_ERROR,
            )

        image_paths = self._collect_source_images(input_folder, overlay_path)
        if not image_paths:
            return self._error(
                procedure,
                "No supported source images were found in the selected folder.",
                Gimp.PDBStatusType.CALLING_ERROR,
            )

        rows = (len(image_paths) + columns - 1) // columns
        montage_width = columns * cell_width
        montage_height = rows * cell_height

        try:
            montage = Gimp.Image.new(
                montage_width,
                montage_height,
                Gimp.ImageBaseType.RGB,
            )

            background = Gimp.Layer.new(
                montage,
                "Montage Background",
                montage_width,
                montage_height,
                Gimp.ImageType.RGBA_IMAGE,
                100.0,
                Gimp.LayerMode.NORMAL,
            )
            background.fill(Gimp.FillType.TRANSPARENT)
            montage.insert_layer(background, None, 0)

            for index, image_path in enumerate(image_paths):
                x = (index % columns) * cell_width
                y = (index // columns) * cell_height
                layer = self._insert_scaled_layer(
                    montage,
                    image_path,
                    cell_width,
                    cell_height,
                    x,
                    y,
                )
                layer.set_name(image_path.stem)

            overlay_layer = self._insert_scaled_layer(
                montage,
                overlay_path,
                montage_width,
                montage_height,
                0,
                0,
                opacity=overlay_opacity,
            )
            overlay_layer.set_name("Overlay")

            merged_layer = montage.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)
            if merged_layer is not None:
                merged_layer.set_name("Montage + Overlay")

            Gimp.Display.new(montage)
            return procedure.new_return_values(
                Gimp.PDBStatusType.SUCCESS,
                GLib.Error(),
            )
        except Exception as exc:
            return self._error(
                procedure,
                f"Failed to build the montage: {exc}",
                Gimp.PDBStatusType.EXECUTION_ERROR,
            )


Gimp.main(MontageOverlayPlugin.__gtype__, sys.argv)
