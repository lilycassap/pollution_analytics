import numpy as np
from matplotlib import pyplot as mat_plot


def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Reads an image file, finds all the red pixels, returns a 2D array in numpy representing the output binary 
    image and writes the 2D array into a file named map-red-pixels.jpg.

    Parameters:
        map_filename (str): string containing the required filename
        upper_threshold (int): integer representing the min value for the red pixels
        lower_threshold (int): integer representing the max value for the green and blue pixels
    Returns:
        Saves output black and white image to map-red-pixels.jpg
        red_pixels_binary (np array): 2D numpy array representing the black and white pixels
    """

    # Read and format specified file
    map = mat_plot.imread(f'data\{map_filename}')
    map *= 255

    red_pixels = []
    red_pixels_binary = []

    for row in map:
        row_pixels = []
        row_pixels_binary = []
        for pixel in row:
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]

            # Check colour of pixel
            if r > upper_threshold and g < lower_threshold and b < lower_threshold:
                # If it is red, add white pixel
                row_pixels.append([255, 255, 255])
                row_pixels_binary.append(1)
            else:
                # If not red, add black pixel
                row_pixels.append([0, 0, 0])
                row_pixels_binary.append(0)
        red_pixels.append(row_pixels)
        red_pixels_binary.append(row_pixels_binary)
    
    red_pixels = np.array(red_pixels)
    red_pixels_binary = np.array(red_pixels_binary)

    # Save output image
    mat_plot.imsave('map-red-pixels.jpg', red_pixels/255)
    return red_pixels_binary



def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Reads an image file, finds all the cyan pixels, returns a 2D array in numpy representing the output binary 
    image and writes the 2D array into a file named map-cyan-pixels.jpg.

    Parameters:
        map_filename (str): string containing the required filename
        upper_threshold (int): integer representing the min value for the green and blue pixels
        lower_threshold (int): integer representing the max value for the red pixels
    Returns:
        Saves output black and white image to map-cyan-pixels.jpg
        cyan_pixels_binary (np array): 2D numpy array representing the black and white pixels
    """

    # Read and format specified file
    map = mat_plot.imread(f'data\{map_filename}')
    map *= 255

    cyan_pixels = []
    cyan_pixels_binary = []

    for row in map:
        row_pixels = []
        row_pixels_binary = []
        for pixel in row:
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]

            # Check colour of pixel
            if r < lower_threshold and g > upper_threshold and b > upper_threshold:
                # If it is cyan, add white pixel
                row_pixels.append([255, 255, 255])
                row_pixels_binary.append(1)
            else:
                # If not cyan, add black pixel
                row_pixels.append([0, 0, 0])
                row_pixels_binary.append(0)

        cyan_pixels.append(row_pixels)
        cyan_pixels_binary.append(row_pixels_binary)
    
    cyan_pixels = np.array(cyan_pixels)
    cyan_pixels_binary = np.array(cyan_pixels_binary)

    # Save output image
    mat_plot.imsave('map-cyan-pixels.jpg', cyan_pixels/255)
    return cyan_pixels_binary



def detect_connected_components(IMG): 
    """
    Uses the connected components algorithm, reads a binary 2D image array IMG, returns a 2D array in numpy MARK 
    and writes the number of pixels inside each connected component region into a text file cc-output-2a.txt.
    
    Parameters:
        IMG (np array): 2D numpy array representing a binary black and white image
    Returns:
        Writes connected components to file
        MARK (np array): 2D numpy array containing either 0 (unvisited) or the component number (visited)
    """

    # Set all elements in MARK as unvisited ie 0
    MARK = np.zeros(IMG.shape) 

    # Create an empty queue like ndarray Q to hold coordinates as a list in the form [y,x] 
    Q = np.empty((0, 2))  

    component_num = 1

    f = open('cc-output-2a.txt', 'w')

    # Iterate through each pixel of IMG
    for y in range(len(IMG)):
        for x in range(len(IMG[0])):     

            pixel_num = 0          

            # Check if current pixel is white and unvisited
            if IMG[y][x] == 1 and not MARK[y][x]: 

                # Set pixel as visited by replacing the 0 with the component num
                MARK[y][x] = component_num  

                # Add pixel to queue
                Q = np.append(Q, np.array([[y, x]]), axis=0)  
                pixel_num += 1

                while len(Q) > 0:
                    q = Q[0]

                    # Remove first pixel (q) of queue
                    Q = np.delete(Q, 0, 0)  

                    # Find all the neighbours of q:
                    neighbours = []

                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            y_coord = q[0] + i
                            x_coord = q[1] + j

                            # Check if the neighbouring pixels are within the bounds of the image
                            if x_coord >= 0 and y_coord >= 0 and x_coord < IMG.shape[1] and y_coord < IMG.shape[0]:
                                neighbours.append([y_coord, x_coord])
                    
                    for neighbour in neighbours:
                        y_coord = int(neighbour[0])
                        x_coord = int(neighbour[1])
                        
                        # Check if current pixel is white and unvisited
                        if IMG[y_coord][x_coord] == 1 and not MARK[y_coord][x_coord]:

                            # Mark pixel as visited
                            MARK[y_coord][x_coord] = component_num  

                            # Add pixel to queue
                            Q = np.append(Q, np.array([[y_coord, x_coord]]), axis=0)

                            # New pixel found so increment by one
                            pixel_num += 1 
 
                component_num += 1
                f.write(f'Connected Component {component_num-1}, number of pixels = {pixel_num}\n')

    f.write(f'Total number of connected components = {component_num-1}')
    f.close()

    return MARK



def detect_connected_components_sorted(MARK):
    """
    Reads MARK and writes all connected components in decreasing order into a text file cc-output-2b.txt, and
    writes the top two largest connected components into a file named as cc-top-2.jpg.

    Parameters:
        MARK (np array): 2D numpy array containing either 0 (unvisited) or the component number (visited)
    Returns:
        Writes sorted components to text file
        Saves jpg image of top two components
    """
    
    lst = []

    with open('cc-output-2a.txt') as f: 
        for line in f:
            line = line.strip().split()
            
            try:
                # Add component number and pixel number to list
                lst.append([int(line[2][:-1]), int(line[7])])
            except:
                pass
    
    # Extract total number of components from file
    total = lst[-1][0]

    # Insertion sort:
    for i in range(1, len(lst)):
        temp = lst[i]
        j = i

        # Move item until it is in the correct place
        while j > 0 and lst[j-1][1] < temp[1]:
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = temp
    
    with open('cc-output-2b.txt', 'w') as f:
        for row in lst:
            f.write(f'Connected Component {row[0]}, number of pixels = {row[1]}\n')
        f.write(f'Total number of connected components = {total}')
    

    top_two = []

    # Iterate through each pixel in MARK
    for y in range(len(MARK)):
        top_two_row = []
        for x in range(len(MARK[0])):

            # Look for top two components in file
            if MARK[y][x] == lst[0][0] or MARK[y][x] == lst[1][0]:
                # If found, add a white pixel
                top_two_row.append([255, 255, 255])
            else:
                # Otherwise, add a black pixel
                top_two_row.append([0, 0, 0])
        
        top_two.append(top_two_row)
    
    top_two = np.array(top_two)
    mat_plot.imsave('cc-top-2.jpg', top_two/255)


