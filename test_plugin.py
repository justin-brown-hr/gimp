#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import gi

gi.require_version("Gegl", "0.4")
gi.require_version("Gimp", "3.0")

from gi.repository import Gegl, GLib, Gimp

Gegl.init(None)

PLUGIN_NAME = "python-fu-test-plugin"


class TestPlugin(Gimp.PlugIn):
    def do_query_procedures(self):
        return [PLUGIN_NAME]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None,
        )

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Test Python Plugin")
        procedure.add_menu_path("<Image>/Filters/Mark/")
        procedure.set_documentation(
            "Creates a simple red image to confirm Python plug-ins work in GIMP 3.",
            "Creates a 400x200 image with a solid red layer and opens it in a new display.",
            name,
        )
        procedure.set_attribution("Mark's Copilot", "Mark's Copilot", "2026")

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        try:
            image = Gimp.Image.new(400, 200, Gimp.ImageBaseType.RGB)
            layer = Gimp.Layer.new(
                image,
                "Test Layer",
                400,
                200,
                Gimp.ImageType.RGBA_IMAGE,
                100.0,
                Gimp.LayerMode.NORMAL,
            )

            image.insert_layer(layer, None, 0)

            Gimp.context_push()
            try:
                Gimp.context_set_foreground(Gegl.Color.new("red"))
                layer.fill(Gimp.FillType.FOREGROUND)
            finally:
                Gimp.context_pop()

            Gimp.Display.new(image)
            return procedure.new_return_values(
                Gimp.PDBStatusType.SUCCESS,
                GLib.Error(),
            )
        except Exception as exc:
            return procedure.new_return_values(
                Gimp.PDBStatusType.EXECUTION_ERROR,
                GLib.Error.new_literal(
                    Gimp.PlugIn.error_quark(),
                    f"Failed to create the test image: {exc}",
                    0,
                ),
            )


Gimp.main(TestPlugin.__gtype__, sys.argv)
