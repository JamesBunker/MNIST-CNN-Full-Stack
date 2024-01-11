import mxarr;

header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n
<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg"\n
xmlns:xlink="http://www.w3.org/1999/xlink">\n"""
footer = """</svg>\n"""
pxsize = 10

# function to create svg images from yann lecun data
def svg(arr):
    svg_output = []
    text = """ <rect x="%d" y="%d" width="10" height="10" fill="#%02x%02x%02x" />\n"""
    svg_output.append(header % (280,280))
    # iterating through array and adding pixel data to svg template
    for i in range(arr.getdim(0)):
        for j in range(arr.getdim(1)):
            try:
                pixel = int(arr[j,i])
            except:
                pixel = 0
            svg_output.append(text % (i*pxsize,j*pxsize,pixel,pixel,pixel))
    svg_output.append(footer)

    # returning svg file as string
    ret = ""
    for x in svg_output:
        ret += x
    return ret

# function to graph file as svg file
def graph(arr, xlabels, ylabels, xoff, yoff, xscale, yscale):
    # file template strings
    svg_graph_output = []
    line_axis = """<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:rgb(0,0,0);stroke-width:4" />\n"""
    axis_label = ["""<text text-anchor="%s" x="%d" y="%d">""","%s", "</text>\n"]
    line_data = """<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:rgb(0,0,255);stroke-width:2" />\n"""

    # file header
    svg_graph_output.append(header % (700,450))

    # y-axis line
    svg_graph_output.append(line_axis % (50,25,50,425))

    # x-axis line
    svg_graph_output.append(line_axis % (50,425,650,425))

    counter = 425

    # y-axis labels
    for y in ylabels:
        svg_graph_output.append(axis_label[0] % ("end",45,counter))
        svg_graph_output.append(axis_label[1] % (y))
        svg_graph_output.append(axis_label[2])
        counter -= 100

    counter = 50

    # x-axis labels
    for x in xlabels:
        svg_graph_output.append(axis_label[0] % ("middle",counter,445))
        svg_graph_output.append(axis_label[1] % (x))
        svg_graph_output.append(axis_label[2])
        counter += 150

    xy_val_prev = (0.0,0.0)

    # iterating though columns to set connections between points
    for j in range(arr.getdim(1)):
        xy_val_cur = ((arr[0,j]+xoff)*xscale + 50,(arr[1,j]+yoff)*yscale*-1 + 425)
        if j == 0:
            xy_val_prev = xy_val_cur
        else:
            svg_graph_output.append(line_data % (xy_val_prev[0],xy_val_prev[1],xy_val_cur[0],xy_val_cur[1]))
        xy_val_prev = xy_val_cur

    svg_graph_output.append(footer)

    # returning graph output as a string
    ret = ""
    for x in svg_graph_output:
        ret += x
    return ret

# helper function to get array from file with index
def get_arr(file, index):
    fp = mxarr.fopen( file, "r" )
    data = mxarr.readarray( fp )
    mxarr.fclose( fp )
    return data.getmatrix(index)

# helper function to get array from file
def load_arr(file):
    fp = mxarr.fopen( file, "r" )
    data = mxarr.readarray( fp )
    mxarr.fclose( fp )
    return data
     
# function to graph file as svg file
def lazygraph(path, xlabels, ylabels, xoff, yoff, xscale, yscale):
    x_values = []
    y_values = []
    f = open(path, "r")
    lines = f.readlines()

    for line in lines:
        x_values.append(float(line.split(": ")[0]))
        y_values.append(float(line.split(": ")[1]))
    f.close()

    # file template strings
    svg_graph_output = []
    line_axis = """<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:rgb(0,0,0);stroke-width:4" />\n"""
    axis_label = ["""<text text-anchor="%s" x="%d" y="%d">""","%s", "</text>\n"]
    line_data = """<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:rgb(0,0,255);stroke-width:2" />\n"""

    # file header
    svg_graph_output.append(header % (700,450))

    # y-axis line
    svg_graph_output.append(line_axis % (50,25,50,425))

    # x-axis line
    svg_graph_output.append(line_axis % (50,425,650,425))

    counter = 425

    # y-axis labels
    for y in ylabels:
        svg_graph_output.append(axis_label[0] % ("end",45,counter))
        svg_graph_output.append(axis_label[1] % (y))
        svg_graph_output.append(axis_label[2])
        counter -= 100


    # x-axis labels
    for x in xlabels:
        svg_graph_output.append(axis_label[0] % ("middle",325,445))
        svg_graph_output.append(axis_label[1] % (x))
        svg_graph_output.append(axis_label[2])

    xy_val_prev = (0.0,0.0)

    # iterating though columns to set connections between points
    for j in range(len(y_values)):
        xy_val_cur = (((j+xoff)*xscale + 55),((y_values[j]+yoff)*yscale*-1 + 425))
        if j == 0:
            xy_val_prev = xy_val_cur
            svg_graph_output.append(line_data % (xy_val_prev[0],xy_val_prev[1],xy_val_cur[0],xy_val_cur[1]))

        else:
            svg_graph_output.append(line_data % (xy_val_prev[0],xy_val_prev[1],xy_val_cur[0],xy_val_cur[1]))
        xy_val_prev = xy_val_cur

    svg_graph_output.append(footer)

    # returning graph output as a string
    ret = ""
    for x in svg_graph_output:
        ret += x
    return ret