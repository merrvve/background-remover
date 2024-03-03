import rembg
import numpy as np
from PIL import Image
import cv2
import skimage.exposure


def remove_bg(image_cv, output_path):
    # Load the input image
    #input_image = Image.open(image_path)
    input_image = image_cv
    # Convert the input image to a numpy array
    #input_array = np.array(input_image)

    # Apply background removal using rembg
    output_image = rembg.remove(input_image,
                                #alpha_matting=True,
                                #alpha_matting_foreground_threshold=200,  # Experiment with different values
                                #alpha_matting_background_threshold=30,  # Experiment with different values
                                #alpha_matting_erode_size=15,
                                only_mask=True,
                                post_process_mask=True)
                             

    # Create a PIL Image from the output array
    #output_image = Image.fromarray(output_array)

    # Save the output image
    #output_image.save(output_path)

    cv2.imwrite(output_path,output_image)
    return output_image

def convert_white_to_transparent(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[2] == 3:  # If image is in RGB format, convert to RGBA
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    # Split the image into channels
    b, g, r, alpha = cv2.split(image)
    
    # Create a mask where #ffffff pixels are set to 0 (black)
    mask = cv2.inRange(image, (255, 255, 255, 255), (255, 255, 255, 255))
    
    # Invert the mask (where #ffffff pixels are now set to 255)
    mask = cv2.bitwise_not(mask)
    
    # Apply the mask to the alpha channel
    alpha = cv2.bitwise_and(alpha, alpha, mask=mask)
    
    # Merge the channels back together
    result = cv2.merge((b, g, r, alpha))
    
    # Save the resulting image
    cv2.imwrite(output_path, result)



def apply_mask(original_image, mask, output_path):

    # Convert the original image to RGBA if it's in RGB format
    if original_image.shape[2] == 3:
        original_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2RGBA)

    # Ensure that the mask is in grayscale
    if mask.ndim == 3 and mask.shape[2] == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)

    
    # Convert the mask to binary (black to transparent, white to opaque)
    #_, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    # Normalize mask values to range [0, 1]
    normalized_mask = mask.astype(np.float32) / 255.0

    # Invert the binary mask (black to opaque, white to transparent)
    #inverted_mask = cv2.bitwise_not(binary_mask)

    # Split the original image into channels
    b, g, r, alpha = cv2.split(original_image)

# Convert alpha channel to float32 for arithmetic operations
    alpha = alpha.astype(np.float32)

    # Apply the mask to the alpha channel with different levels of transparency
    alpha = cv2.multiply(alpha, normalized_mask)
  # Keep transparent pixels transparent by combining with the original alpha channel
    alpha = cv2.addWeighted(alpha, 1.0, alpha, 0.0, 0)

    # Convert alpha channel back to uint8
    alpha = np.clip(alpha, 0, 255).astype(np.uint8) 
 # Apply the inverted mask to the alpha channel
    #alpha = cv2.bitwise_and(alpha, alpha, mask=mask)

    # Merge the channels back together
    result = cv2.merge((b, g, r, alpha))

    # Save the resulting image
    cv2.imwrite(output_path, result)
    return result


def blur_edges(input_cv, output_image):

# load image
    img = input_cv

    # blur threshold image
    blur = cv2.GaussianBlur(img, (0,0), sigmaX=3, sigmaY=3, borderType = cv2.BORDER_DEFAULT)

    # stretch so that 255 -> 255 and 127.5 -> 0
    # C = A*X+B
    # 255 = A*255+B
    # 0 = A*127.5+B
    # Thus A=2 and B=-127.5
    #aa = a*2.0-255.0 does not work correctly, so use skimage
    result = skimage.exposure.rescale_intensity(blur, in_range=(127.5,255), out_range=(0,255))

    # save output
    cv2.imwrite(output_image, result)
    return result

def get_lasso_selection_pixels(image, coordinates):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    points = np.array([coordinates], dtype=np.int32)
    cv2.fillPoly(mask, [points], 255)
    selected_pixels = cv2.bitwise_and(image, image, mask=mask)
    #selected_pixels = cv2.bitwise_not(selected_pixels)
    return selected_pixels
def lasso_select(image, seed_point, tolerance=20):


    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to create a mask of the region of interest
    _, mask = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    
    # Copy the mask to keep the original intact
    lasso_mask = mask.copy()
    
    # Define the flood fill parameters
    h, w = image.shape[:2]
    mask_fill = np.zeros((h+2, w+2), np.uint8)
    flags = 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8)  # Use mask only
    
    # Get the color value of the seed point
    seed_color = image[seed_point[1], seed_point[0]].tolist()
    
    # Perform flood fill from the seed point
    cv2.floodFill(image, mask_fill, seed_point, (255,255,255), (tolerance,)*3, (tolerance,)*3, flags)
    
    # Extract the flood fill result from the mask
    floodfill_mask = mask_fill[1:-1, 1:-1]
    
    # Combine the flood fill result with the original mask
    lasso_mask = cv2.bitwise_and(lasso_mask, floodfill_mask)
    
    # Invert the mask
    lasso_mask = cv2.bitwise_not(lasso_mask)
    
    # Return the lasso-selected area
    return lasso_mask

def get_white_pixels(image):
    # Find white pixel coordinates
    white_pixels = np.argwhere((image[..., :3] == [255, 255, 255]).all(axis=2) & (image[..., 3] == 255))
    # Convert coordinates to tuples
    white_pixels_tuples = [tuple(coord) for coord in white_pixels]

    return white_pixels_tuples

inputim ='IMG_0027.jpg'
input_cv = cv2.imread(inputim)
removed_cv = remove_bg(input_cv,'output_image.png')
removed_cv = blur_edges(removed_cv,'bw_image_antialiased.png')
removed_cv = apply_mask(input_cv,removed_cv,'out2.png')
removed_cv=cv2.imread('out2.png')
im=Image.open('out2.png')
im_array=np.array(im)
wp = get_white_pixels(im_array)
a,b=wp[len(wp)//2]
lasso = lasso_select(removed_cv,(b,a))
lasso = blur_edges(lasso,'lasso.png')
removed_cv=cv2.imread('out2.png', cv2.IMREAD_UNCHANGED)
apply_mask(removed_cv,lasso,'son.png')
sonim=Image.open('out2.png')
bg = Image.new('RGBA', sonim.size, (0,100,0,255))
bg.paste(sonim,(0,0),sonim)
bg.save('son-bg.png')                    
