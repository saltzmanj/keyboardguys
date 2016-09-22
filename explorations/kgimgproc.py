import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.draw import line
import skimage.transform as skt
import matplotlib.patches as mpatches

BLK_COLOR = 0
WHT_COLOR = 255
PLOT_BUFFER = 10
SEGMENTATION_BUFFER = 5

def array_assign_list(ndarray_in, indexlist, value = 1):
    """ Assigns a single value to a disparate list of indices in a numpy array """
    for l in indexlist:
        ndarray_in[(l[0],l[1])] = value
    return ndarray_in

def gen_feature_matrix(dataframe_in, note_id, dims = [300, 450], idfieldname = 'id', dim_names= ['x1f','x2f'], stroke_name = "stroke", interpolate = True):
    """ Generates an image from a list of points in a pandas dataframe. """
    for key in dim_names:
        if key not in dataframe_in.keys():
            raise KeyError("Could not find column name '" + str(key) + "' in input DataFrame")
            
    if note_id not in dataframe_in[idfieldname].unique():
        raise KeyError(str(note_id) + " is not a member of column '" + str(idfieldname) +"'")
        
    if idfieldname not in dataframe_in.keys():
        raise KeyError("Could not find column name '" + str(idfieldname) + "' in input DataFrame")
        
    dfsubset = dataframe_in[dataframe_in[idfieldname] == note_id] # Get the note's data
    
    x1 =list( dfsubset[dim_names[0]])
    x2 = list(dfsubset[dim_names[1]])
    strk = list(dfsubset[stroke_name])
    # print(len(x1))
    # print(len(x2))
    # Converts dataframe columns to a list of points
    indexlist = [[x2[j], x1[j]] for j in range(0,len(x1)-1)]
    
    # Initialize the output array
    outputX = np.ones((dims[0], dims[1])) * WHT_COLOR
#     print(indexlist[1:5])

    # If interpolation is enabled, draw a "line" between each sequential pair of points
    if interpolate:
        for k in range(1,len(indexlist) - 2):
            if strk[k] != strk[k+1]:
                continue
            pt1 = indexlist[k]
            pt2 = indexlist[k+1]
            
            # Use SciKit Image's line drawing function
            rr, cc = line(pt1[0], pt1[1], pt2[0], pt2[1])
            
            outputX[rr,cc] = BLK_COLOR
    else:        
        outputX = array_assign_list(outputX, indexlist, BLK_COLOR)

    return outputX

def plot_image(dataframe_in, note_id, dims = [300, 450], dim_names = ['x1f','x2f'], idfieldname = 'id', notetypefieldname = 'y', interpolate = True):
    """Plots a note with a red detection box around it"""
    f = gen_feature_matrix(dataframe_in, note_id, dims, interpolate = interpolate)
    
    dfsubset = dataframe_in[dataframe_in[idfieldname] == note_id]
    
    x1min = min(dfsubset[dim_names[0]]) - PLOT_BUFFER
    x1max = max(dfsubset[dim_names[0]]) + PLOT_BUFFER
    
    x2min = min(dfsubset[dim_names[1]]) - PLOT_BUFFER
    x2max = max(dfsubset[dim_names[1]]) + PLOT_BUFFER
    
    
    t1 = dfsubset[idfieldname].unique()
    t2 = dfsubset[notetypefieldname].unique()
    tstring = str(t1) + " : " + str(t2)
    
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    fig.suptitle(tstring)
    rect = mpatches.Rectangle((x1min, x2min),  x1max - x1min, x2max - x2min,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)
    ax.imshow(f, cmap='Greys_r', interpolation = "nearest")

def segment_image(dataframe_in, note_id, dims = [300, 450], dim_names = ['x1f','x2f'], idfieldname = 'id', sizeout = [40, 40]):
    """ Segments a note into a standard image with set dimension"""
    f = gen_feature_matrix(dataframe_in, note_id, dims = [300, 450], interpolate = True)
    dfsubset = dataframe_in[dataframe_in[idfieldname] == note_id]
    
    x1min = min(dfsubset[dim_names[0]]) - SEGMENTATION_BUFFER
    x1max = max(dfsubset[dim_names[0]]) + SEGMENTATION_BUFFER
    
    x2min = min(dfsubset[dim_names[1]]) - SEGMENTATION_BUFFER
    x2max = max(dfsubset[dim_names[1]]) + SEGMENTATION_BUFFER
    
    subimg = f[x2min:x2max, x1min:x1max]
    scaledimage = skt.resize(subimg, sizeout)
    return scaledimage
