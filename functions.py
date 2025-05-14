
import numpy as np
import ants

def pad_images_to_same_size(images):
    # Get the maximum dimensions
    max_shape = np.max([img.shape for img in images.values()], axis=0)

    # Pad each image to the maximum dimensions
    padded_images = {}
    for sampleid, img in images.items():
        pad_width = [(0, max_dim - img_dim) for img_dim, max_dim in zip(img.shape, max_shape)]
        padded_images[sampleid] = np.pad(img, pad_width, mode='constant', constant_values=0)
    return padded_images

def convert_to_ants_images(padded_images):
    """
    Converts a dictionary of padded images to ANTs images.
    """
    padded_images_ants = {}
    for sampleid, padded_image in padded_images.items():
        padded_images_ants[sampleid] = ants.from_numpy(padded_image)
    return padded_images_ants