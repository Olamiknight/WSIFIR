# WSIFIR
Whole Slide Immunofluorescence Image Registration of Mono-Modal Histopathological Images located on the AstroPath database using ANTsPy.

# 1. Description

This script reads in histological images located on 3 separate biomarker panels located on the AstroPath SQL database. The first panel is focused on the PD-L1/PD-1 axis (WSI02/Axis), The second is focused on tumour regression (WSI06/Regression), and the third one is focused on T-cell activation (WSI14/Tbet).
![Slide3](https://github.com/user-attachments/assets/a470281c-c6e6-41af-a3d7-d9c0bc2db7a9)

Each panel has a corresponding image slice for the same patient as their tissue blocks were sliced into three slices and stained with fluorescent chemicals for digital visualization. Ideally, these sets of images should be mapped unto the same plane however during the tissue sectioning process tissue deformation can occur causing the images to be unaligned.

So, this code was designed to streamline the registration process of these adjacent sections so that they are mapped unto the same coordinate space. Thus, allowing for simulatenous assessment of various aspects of biological response to immmunotheraepeutic treatment for pathologists. 

For each image, there are a total of 9 resolutions therefore registration will be conducted at each resolution with less complex rigid registrations occuring at lower resolutions, moderately complex affine resolutions happenning at medium resolutions and deformable registrations happening at the higher resolutions. 


To evaluate the degree of registration, this notebook uses metrics such as Mutual Information, Cross Correlation, Mean Squared Error, Jaccard Index, Dice Similarity Score, and Hausdorff Distance. The notebook is designed to evaluate the alignment of WSI images before and after transformations performed at each image resolution.

# 2. Prerequisties 

- ants
- dask
- numpy
- matplotlib.pyplot
- pandas
- itertools
- scipy
- sidus
- sitk
- skimage
- sklearn
- spatialdata
- xarray

# 3. Workflow

- First, load an samples table with the slide and sampleids of the sets (rows) images you want to access
- Using the [Sidus](https://laughing-adventure-mzoz3p7.pages.github.io/index.html](https://redesigned-waddle-y65p2r9.pages.github.io/ ) package load in the images and crop them to low resolution.
- Using [ANTsPy](https://github.com/ANTsX/ANTsPy) package run the Rigid Registration code on the images at a low resolution (7-9) and save the transformation paramaters and metrics as an excel file.
- Repeat the process at a higher resolution using the Affine Registration code on the images at a medium resolution (3-5) and save the transformation paramaters and metrics as an excel file.
- Conduct a final registration using the Deformable Registration code on the images at a higher resolution (1-2) and save the transformation parameters and metrics as an excel file.

  ![Slide5](https://github.com/user-attachments/assets/014bc73a-6f0f-4c65-ba3b-5141b9e85b0f)

 
