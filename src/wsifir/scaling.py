import ants
import numpy as np


def compute_scaling_factor(higher_res_scale, lower_res_scale):
    """
    Compute the scaling factor based on the image transformations.
    """
    # Directly compute the scaling factor as a scalar
    return lower_res_scale / higher_res_scale


def scale_transform(transform_path, scaling_factors, fixed_image, moving_image):
    """
    Scale a 2D rigid transformation matrix while preserving rotation components and adjusting translation.

    Parameters:
        transform_path (str): Path to the original transformation matrix (.mat file).
        scaling_factors (list or float): Scaling factors for translation components.
                                         Can be a scalar or a list of 2 values for 2D transformations.
        fixed_image (ants.ANTsImage): The fixed image (reference image).
        moving_image (ants.ANTsImage): The moving image to be transformed.

    Returns:
        str: Path to the scaled transformation matrix.
    """
    try:
        # Read the transformation matrix
        transform = ants.read_transform(transform_path)

        # Ensure the transform is 2D
        if transform.dimension != 2:
            raise ValueError("This function only supports 2D transformations.")

        # Extract the transformation parameters
        parameters = np.array(transform.parameters)

        # Validate scaling_factors
        if isinstance(scaling_factors, (int, float)):
            scaling_factors = [scaling_factors] * 2
        elif len(scaling_factors) != 2:
            raise ValueError(
                "Scaling factors must be a scalar or a list of 2 values for 2D transformations."
            )

        # Scale only the translation components (last two parameters for tx, ty in 2D rigid)
        scaled_parameters = parameters.copy()
        if len(parameters) >= 6:
            scaled_parameters[4] *= scaling_factors[0]
            scaled_parameters[5] *= scaling_factors[1]

            x_shift = (
                fixed_image.origin[0] - moving_image.origin[0]
            ) / scaling_factors[0]
            y_shift = (
                fixed_image.origin[1] - moving_image.origin[1]
            ) / scaling_factors[1]

            scaled_parameters[4] += x_shift
            scaled_parameters[5] += y_shift
        else:
            raise ValueError(
                "Transformation parameters do not have enough components to scale translation."
            )

        # Create a new transform with the scaled parameters
        scaled_transform = ants.create_ants_transform(
            transform_type=transform.type,
            dimension=transform.dimension,
            parameters=scaled_parameters.tolist(),
            fixed_parameters=transform.fixed_parameters,
        )

        # Save the scaled transformation matrix
        scaled_transform_path = transform_path.replace(".mat", "_scaled.mat")
        ants.write_transform(scaled_transform, scaled_transform_path)

        return scaled_transform_path

    except Exception as e:
        raise RuntimeError(f"Error scaling transform: {e}") from e
