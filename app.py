from decode import decode
from encode import encode
import math
from os import O_EXCL
import PySimpleGUI as sg
import os.path
from PIL import Image
from PySimpleGUI.PySimpleGUI import Element

sg.theme('DarkAmber')  

encoding_densities = ['1x','2x','3x','4x','5x','6x','7x','8x']
image_view_size = 960

encode_data_input = [
    [
        sg.Text("Source Image"),
    ],
    [
        sg.In(size=(50, 1), enable_events=True, key='-ENCODE-SOURCE-'),
        sg.FileBrowse(file_types=(("Image Files", "*.png"),)),
    ],
    [
        sg.Text("Source Data"),
    ],
    [
        sg.In(size=(50, 1), enable_events=True, key="-ENCODE-DATA-"),
        sg.FileBrowse(),
    ],
    [   sg.Text(size=(1, 5))],
    [
        sg.Text("Source Image Size:"),
        sg.Text(size=(20, 1), key="-ENCODE-SOURCE-SIZE-"),
    ],
    [
        sg.Text("Source Image Dimensions:"),
        sg.Text(size=(20, 1), key="-ENCODE-INPUT-IMG-DIMENSIONS-"),
    ],
    [   sg.Text(size=(1, 1))],
    [
        sg.Text("Source Data Size:"),
        sg.Text(size=(20, 1), key="-ENCODE-DATA-SIZE-"),
    ],
    [   sg.Text(size=(1, 1))],
    [
        sg.Text("Adjusted Dimensions:"),
        sg.Text(size=(20, 1), key="-ENCODE-OUTPUT-IMG-DIMENSIONS-"),
    ],
    [   sg.Text(size=(1, 5))],
    [
        sg.Text("Encoding Density"),
    ],
    [
        sg.Combo(values=encoding_densities, size=(20, 1), enable_events=True, default_value='1x', key="-ENCODE-ENCODING-DENSITY-"),
    ],
    [
        sg.Checkbox("Use Minimum Size", enable_events=True, key="-ENCODE-USE-MIN-")
    ],
    [
        sg.Checkbox("Stripe Data", enable_events=True, key="-ENCODE-USE-STRIPE-")
    ],
    [   sg.Text(size=(1, 23))],
    [
        sg.Text("Output Folder"),
    ],
    [
        sg.In(size=(50, 1), enable_events=True, key='-ENCODE-OUTPUT-FOLDER-'),
        sg.FolderBrowse(),
    ],
    [        
        sg.Button('Encode', size=(51, 1), enable_events=True, key='-ENCODE-')
    ]
]

encode_image_input_column = [
    [sg.Image(size=(image_view_size, image_view_size), key="-ENCODE-IMAGE-IN-")],
]

encode_columns = [
    sg.Column(encode_data_input, vertical_alignment='top'),
    sg.VSeperator(),
    sg.Column(encode_image_input_column),
]

decode_data_input = [
    [
        sg.Text("Source Image"),
    ],
    [
        sg.In(size=(50, 1), enable_events=True, key='-DECODE-SOURCE-'),
        sg.FileBrowse(file_types=(("Image Files", "*.png"),)),
    ],
    [   sg.Text(size=(1, 5))],
    [
        sg.Text("Source Image Size:"),
        sg.Text(size=(20, 1), key="-DECODE-SOURCE-SIZE-"),
    ],
    [
        sg.Text("Source Image Dimensions:"),
        sg.Text(size=(20, 1), key="-DECODE-INPUT-IMG-DIMENSIONS-"),
    ],
    [   sg.Text(size=(1, 1))],
    [
        sg.Text("Extracted Data:"),
        sg.Text(size=(30, 1), key="-DECODE-DATA-OUTPUT-"),
    ],
    [
        sg.Text("Extracted Data Size:"),
        sg.Text(size=(20, 1), key="-DECODE-DATA-OUTPUT-SIZE-"),
    ],
    [   sg.Text(size=(1, 39))],
    [
        sg.Text("Output Folder"),
    ],
    [
        sg.In(size=(50, 1), enable_events=True, key='-DECODE-OUTPUT-FOLDER-'),
        sg.FolderBrowse(),
    ],
    [
        sg.Button('Decode', size=(51, 1), enable_events=True, key='-DECODE-')
    ]
]

decode_image_input_column = [
    [sg.Image(size=(image_view_size, image_view_size), key="-DECODE-IMAGE-IN-")],
]

decode_columns = [
    sg.Column(decode_data_input, vertical_alignment='top'),
    sg.VSeperator(),
    sg.Column(decode_image_input_column),
]

encode_tab = [
    encode_columns
]

decode_tab = [
    decode_columns
]

layout = [
    [sg.TabGroup([[sg.Tab('Encode', encode_tab), sg.Tab('Decode', decode_tab)]])]
]

window = sg.Window("Image Encoder/ Decoder", layout)

