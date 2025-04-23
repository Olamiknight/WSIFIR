# WSIFIR
Whole Slide Immunofluorescence Image Registration (WSIFIR) of Mono-Modal Histopathological Images located on the AstroPath database using ANTsPy.

# Description

This script reads in histological images located on 3 separate biomarker panels located on the AstroPath SQL database. The first panel is focused on the PD-L1/PD-1 axis (WSI02/Axis), The second is focused on tumour regression (WSI06/Regression), and the third one is focused on T-cell activation (WSI14/Tbet).
![Slide3](https://github.com/user-attachments/assets/a470281c-c6e6-41af-a3d7-d9c0bc2db7a9)

Each panel has a corresponding image slice for the same patient as their tissue blocks were sliced into three slices and stained with fluorescent chemicals for digital visualization. Ideally, these sets of images should be mapped unto the same plane however during the tissue sectioning process tissue deformation can occur causing the images to be unaligned.

So, this code was designed to streamline the registration process of these adjacent sections so that they are mapped unto the same coordinate space. Thus, allowing for simulatenous assessment of various aspects of biological response to immmunotheraepeutic treatment for pathologists. 

For each image, there are a total of 9 resolutions therefore registration will be conducted at each resolution with less complex rigid registrations occuring at lower resolutions, moderately complex affine resolutions happenning at medium resolutions and deformable registrations happening at the higher resolutions. 

To evaluate the degree of registration, this notebook uses metrics such as Mutual Information, Cross Correlation, Mean Squared Error, Jaccard Index, Dice Similarity Score, and Hausdorff Distance. The notebook is designed to evaluate the alignment of WSI images before and after transformations performed at each image resolution.

# User installation
- Python Version:
    - Python 3.10    
- Packages:
  - Using pip install the following packages and save them to a conda environment
    - ants
    - dask
    - numpy
    - matplotlib.pyplot
    - pandas
    - sidus
    - skimage
    - sklearn.metrics
    

# Workflow

- First, load an samples table with the slide and sampleids of the sets (rows) images you want to access
    - Example Table:

      <img width="499" alt="image" src="https://github.com/user-attachments/assets/78ea259d-b0a6-4930-a686-e01f2cef30f1" />

- Using the [Sidus](https://laughing-adventure-mzoz3p7.pages.github.io/index.html](https://redesigned-waddle-y65p2r9.pages.github.io/ ) package load in the images and crop them to low resolution.
- Using [ANTsPy](https://github.com/ANTsX/ANTsPy) package run the Rigid Registration code on the images at a low resolution (7-9) and save the transformation paramaters and metrics as an excel file.
- Repeat the process at a higher resolution using the Affine Registration code on the images at a medium resolution (3-5) and save the transformation paramaters and metrics as an excel file.
- Conduct another registration using the Deformable Registration code on the images at a higher resolution (1-2) and save the transformation parameters and metrics as an excel file.
  
![multi_slide_registration](https://github.com/user-attachments/assets/32f13b0c-e26c-4e87-a71c-b2e2e4ba55f2)



# Examples

[Rigid Registration](https://github.com/Olamiknight/WSIFIR/blob/main/Rigid_Reg.ipynb)

# Useful Resources

[ANTsPy API](https://github.com/ANTsX/ANTsPy) Optimized Medical Imaging Library that is based on Simple ITK. It allows for registration, segementation and statisical learning.

[AstroPathDB API](https://laughing-adventure-mzoz3p7.pages.github.io/) Package that allows for access of multispectral images in Python that are located on Microsoft SQL databases.

[Sidus API](https://github.com/pages/auth?nonce=ca5bb124-9131-4f6f-8803-b19e1385532a&page_id=53985155&path=L3BrZ19leGFtcGxlc190dXRvcmlhbHMvY29yZS9sb2FkaW5nX2RhdGEuaHRtbA) Package that allows for access and of spatial omics data for analysis based on AstroPathDB

[Simple ITK API](https://github.com/SimpleITK/SimpleITKPythonPackage) Multidimensional image analysis sofware that also has several useful similariy metrics. 

# References

Doyle, J., Green, B. F., Eminizer, M., Jimenez-Sanchez, D., Lu, S., Engle, E. L., Xu, H., Ogurtsova, A., Lai, J., Soto-Diaz, S., Roskes, J. S., Deutsch, J. S., Taube, J. M., Sunshine, J. C., & Szalay, A. S. (2023). Whole-Slide Imaging, Mutual Information Registration for Multiplex Immunohistochemistry and Immunofluorescence. Laboratory investigation; a journal of technical methods and pathology, 103(8), 100175. https://doi.org/10.1016/j.labinv.2023.100175

Tustison, N. J., Cook, P. A., Holbrook, A. J., Johnson, H. J., Muschelli, J., Devenyi, G. A., Duda, J. T., Das, S. R., Cullen, N. C., Gillen, D. L., Yassa, M. A., Stone, J. R., Gee, J. C., & Avants, B. B. (2021). The ANTsX ecosystem for quantitative biological and medical imaging. Scientific reports, 11(1), 9068. https://doi.org/10.1038/s41598-021-87564-6

Yaniv, Z., Lowekamp, B. C., Johnson, H. J., & Beare, R. (2018). SimpleITK Image-Analysis Notebooks: a Collaborative Environment for Education and Reproducible Research. Journal of digital imaging, 31(3), 290–303. https://doi.org/10.1007/s10278-017-0037-8


# Contact

Mide Olanrewaju (19oo7@queensu.ca)
 
