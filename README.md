# wsimir
Whole Slide Multi-Scale Image Registration of Biomedical Images using ANTsPy.

# Description

This code was designed to streamline the registration process of these adjacent sections so that they are mapped to the same coordinate space. Thus, it allows pathologists to simultaneously assess various aspects of biological response to immunotherapeutic treatment. 

Less complex rigid registrations occur at lower resolutions, moderately complex affine registrations at medium resolutions, and deformable registrations at higher resolutions. 

This pipeline uses metrics such as mutual information, cross correlation, mean squared error, Jaccard Index, dice similarity score, and Hausdorff distance to evaluate the degree of registration. It is designed to assess the alignment of WSI images before and after transformations performed at each image resolution.

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
    - skimage.exposure
    - ipywidgets
    - pyimagej

# Examples

[Mono-Modal IF Axis to Regression Panel Registration](notebooks/Axis_Reg_Registration.ipynb)

[Mono-Modal IF Regression to Tbet Panel Registration](notebooks/Regression_Tbet_Registration.ipynb) 

[Multi-Modal IF to IHC Image Registration](notebooks/IF_IHC_Registration.ipynb)

# Useful Resources

[ANTsPy API](https://github.com/ANTsX/ANTsPy) Optimized Medical Imaging Library that is based on Simple ITK. It allows for registration, segementation and statisical learning.

[AstroPathDB API](https://laughing-adventure-mzoz3p7.pages.github.io/) Package that allows for access of multispectral images in Python that are located on Microsoft SQL databases.

[PyImageJ API](https://github.com/imagej/pyimagej)
Python wrapper for ImageJ2 used for multidimensional image data.

[Sidus API](https://redesigned-waddle-y65p2r9.pages.github.io/index.html#) Package that allows for access and of spatial omics data for analysis based on AstroPathDB.

[Simple ITK API](https://github.com/SimpleITK/SimpleITKPythonPackage) Multidimensional image analysis sofware that also has several useful similariy metrics. 

# References

Doyle, J., Green, B. F., Eminizer, M., Jimenez-Sanchez, D., Lu, S., Engle, E. L., Xu, H., Ogurtsova, A., Lai, J., Soto-Diaz, S., Roskes, J. S., Deutsch, J. S., Taube, J. M., Sunshine, J. C., & Szalay, A. S. (2023). Whole-Slide Imaging, Mutual Information Registration for Multiplex Immunohistochemistry and Immunofluorescence. Laboratory investigation; a journal of technical methods and pathology, 103(8), 100175. https://doi.org/10.1016/j.labinv.2023.100175

Tustison, N. J., Cook, P. A., Holbrook, A. J., Johnson, H. J., Muschelli, J., Devenyi, G. A., Duda, J. T., Das, S. R., Cullen, N. C., Gillen, D. L., Yassa, M. A., Stone, J. R., Gee, J. C., & Avants, B. B. (2021). The ANTsX ecosystem for quantitative biological and medical imaging. Scientific reports, 11(1), 9068. https://doi.org/10.1038/s41598-021-87564-6

Yaniv, Z., Lowekamp, B. C., Johnson, H. J., & Beare, R. (2018). SimpleITK Image-Analysis Notebooks: a Collaborative Environment for Education and Reproducible Research. Journal of digital imaging, 31(3), 290–303. https://doi.org/10.1007/s10278-017-0037-8


# Contacts
Olamide Olanrewaju (mide.olanrewaju@queensu.ca)
Benjamin Green (bgreen42@jhmi.edu)
 
