from ants.core.ants_image import ANTsImage
from matplotlib import pyplot as plt
from matplotlib.transforms import Affine2D
import numpy as np
import pandas as pd
from typing import Union
from sidus.tools._math import get_transformed_aabb
import ipywidgets
import scyjava as sj

sj.config.add_options("-Xmx6g")  # Set max heap size to 6GB
import imagej

# Initialize Fiji
ij = imagej.init("sc.fiji:fiji", mode="interactive")


# try not to hard code the matplotlib style stuff
# use arguments instead and pass them to the plotting functions
def plot_grouped_bar_chart(df1: pd.DataFrame, df2: pd.DataFrame, title: str):
    """
    Plot a grouped bar chart with error bars.
    Args:
        df1 (pd.DataFrame): DataFrame containing the first set of data
        with 'Mean' and 'Standard Deviation' columns.
        df2 (pd.DataFrame): DataFrame containing the second set of data
        with 'Mean' and 'Standard Deviation' columns.
        title (str): Title for the plot.

    Returns:
        None: Displays the plot directly.

    Raises:
        ValueError: If the DataFrames do not have the same index
        or if they do not contain 'Mean' and 'Standard Deviation' columns.
    """
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
    fixed_image: ANTsImage,
    moving_image: ANTsImage,
    transformed_image: ANTsImage,
    **kwargs,
):
    """
    Plot fixed and moving images side by side with transformation overlay.

    Args:
        fixed_image (ANTsImage): The fixed image.
        moving_image (ANTsImage): The moving image.
        transformed_image (ANTsImage): The transformed image.
        **kwargs: Additional keyword arguments for matplotlib's subplots.
    Returns:
        fig (matplotlib.figure.Figure): The figure object containing the plot.
        axes (list of matplotlib.axes.Axes): The axes objects for the plot.

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
    fixed_image: ANTsImage,
    transformed_image: ANTsImage,
    fixed_alpha=0.5,
    transformed_alpha=0.75,
):
    """
    Plot the transformed image over the fixed image w specified alpha values.

    Args:
        fixed_image (ANTsImage): The fixed image.
        transformed_image (ANTsImage): The transformed image.
        fixed_alpha (float): Alpha value for the
        fixed image overlay. Default is 0.5.
        transformed_alpha (float): Alpha value for
        the transformed image overlay. Default is 0.75.

    Returns:
        fig (matplotlib.figure.Figure): The figure object containing the plot.
        ax (matplotlib.axes.Axes): The axes object for the plot.

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
    fixed_image: ANTsImage,
    moving_image: ANTsImage,
    affine_matrix: np.ndarray,
    fixed_alpha=0.5,
    moving_alpha=0.75,
    invert=True,
):
    """
    Transform the moving image with the affine matrix. This is plotted over the fixed image.

    Args:
        fixed_image (ANTsImage): The fixed image.
        moving_image (ANTsImage): The moving image.
        affine_matrix (np.ndarray): The affine transformation matrix.
        fixed_alpha (float): Alpha value for the fixed image overlay. Default is 0.5.
        moving_alpha (float): Alpha value for the moving image overlay. Default is 0.75.
        invert (bool): Whether to invert the affine transformation. Default is True.

    Returns:
        fig (matplotlib.figure.Figure): The figure object containing the plot.
        ax (matplotlib.axes.Axes): The axes object for the plot.


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


def plane(image: Union[ANTsImage], pos: dict) -> ANTsImage:
    """
    Slices an image plane at the given position.
    Args:
        image (ANTsImage): The image to slice.
        pos (dict): A dictionary mapping dimension names to slice positions.
                    For example, {'x': 10, 'y': 20} will slice at x=10 and y=20.

    Returns:
        ANTsImage: The sliced image plane.

    Raises:
        ValueError: If the position dictionary does not match the image dimensions.

    """
    # Convert pos dictionary to position indices in dimension order.
    # See https://stackoverflow.com/q/39474396/1207769.
    p = tuple(
        pos[image.dims[d]] if image.dims[d] in pos else slice(None)
        for d in range(image.ndim)
    )
    return image[p]


def _axis_index(image: Union[ANTsImage], *options: str) -> int:
    """
    Get the index of the first axis in the image that matches one of the given options.
    Args:
        image (ANTsImage): The image to check.
        options (str): Axis labels to match against the image dimensions.
    Returns:
        int: The index of the first matching axis.
    Raises:
        ValueError: If no matching axis is found.
    """
    axes = tuple(
        d for d in range(image.ndim) if image.dims[d].lower() in options
    )
    if len(axes) == 0:
        raise ValueError(f"Image has no {options[0]} axis!")
    return axes[0]


def ndshow(
    image: Union[ANTsImage],
    cmap=None,
    x_axis=None,
    y_axis=None,
    immediate=False,
):
    """
    Display a multi-dimensional image with interactive sliders for non-planar dimensions.
    Args:
        image (ANTsImage): The image to display, must have dimensional axis labels.
        cmap: Colormap to use for displaying the image.
        x_axis: Optional; index of the x-axis (default is first 'x' or 'col' dimension).
        y_axis: Optional; index of the y-axis (default is first 'y' or 'row' dimension).
        immediate: If True, updates the display immediately when sliders are moved.
    Raises:
        TypeError: If the image does not have dimensional axis labels.
        ValueError: If no matching axis is found for x or y.

    """
    if not hasattr(image, "dims"):
        # We need dimensional axis labels!
        raise TypeError("Metadata-rich image required")

    # Infer X and/or Y axes as needed.
    if x_axis is None:
        x_axis = _axis_index(image, "x", "col")
    if y_axis is None:
        y_axis = _axis_index(image, "y", "row")

    # Build ipywidgets sliders, one per non-planar dimension.
    widgets = {}
    for d in range(image.ndim):
        if d == x_axis or d == y_axis:
            continue
        label = image.dims[d]
        widgets[label] = ipywidgets.IntSlider(
            description=label,
            max=image.shape[d] - 1,
            continuous_update=immediate,
        )

    # Create image plot with interactive sliders.
    def recalc(**kwargs):
        print("displaying")
        ij.py.show(plane(image, kwargs), cmap=cmap)

    ipywidgets.interact(recalc, **widgets)
