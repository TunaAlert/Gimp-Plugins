#!/usr/bin/env python3

#file_nft.py    Saves the image in the Nitrogen Fingers Text format
#               used in ComputerCraft.
#
#               Author: Leona Gatz
#               Date: June 12, 2026
#               Last Update: June 13, 2026

#   file_nft - A GIMP plugin for exporting Nitrogen Fingers Text files
#   Copyright (C) 2026 Leona Gatz
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import Babl
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio

plug_in_save_proc = "plug-in-tunaalert-py3-file-nft-save"
plug_in_load_proc = "plug-in-tunaalert-py3-file-nft-load"
plug_in_binary = "file-nft"

colors = {
    0x0: 0xf0f0f0, #white
    0x1: 0xf2b233, #orange
    0x2: 0xe57fd8, #magenta
    0x3: 0x99b2f2, #light blue
    0x4: 0xdede6c, #yellow
    0x5: 0x7fcc19, #lime
    0x6: 0xf2b2cc, #pink
    0x7: 0x4c4c4c, #gray
    0x8: 0x999999, #light gray
    0x9: 0x4c99b2, #cyan
    0xa: 0xb266e5, #purple
    0xb: 0x3366cc, #blue
    0xc: 0x7f664c, #brown
    0xd: 0x57a64e, #green
    0xe: 0xcc4c4c, #red
    0xf: 0x111111  #black
}

#old chars used for copy-pasting

# chars = {
#     0x00:' ',
#     0x01:'\U0001fb00',
#     0x02:'\U0001fb01',
#     0x03:'\U0001fb02',
#     0x04:'\U0001fb03',
#     0x05:'\U0001fb04',
#     0x06:'\U0001fb05',
#     0x07:'\U0001fb06',
#     0x08:'\U0001fb07',
#     0x09:'\U0001fb08',
#     0x0a:'\U0001fb09',
#     0x0b:'\U0001fb0a',
#     0x0c:'\U0001fb0b',
#     0x0d:'\U0001fb0c',
#     0x0e:'\U0001fb0d',
#     0x0f:'\U0001fb0e',
#     0x10:'\U0001fb0f',
#     0x11:'\U0001fb10',
#     0x12:'\U0001fb11',
#     0x13:'\U0001fb12',
#     0x14:'\U0001fb13',
#     0x15:'\U0000258c',
#     0x16:'\U0001fb14',
#     0x17:'\U0001fb15',
#     0x18:'\U0001fb16',
#     0x19:'\U0001fb17',
#     0x1a:'\U0001fb18',
#     0x1b:'\U0001fb19',
#     0x1c:'\U0001fb1a',
#     0x1d:'\U0001fb1b',
#     0x1e:'\U0001fb1c',
#     0x1f:'\U0001fb1d'
# }

# bg_char = '\U000025b2'
# fg_char = '\U000025bc'

#new chars used for saving

chars = {
    0x00:0x80,
    0x01:0x81,
    0x02:0x82,
    0x03:0x83,
    0x04:0x84,
    0x05:0x85,
    0x06:0x86,
    0x07:0x87,
    0x08:0x88,
    0x09:0x89,
    0x0a:0x8a,
    0x0b:0x8b,
    0x0c:0x8c,
    0x0d:0x8d,
    0x0e:0x8e,
    0x0f:0x8f,
    0x10:0x90,
    0x11:0x91,
    0x12:0x92,
    0x13:0x93,
    0x14:0x94,
    0x15:0x95,
    0x16:0x96,
    0x17:0x97,
    0x18:0x98,
    0x19:0x99,
    0x1a:0x9a,
    0x1b:0x9b,
    0x1c:0x9c,
    0x1d:0x9d,
    0x1e:0x9e,
    0x1f:0x9f
}

bg_char = 0x1e
fg_char = 0x1f

def create_palette():
    if Gimp.Palette.get_by_name("ComputerCraft") == None:
        palette = Gimp.Palette.new("ComputerCraft")
        palette.set_columns(4)
        for i in range(16):
            palette.add_entry("{}".format(i), Gegl.Color.new("#{:6x}".format(colors[i])))

def color_to_index(color):
    data = color.get_data()
    color_int = (data[0] << 16) + (data[1] << 8) + data[2]
    for i in range(16):
        if color_int == colors[i]:
            return i
    return 0

