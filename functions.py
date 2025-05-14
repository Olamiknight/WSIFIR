import numpy as np

def pad_images_to_same_size(images):
    """
    Pads all images in the input dictionary to the same size.

    Parameters:
        images (dict): A dictionary where keys are sample IDs and values are NumPy arrays representing images.

    Returns:
        dict: A dictionary with the same keys as the input, but with images padded to the same size.
    """
    # Validate input
    if not isinstance(images, dict):
        raise ValueError("Input 'images' must be a dictionary.")
    if not all(isinstance(img, np.ndarray) for img in images.values()):
        raise ValueError("All values in 'images' must be NumPy arrays.")
    if len(images) == 0:
        return {}

    # Ensure all images have the same number of dimensions
    first_image_shape = next(iter(images.values())).shape
    if not all(img.ndim == len(first_image_shape) for img in images.values()):
        raise ValueError("All images must have the same number of dimensions.")

    # Get the maximum dimensions
    max_shape = np.max([img.shape for img in images.values()], axis=0)

    # Pad each image to the maximum dimensions
    padded_images = {}
    for sampleid, img in images.items():
        pad_width = [(0, max_dim - img_dim) for img_dim, max_dim in zip(img.shape, max_shape)]
        padded_images[sampleid] = np.pad(img, pad_width, mode='constant', constant_values=0)

    return padded_images