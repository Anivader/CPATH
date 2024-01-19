#import pyvips   # create image pyramid from tiles
from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tifffile as tiff   # we want to write/handle our images as "TIFF"
import glob
import os

# #Load the slide file (svs) into an object.
# slide = open_slide("/Users/anirudhgangadhar/Desktop/UHN_Postdoc/Datasets/Liver_biopsy_patient_images/104.svs")
# # print(slide.properties)

### Save normalized image tiles at all levels for all patient WSIs
# We also want to sort the images into "Strong_signal" and "Weak_signal"

def svs_2_imgs(dir_svs, dir_saveimgs):

    # Get list of all patient WSIs
    dir_name = dir_svs
    wsi_img_list=(glob.glob(dir_name + "*.svs"))

    # Change path to wherever you want to store the image tiles
    os.chdir(dir_saveimgs)
    for i in range(len(wsi_img_list)): 
    
        # if we want to test for 1 WSI case 
    #     if i == 3:
    #         break
    
        # Get WSI filename w/o extension - we will use this to name folders
        filename_noext = os.path.splitext(os.path.basename(wsi_img_list[i]))[0]
    
        # Create unique folder for patient
        parent_dir = dir_saveimgs
        directory = filename_noext
        path = os.path.join(parent_dir, directory)
    
        # check if directory exists already - if so don't create new directory
        if os.path.exists(path) == False:
        
            print('Saving images for quantitative analysis ...')
            os.mkdir(path)
    
            # Create sub-folders for different tile levels
            # Read WSI image
            slide = open_slide(wsi_img_list[i])
    
            tile_sz = 256
            tiles = DeepZoomGenerator(slide, tile_size=tile_sz, overlap=0, limit_bounds=False)
            num_levels = tiles.level_count
        
            # Create folder for each tile level
            for j in range(15):  # All levels will generate too may images
                cols, rows = tiles.level_tiles[j]
                # First, create unique folder for each tile level
                path_level = os.path.join(path, '%d' % j)
                os.mkdir(path_level)
            
                # create sub-folders for segregating tile images
                parent_dir_level = path_level
                directory_level_1, directory_level_2 = 'High_signal', 'Low_signal'
                path_level_seg_1 = os.path.join(parent_dir_level, directory_level_1)
                path_level_seg_2 = os.path.join(parent_dir_level, directory_level_2)
                os.mkdir(path_level_seg_1)
                os.mkdir(path_level_seg_2)
            
                # Saving image tiles at each level
                for row in range(rows):
                    for col in range(cols):
                        tile_name = os.path.join(path_level, '%s_%d_%d' % (filename_noext, col, row))
                        temp_tile = tiles.get_tile(j, (col, row))
                        temp_tile_np = np.array(temp_tile.convert('RGB'))
                        plt.imsave(tile_name + ".tiff", temp_tile_np)
                    
    #                     image = tiff.imread(tile_name)
                        # use SD to filter
                        if (temp_tile_np.std() >= 10):
                            tile_name_1 = os.path.join(path_level_seg_1, '%s_%d_%d' % (filename_noext, col, row))
                            plt.imsave(tile_name_1 + ".tiff", temp_tile_np)
                        else:
                            tile_name_2 = os.path.join(path_level_seg_2, '%s_%d_%d' % (filename_noext, col, row))
                            plt.imsave(tile_name_2 + ".tiff", temp_tile_np)
            print('WSI imageset created !')
        else:
            print('Folder already exists !!')