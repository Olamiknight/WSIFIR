""" "
Plotting utilities for WSIFIR.
"""

from ants.core.ants_image import ANTsImage
from matplotlib import pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np
from sidus.tools._math import get_transformed_aabb


# try not to hard code the matplotlib style stuff
# use arguments instead and pass them to the plotting functions
def plot_grouped_bar_chart(df1, df2, title):
    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Set the bar width
    bar_width = 0.35

    # Set the x locations for the bars
    x = np.arange(len(df1))

    # Create the bars for df1
    plt.bar(
        x,
        df1["Mean"],
        yerr=df1["Standard Deviation"],
        width=bar_width,
        label="Initial",
    )

    # Create the bars for df2
    plt.bar(
        x + bar_width,
        df2["Mean"],
        yerr=df2["Standard Deviation"],
        width=bar_width,
        label="Registered",
    )

    # Add labels and title
    plt.xlabel("Metrics")
    plt.ylabel("Values")
    plt.title(title)
    plt.xticks(x + bar_width / 2, df1.index)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


def plot_transformation_panels(
    fixed_image, moving_image, transformed_image, **kwargs
):
    """
    Plot fixed and moving images side by side with transformation overlay.
    """
    if isinstance(fixed_image, ANTsImage):
        fixed_image = fixed_image.numpy()
    #
    fixed_image = fixed_image / np.max(fixed_image)
    fixed_image[fixed_image < 0] = 0
    #
    if isinstance(moving_image, ANTsImage):
        moving_image = moving_image.numpy()
    moving_image = moving_image / np.max(moving_image)
    moving_image[moving_image < 0] = 0
    #
    if isinstance(transformed_image, ANTsImage):
        transformed_image = transformed_image.numpy()
    transformed_image = transformed_image / np.max(transformed_image)
    transformed_image[transformed_image < 0] = 0
    #
    fig, axes = plt.subplots(1, 3, **kwargs)
    # Create an overlay image by stacking the images along the third dimension
    H, W = transformed_image.shape[:2]
    color_image = np.zeros((H, W, 3), dtype=np.float32)
    # Assign channels
    color_image[..., 0] = transformed_image  # Red channel
    color_image[..., 1] = fixed_image  # Green channel
    color_image[..., 2] = fixed_image  # Blue channel
    #
    axes[0].imshow(fixed_image)
    axes[0].set_title("Fixed Image")
    axes[1].imshow(moving_image)
    axes[1].set_title("Moving Image")
    axes[2].imshow(color_image)
    axes[2].set_title("Transformed Image Overlay")
    #
    return fig, axes


def plot_transformed_image(
    fixed_image, transformed_image, fixed_alpha=0.5, transformed_alpha=0.75
):
    """
    Plot the transformed image over the fixed image w specified alpha values.
    """
    fig = plt.figure()
    ax = plt.axes()
    ax.imshow(
        transformed_image.numpy(), cmap="Blues_r", alpha=transformed_alpha
    )
    ax.imshow(fixed_image.numpy(), cmap="Reds_r", alpha=fixed_alpha)
    #
    return fig, ax


def plot_transformation_mpl(
    fixed_image,
    moving_image,
    affine_matrix,
    fixed_alpha=0.5,
    moving_alpha=0.75,
    invert=True,
):
    """
    Transform the moving image with the affine matrix.

    THis is plotted over the fixed image.
    """
    #
    h, w = moving_image.shape[:2]
    extent = get_transformed_aabb(affine_matrix, [0, 0, h, w])
    #
    fig = plt.figure()
    ax = plt.axes()
    #
    im = ax.imshow(
        moving_image.numpy(),
        cmap="Blues_r",
        alpha=moving_alpha,
    )
    ax.imshow(
        fixed_image.numpy(),
        cmap="Reds_r",
        alpha=fixed_alpha,  # extent=[-0.5, 127.5, 127.5, -0.5],
    )
    aff = Affine2D(matrix=affine_matrix)
    if invert:
        aff = aff.inverted()

    im.set_transform(aff + ax.transData)
    # fix coordinates
    ax.set_xlim(extent[0], extent[2])
    ax.set_ylim(extent[3], extent[1])  # y-axis is inverted in images;
    return fig, ax
