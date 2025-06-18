"""
utilities for the package
"""

from typing import Union

import ants
import numpy as np
import pandas as pd
from spatialdata.models import Image2DModel


def _validate_scale(scale: Union[int, str]) -> str:
    x_str = str(scale)
    if not x_str.startswith("scale"):
        x_str = "scale" + x_str
    return x_str


def ants_from_sdata(image: Image2DModel, scale: Union[int, str]):
    """
    Extract spatialdata image to an ANTsImage with the specified scale.

    We need to validate this is a datatree and set the origin
    and spacing correctly.

    Args:
        image: The input image element from a spatialdata object.
        scale: The scale from the image xarray to use.

    Returns:
        ants.ANTsImage: The converted ANTsImage.
    """
    scale = _validate_scale(scale)
    numpy_image = np.array(image[scale].image[0].compute())
    return ants.from_numpy(numpy_image)


def get_affine_matrix_from_ants(ants_transform) -> np.ndarray:
    """
    Extract the affine transformation matrix from an ANTs transform object.

    Transform in ants is centered around a center point, the form is described
    in the ANTs documentation:
    https://github.com/ANTsX/ANTsPy/wiki/ANTs-transform-concepts-and-file-formats

    Args:
        ants_transform: ANTs transform object.

    Returns:
        np.ndarray: 2D affine transformation matrix.
    """

    if isinstance(ants_transform, str):
        ants_transform = ants.read_transform(ants_transform)

    if ants_transform.dimension != 2:
        raise ValueError("This function only supports 2D transformations.")

    # Extract the parameters and reshape them into a 3x3 matrix
    params = ants_transform.parameters
    center = ants_transform.fixed_parameters + 1
    # center = np.array((128 / 2, 128 / 2))
    #
    a = params[:4].reshape(2, 2)
    t = params[4:]
    b = t + center - a @ center
    #
    transform = np.eye(3)
    transform[:2, :2] = a
    transform[:2, 2] = b
    # x and y are swapped in the ANTs transform
    rotation = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    #
    return rotation @ transform @ rotation


def get_affine_table(fixed_image_id, moving_image_id, scale, affine_matrix):
    """
    Create a DataFrame with the affine transformation matrix.

    Args:
        fixed_image_id: ID of the fixed image.
        moving_image_id: ID of the moving image.
        scale: Scale name.
        affine_matrix: 2D affine transformation matrix.

    Returns:
        pd.DataFrame: DataFrame containing the affine transformation parameters.
    """
    affine_parameters = pd.DataFrame(
        [affine_matrix.flatten()[:6]], columns=["a", "b", "tx", "c", "d", "ty"]
    )
    affine_labels = pd.DataFrame(
        [[fixed_image_id, moving_image_id, str(scale)]],
        columns=["fixed_image_id", "moving_image_id", "scale"],
    )
    #
    return pd.concat([affine_labels, affine_parameters], axis=1)


def _get_scaling_matrix(image, scale: Union[int, str]) -> float:
    """
    Get the scale factor for a given image and scale.

    Args:
        image: The input image element from a spatialdata object.
        scale: The scale from the image xarray to use.

    Returns:
        float: The scale factor.
    """
    scale = _validate_scale(scale)
    return (
        image[scale]
        .image.transform["global"]
        .to_affine_matrix(("x", "y"), ("x", "y"))
    )


def _scale_affine_matrix(
    affine_matrix: np.ndarray, source, target
) -> np.ndarray:
    """
    Scale an affine transformation matrix based on source and target images.
    Args:
        affine_matrix (np.ndarray): The original affine transformation matrix.
        source: The source image (reference image).
        target: The target image to be transformed.
    Returns:
        np.ndarray: The scaled affine transformation matrix.
    """
    mask = (source != 0) & (target != 0)
    result = np.zeros_like(source, dtype=float)
    result[mask] = source[mask] / target[mask]
    #
    return result @ affine_matrix @ np.linalg.inv(result)


def _get_ants_from_affine(
    A: np.ndarray, tform_path="./scaled_transform.txt"
) -> np.ndarray:
    """
    Recover ANTs transform parameters from a full 3x3 affine matrix,
    assuming the transform was centered at (0, 0) and wrapped with
    ANTs-style x/y axis swap.

    Parameters:
        A (np.ndarray): 3x3 affine matrix (wrapped with rotation swap)

    Returns:
        np.ndarray: ANTs-style parameters: [a00, a01, a10, a11, t0, t1]
    """
    # ANTs uses swapped x/y axes for 2D images
    rotation = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])

    # Unwrap the coordinate swap
    unrotated = rotation @ A @ rotation

    a = unrotated[:2, :2]
    t = unrotated[:2, 2]  # b = t when center = 0
    tform = ants.create_ants_transform(matrix=a, translation=t, dimension=2)
    ants.write_transform(tform, tform_path)
    return tform_path


def get_scaled_ants_transform(
    affine_matrix: np.ndarray,
    fixed_image,
    source_scale,
    target_scale,
    tform_path="./scaled_transform.txt",
) -> str:
    """
    Scale an affine transformation matrix based on source and target images,
    and return the path to the ANTs transform file.

    Args:
        affine_matrix (np.ndarray): The original affine transformation matrix.
        source: The source image (reference image).
        target: The target image to be transformed.
        tform_path (str): Path to save the scaled ANTs transform.

    Returns:
        str: Path to the scaled ANTs transform file.
    """
    source_scale = _get_scaling_matrix(fixed_image, source_scale)
    target_scale = _get_scaling_matrix(fixed_image, target_scale)
    scaled_matrix = _scale_affine_matrix(
        affine_matrix, source_scale, target_scale
    )
    #
    return (
        _get_ants_from_affine(scaled_matrix, tform_path=tform_path),
        scaled_matrix,
    )