source = None
data = None
minify = False
suffix = ''
file = ''
output = None
encoding_density = 1
output_dimensions = (0, 0)

def calc_output_dimensions():
    global output_dimensions

    if (not data): return
    if (not source): return

    pixels = (2 * (len(data) + 17)) / encoding_density
    scale_factor = math.sqrt(pixels /(source.width * source.height))

    x = math.ceil(source.width * scale_factor)
    y = math.ceil(source.height * scale_factor)
    if minify: output_dimensions = (x, y)
    else: output_dimensions = (max(x, source.width), max(y, source.height))
    
    window["-ENCODE-OUTPUT-IMG-DIMENSIONS-"].update(output_dimensions)

def resize_image(source):
    resized_image = source.resize((image_view_size, int((image_view_size / source.width) * source.height)))
    resized_image.thumbnail((image_view_size, image_view_size))

    o_x = 0
    o_y = 0

    if (resized_image.width != image_view_size): o_x = int((image_view_size - resized_image.width) / 2)
    if (resized_image.height != image_view_size): o_y = int((image_view_size - resized_image.height) / 2)
    
    background = Image.new("RGBA", (image_view_size, image_view_size), (255, 255, 255, 0))
    background.paste(resized_image, (o_x, o_y))
    return background

try:
    os.mkdir('storage')
except:
    pass

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "-ENCODE-SOURCE-":
        filename = values["-ENCODE-SOURCE-"]
        if filename:
            file = os.path.basename(filename)
            
            source = Image.open(filename)
            resize_image(source).save('storage/input.png')

            window["-ENCODE-INPUT-IMG-DIMENSIONS-"].update(source.size)
            window["-ENCODE-IMAGE-IN-"].update(filename='storage/input.png')
            window["-ENCODE-SOURCE-SIZE-"].update(str(os.stat(filename).st_size/1000) + 'KB')
            calc_output_dimensions()

    if event == "-ENCODE-DATA-":
        filename = values["-ENCODE-DATA-"]
        if filename:
            data = open(filename, 'rb').read()
            suffix = os.path.basename(filename).split('.')[1]

            window["-ENCODE-DATA-SIZE-"].update(str(os.stat(filename).st_size/1000) + 'KB')
            calc_output_dimensions()

    if event == "-ENCODE-ENCODING-DENSITY-":
        encoding_density = int(values["-ENCODE-ENCODING-DENSITY-"].split('x')[0])
        calc_output_dimensions()
    
    if event == "-ENCODE-USE-MIN-":
        minify = values["-ENCODE-USE-MIN-"]
        calc_output_dimensions()

    if event == "-ENCODE-STRIPE-":
        minify = values["-ENCODE-STRIPE-"]
        calc_output_dimensions()

    if event == "-ENCODE-OUTPUT-FOLDER-":
        output = values["-ENCODE-OUTPUT-FOLDER-"]

    if event == "-ENCODE-":
        if source: 
            if data:
                if output:
                    path = output + '/' + file

                    i = 1
                    while (os.path.exists(path)):
                        path = output + '/' + file.split('.')[0] + str(i) + '.' + file.split('.')[1]
                        i += 1

                    encode(source.resize(output_dimensions), data, suffix, encoding_density-1).save(path)
    
    # DECODE LISTENERS

    if event == "-DECODE-SOURCE-":
        filename = values["-DECODE-SOURCE-"]
        if filename:
            file = os.path.basename(filename)

            source = Image.open(filename)
            resize_image(source).save('storage/output.png')
            
            window["-DECODE-INPUT-IMG-DIMENSIONS-"].update(source.size)
            window["-DECODE-IMAGE-IN-"].update(filename='storage/output.png')
            window["-DECODE-SOURCE-SIZE-"].update(str(os.stat(filename).st_size/1000) + 'KB')

    if event == "-DECODE-OUTPUT-FOLDER-":
        output = values["-DECODE-OUTPUT-FOLDER-"]

    if event == "-DECODE-":
        if source:
            if output:
                out = None
                error = None
                try:
                    out = decode(source)
                except:
                    error = 'Decode failed. Possible malformed data.'

                if (error == None):
                    filename = file.split('.')[0] + "." + str(out[1])
                    path = output + '/' + filename

                    i = 1
                    while (os.path.exists(path)):
                        path = output + '/' +  filename.split('.')[0] + str(i) + '.' + filename.split('.')[1]
                        i += 1
            
                    open(path, 'wb').write(out[0])
                    window["-DECODE-DATA-OUTPUT-"].update(filename)
                    window["-DECODE-DATA-OUTPUT-SIZE-"].update(str(os.stat(path).st_size/1000) + 'KB')
                else:
                    window["-DECODE-DATA-OUTPUT-"].update(error)
                    window["-DECODE-DATA-OUTPUT-SIZE-"].update('')

window.close()