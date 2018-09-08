import sys
from skimage import color,io, data
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage
import random
from scipy.spatial import Voronoi, voronoi_plot_2d

import matplotlib.pyplot as plt


#Step 1 :Reading image
rgb_img = io.imread(sys.argv[1])
print(rgb_img[0][0])

print("shape {}".format(rgb_img.shape))

def imagePreProcessing():
    #Step 1.1: color conversion rgb to colorlab
    # lab = color.rgb2lab(img)
    # print(lab.shape)


    #Step 2: Get feature point

    #Step 2.1: greyscaling image to get the edges
    greyscaled = color.rgb2grey(rgb_img)

    #Step 2.2: Convolving image with filter to get edge
    filter = np.array([[1,0,-1],
                       [1,0,-1],
                       [1,0,-1]])
    convolved_image = ndimage.convolve(greyscaled,filter)
    convolved_image[convolved_image > 0.5] = 255.0

    #returns points which could be part of sample
    return np.argwhere(convolved_image>0)

def getFeatures(n):
    # n - number of points to select
    #Step3: Fetch points from convolved image for sampling
    allPoint = imagePreProcessing()

    # using Poisson Process to select random points

    # TO-DO: Use sobol or halton quasirandom process to select points or
    #        use adaptive mesh refinement to select points
    count = 0
    selectedPoints = []
    while len(allPoint) and count < n :
        inx = int(random.expovariate(1)*len(allPoint))%len(allPoint)
        selectedPoints.append(allPoint[inx])
        allPoint = np.delete(allPoint, inx, 0)
        count = count+1

    return selectedPoints

def delaunayTriangle(n):
    #Step4: Create vornoi diagram

    #Step 4.1: Form the base
    selectedPoints = np.array(getFeatures(n))
    vor = Voronoi(selectedPoints)

    #Step 4.2: Color the base

    #Step 4.2.1: mapping the color
    
    polygons  = []
    voronoi_plot_2d(vor)
    flag=1
    print(len(vor.vertices))
    for region in vor.regions:
        polygon = []
        if -1 not in region:
            for i in region:
                temp = vor.vertices[i]
                temp = np.array(temp)
                polygon.append(temp.astype(int))
            polygons.append(polygon)
    # polygons = np.array(polygons)
    # polygons = polygons.astype(int)
    base = Image.new('RGB',(350,350), (0,0,0))
    global drw
    drw = ImageDraw.Draw(base,'RGB')
    for coordinate in polygons:
    	if coordinate:
            y = coordinate[0][0]%350
            x = coordinate[0][1]%350
            global color
            coord = []
            for i  in range(len(coordinate)):
            	coord.append(tuple(coordinate[i]))
            color = rgb_img[x][y]

            color = np.append(color, [1])
            color =tuple(color)
            drw.polygon(coord, color, None)
    base.show()
    plt.show()

def main():
    delaunayTriangle(500)

if __name__ == '__main__':
    main()