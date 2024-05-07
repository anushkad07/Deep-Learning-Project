import cv2
import numpy as np
import os

def calculate_colorfulness(image):
    # Convert the image to sRGB color space
    srgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Calculate the pixel cloud along directions (rg, yb)
    rg = srgb_image[:,:,0] - srgb_image[:,:,1]
    yb = (srgb_image[:,:,0] + srgb_image[:,:,1]) / 2 - srgb_image[:,:,2]

    # Calculate the standard deviation and mean value along directions (rg, yb)
    std_rg = np.std(rg)
    std_yb = np.std(yb)
    mean_rg = np.mean(rg)
    mean_yb = np.mean(yb)

    # Calculate ^M(3) colorfulness metric
    colorfulness = np.sqrt(std_rg**2 + std_yb**2) + 0.3 * np.sqrt(mean_rg**2 + mean_yb**2)
    #make colour between 0 and 1
    colorfulness = colorfulness / 200

    return colorfulness