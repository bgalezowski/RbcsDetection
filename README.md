## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Run](#run)


## General info
Name: rbcs_detection <br /> 
Description: Application for diagnosing of selected disases based on detection erythrocyte deformations <br /> 
Authors: Bartłomiej Gałęzowski <br /> 
License: Unlicensed  <br /> 
	
## Technologies
Project is created with:
* OpenCV
* Matplotlib
* Numpy

## Setup
Clone this repository to directory like ```rbcs_detection``` (root directory)  
First you should be sure that you have installed Python in 3.6 version or greater.
Check, if you have installed Pip to install needef packages.
You need to run setup.py file or install all needed packages provided in setup.py file.
# Run
In project root directory run:
```
python main.py --help
```
or
```
python main.py -path [path to file] --descriptor [unl or log-pol] --comparing_method [mahalanobis, euclidean, correlation or canberra]
```