def export_to_nft(procedure, _run_mode, image, file, _options, _metadata, _config, _data, _x):

    create_palette()

    #convert to indexed with colormap defined in colors
    nft_image = image.duplicate()
    nft_image.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)
    if nft_image.get_base_type() == Gimp.ImageBaseType.INDEXED:
        nft_image.convert_rgb()
        nft_image.convert_indexed(Gimp.ConvertDitherType.NONE, Gimp.ConvertPaletteType.CUSTOM, 0, False, False, 'ComputerCraft')
    else:
        nft_image.convert_indexed(Gimp.ConvertDitherType.NONE, Gimp.ConvertPaletteType.CUSTOM, 0, False, False, 'ComputerCraft')
    
    nft_image.resize(
        ((nft_image.get_width()+1)//2)*2,
        ((nft_image.get_height()+2)//3)*3,
        0, 0
        )
    nft_drawable = None
    if len(nft_image.get_layers()) == 0:
        nft_drawable = Gimp.Layer.new(nft_image, "", nft_image.get_width(), nft_image.get_height(), Gimp.ImageType.INDEXED_IMAGE, 1.0, Gimp.LayerMode.NORMAL)
        nft_image.insert_layer(nft_drawable, None, 0)
    else:
        nft_drawable = nft_image.get_layers()[0]
        nft_drawable.resize_to_image_size()

    nft_data = []

    for ty in range((nft_drawable.get_height()+2)//3):
        nft_row = []
        for tx in range((nft_drawable.get_width()+1)//2):
            bgcolorarr = nft_drawable.get_pixel(2*tx+1, 3*ty+2).get_bytes(Babl.format("R'G'B' u8"))
            bgcolor = color_to_index(bgcolorarr)
            i = 0
            fgcolor = bgcolor
            char = 0
            for i in range(5):
                dx = i % 2
                dy = i // 2
                colorarr = nft_drawable.get_pixel(2*tx+dx, 3*ty+dy).get_bytes(Babl.format("R'G'B' u8"))
                color = color_to_index(colorarr)
                if color != bgcolor:
                    fgcolor = color
                    char |= (1 << i)
            nft_row.append([char, fgcolor, bgcolor])
        nft_data.append(nft_row)
    
    stream = file.replace(None, False, Gio.FileCreateFlags.NONE, None)

    format = "utf-8"

    for row in nft_data:
        fg = -1
        bg = -1
        for col in row:
            char = col[0]
            if fg != col[1]:
                fg = col[1]
                stream.write([fg_char])
                stream.write('{:1x}'.format(fg).encode())
            if bg != col[2]:
                bg = col[2]
                stream.write([bg_char])
                stream.write('{:1x}'.format(bg).encode())
            char_byte = chars[char].to_bytes()
            stream.write(char_byte)
        stream.write(b'\n')
    
    stream.close()

    nft_image.delete()

    Gimp.message("Saved file as {} :3".format(file.get_basename()))
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

def import_nft(procedure, _run_mode, file, _metadata, _flags, _config, _data, _x):
    (nft_bytes, error) = file.load_bytes()
    nft_bytes = nft_bytes.get_data()

    image = Gimp.Image.new(2, 3, Gimp.ImageBaseType.INDEXED)
    image.set_palette(Gimp.Palette.get_by_name("ComputerCraft"))

    layer = Gimp.Layer.new(image, file.get_basename(), 2, 3, Gimp.ImageType.INDEXED_IMAGE, 100.0, Gimp.LayerMode.NORMAL)
    image.insert_layer(layer, None, 0)

    tx = 0
    ty = 0
    fg = 0
    bg = 0
    for i in range(len(nft_bytes)):
        b = nft_bytes[i]
        if b == fg_char:
            fg = int(bytes([nft_bytes[i+1]]).decode(), 16)
            i = i+1
        elif b == bg_char:
            bg = int(bytes([nft_bytes[i+1]]).decode(), 16)
            i = i+1
        elif b == b'\n'[0]:
            fg = 0
            bg = 0
            tx = 0
            ty = ty+1
        elif int(b) >= 0x80 and int(b) < 0xa0:
            image.resize(max(image.get_width(), 2*tx+2), max(image.get_height(), 3*ty+3), 0, 0)
            layer.resize_to_image_size()

            for j in range(6):
                color = Gegl.Color.new("#{:6x}".format(colors[bg]))
                if b & (1 << j) != 0:
                    color = Gegl.Color.new("#{:6x}".format(colors[fg]))
                
                layer.set_pixel(2*tx + j % 2, 3*ty + j // 2, color)
            
            tx = tx+1

    Gimp.Display.new(image)

    return_values = procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

    return return_values

class FileNFT (Gimp.PlugIn):
    def do_query_procedures(self):
        return [plug_in_save_proc, plug_in_load_proc]

    def do_create_procedure(self, name):
        procedure = None
        if name == plug_in_save_proc:
            procedure = Gimp.ExportProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, False, export_to_nft, None, None)
            procedure.set_extensions("nft")
            procedure.set_format_name("Nitrogen Fingers Text")
            procedure.set_menu_label("Nitrogen Fingers Text")
        if name == plug_in_load_proc:
            procedure = Gimp.LoadProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, import_nft, None, None)
            procedure.set_extensions("nft")
            procedure.set_format_name("Nitrogen Fingers Text")
            procedure.set_menu_label("Nitrogen Fingers Text")
        return procedure

Gimp.main(FileNFT.__gtype__, sys.argv)
