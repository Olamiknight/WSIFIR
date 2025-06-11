import ants
import pandas as pd
import SimpleITK as sitk
from sklearn.metrics import jaccard_score, f1_score


# Compute mutual information, cross correlation, mse between the fixed regression and moving tbet images


def compute_metrics(
    fixed_image_id, moving_image_id, scale_name, fixed_image, moving_image
):

    # Compute Mutual Information
    mutual_info = ants.image_mutual_information(fixed_image, moving_image)

    # Compute Cross Correlation
    cross_corr = ants.math.image_similarity(
        fixed_image, moving_image, "Correlation"
    )

    # Compute Mean Squared Error
    mse = ants.math.image_similarity(fixed_image, moving_image, "MeanSquares")

    # Binarize the images
    fixed_image_bin = (fixed_image.numpy() > 0.5).astype(int)
    moving_image_bin = (moving_image.numpy() > 0.5).astype(int)
    # Compute Jaccard Index
    jaccard_index = jaccard_score(
        fixed_image_bin.flatten(),
        moving_image_bin.flatten(),
        average="weighted",
    )

    # Compute the Dice coefficient
    f1 = f1_score(
        fixed_image_bin.flatten(),
        moving_image_bin.flatten(),
        average="weighted",
    )

    # Get image from array
    # fixed_image = sitk.GetImageFromArray(fixed_image.numpy())
    # moving_image = sitk.GetImageFromArray(moving_image.numpy())

    # Compute the Hausdorff distance
    # hausdoroff_distance = sitk.HausdorffDistanceImageFilter()
    # hausdoroff_distance.Execute(fixed_image, moving_image)
    # hausdoroff_distance_value = hausdoroff_distance.GetHausdorffDistance()
    #
    return pd.DataFrame.from_dict(
        {
            "fixed_image_id": [fixed_image_id],
            "moving_image_id": [moving_image_id],
            "scale_name": [str(scale_name)],
            "Mutual Information": [mutual_info],
            "Cross Correlation": [cross_corr],
            "Mean Squared Error": [mse],
            "Jaccard Index": [jaccard_index],
            "F1 Score": [f1],
            # "Hausdorff Distance": [hausdoroff_distance_value],
        }
    )
