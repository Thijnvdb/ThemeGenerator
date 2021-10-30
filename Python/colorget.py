import cv2
import numpy as np

LIGHT_COUNT = 4
DARK_COUNT = 4
ACCENT_COUNT = 8
LIGHT_PERCENTILE = 1 #what range to sample as the upperbound
DARK_PERCENTILE = 5 #what range to sample as the lowerbound

def getChannelPercentile(x,lower = 95, upper=100, inv = False):
    tp = cv2.THRESH_BINARY
    iv = cv2.THRESH_BINARY_INV
    if inv:
        tp = cv2.THRESH_BINARY_INV
        iv = cv2.THRESH_BINARY
    _x,x_thresholded = cv2.threshold(x, np.percentile(x, lower), np.percentile(x, 100), tp)
    _x,x_thresholded = cv2.threshold(x_thresholded, np.percentile(x,upper),np.percentile(x, 100), iv)
    return x_thresholded

def cluster(image, k=5):
    k += 1 #compensate for mask
    pixel_vals = image.reshape((-1,3))
    # Convert to float type only for supporting cv2.kmean
    pixel_vals = np.float32(pixel_vals) 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85) #criteria
    retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS) 
    centers = np.uint8(centers) # convert data into 8-bit values 
    #segmented_data = centers[labels.flatten()] # Mapping labels to center points( RGB Value)
    #segmented_image = segmented_data.reshape((image.shape)) # reshape data into the original image dimensions
    no_mask = []
    for c in centers:
        if(c.sum() >= 1):
            no_mask.append(c)
    return sortByValue(no_mask)
    

def getColors(image_rgb, saturation, value):
    s = saturation * 3
    s = np.clip(saturation, 0, 255)

    _,s_thresholded = cv2.threshold(s, np.percentile(s, 50), np.percentile(s, 100), cv2.THRESH_BINARY)
    # _,v_thresholded = cv2.threshold(value, np.percentile(value, 50), np.percentile(value, 100), cv2.THRESH_BINARY)
    masked = cv2.bitwise_and(image_rgb, image_rgb, mask=s_thresholded)
    #masked = cv2.bitwise_and(masked, masked, mask=v_thresholded)

    r,g,b = cv2.split(masked)

    r_thresholded = getChannelPercentile(r)
    g_thresholded = getChannelPercentile(g)
    b_thresholded = getChannelPercentile(b)

    mask = cv2.bitwise_or(cv2.bitwise_or(r_thresholded,g_thresholded), b_thresholded)
    masked = cv2.bitwise_and(masked, masked, mask=mask) #mask

    return cluster(masked, ACCENT_COUNT)

# def getLights(image_rgb, image_grey, v):
#     _,light_areas = cv2.threshold(image_grey, np.percentile(image_grey, 100 - LIGHT_PERCENTILE), np.percentile(image_grey, 100), cv2.THRESH_BINARY)
#     light = cv2.bitwise_and(image_rgb,image_rgb,mask=light_areas)
#     _,value_high = cv2.threshold(v, np.percentile(v, 50), np.percentile(v, 100), cv2.THRESH_BINARY)
#     light = cv2.bitwise_and(light,light,mask=value_high)
#     return cluster(light, LIGHT_COUNT)

# def getDarks(image_rgb, image_grey, v):
#     _,dark_areas = cv2.threshold(image_grey, np.percentile(image_grey, DARK_PERCENTILE), np.percentile(image_grey, 100), cv2.THRESH_BINARY_INV)
#     dark = cv2.bitwise_and(image_rgb,image_rgb,mask=dark_areas)
#     _,value_low = cv2.threshold(v, np.percentile(v, 20), 255, cv2.THRESH_BINARY_INV)
#     dark = cv2.bitwise_and(dark,dark,mask=value_low)
#     return cluster(dark, DARK_COUNT)

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


def getScheme(image_url):
    image_rgb = cv2.cvtColor(cv2.imread(image_url), cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV_FULL)
    grey = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    h,s,v = cv2.split(hsv)
    colors = getColors(image_rgb, s, v)
    return rgbArrayToHex(colors)