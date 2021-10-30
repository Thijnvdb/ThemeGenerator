import cv2
import numpy as np
from numpy.lib.type_check import imag

def cluster(image, k, unique=True):
    pixel_vals = image.reshape((-1,3))
    #get only unique colors in image
    if(unique):
        pixel_vals = np.unique(pixel_vals, axis=0)
    # Convert to float type only for supporting cv2.kmean
    pixel_vals = np.float32(pixel_vals) 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85) #criteria
    retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS) 
    centers = np.uint8(centers) # convert data into 8-bit values 
    #segmented_data = centers[labels.flatten()] # Mapping labels to center points( RGB Value)
    #segmented_image = segmented_data.reshape((image.shape)) # reshape data into the original image dimensions
    return sortByValue(centers)

def sortByValue(colors_rgb, inverted=False):
    s = sorted(colors_rgb, key=lambda arr: [np.sum(arr)])
    if inverted:
        return np.flip(s);
    return s

def rgbArrayToHex(rgb_array):
    res = []
    for entry in rgb_array:
        res.append('#{:02x}{:02x}{:02x}'.format( entry[0], entry[1] , entry[2] ))
    return res


def getScheme(image_url, clusters = 8):
    image_rgb = cv2.cvtColor(cv2.imread(image_url), cv2.COLOR_BGR2RGB)
    colors = cluster(image_rgb, clusters)
    return rgbArrayToHex(colors)