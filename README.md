# Picman
Picman is a Python-based tool for rapidly building training and test sets with images 
taken from your camera device.

You have only to capture the images you want by pressing SPACE, and ESC when done.

Behind the scene, Picman creates two folders under the same root, 
one for the training set, and the other for the test set, 
and populates them autonomously when you capture the images.  

![picman_sample](doc/img/sample.png)


# Installing
These instructions will get you a copy of this project up and running on your machine.\
If any problem occurs, please, open an issue or email me.

### Development and test platform
* PyCharm 2021
* macOS 11.4 (Big Sur) on MacBookPro with Intel core
* Python 3.9
 
### Installation steps
1. Clone or download this project.
2. Create and activate a new venv (strongly recommended).
3. Install the project's [requirements](requirements.txt) in the venv. 

That's all!

### Run Picman
You can run Picman from PyCharm, or via Terminal.

In both cases, note that the working directory is `../picman/src` and the script path is `../picman/src/picman.py`. 

###### Run via PyCharm
You have to configure the working directory, the script path, and the parameters, as shown [here](doc/img/pycharm-config.png).\
Then run.

###### Run via Terminal (the hard way)
You have to export the Picman root directory `../picman/` in `PYTHONPATH`.\
Then run.
```shell
(venv)$ export PYTHONPATH=$PYTHONPATH:my_path_to_picman
(venv)$ cd picman/src
(venv)/picman/src$ python -d picman.py
```

Note that the parameter `-d ../dataset` avoids Picman creating the dataset folder inside the `src` folder.
See the customization parameters below.

### Custom parameters 
You can specify several parameters to customize Picman, as described in the following.

| Parameter  | Default              | Description 	|
|----------- |--------------------- |-------------- |
|`-d`        | dataset-current_time | The name of the base folder, then the current date-time will be appended     |
|`-n`        | img      	        | Base name for captured images, then an incremental counter will be appended  |
|`-r`        | 0.9      	        | The size of the training set over the entire dataset, in percentage          |
|`-t`        | train        	    | The name of the folder storing the training set                              |
|`-v`        | test        	        | The name of the folder storing the validation/test set            	               |
|`-i`        | 0       	            | Video device index (0 is the webcam)                                         |


# Contributing
Please read our [contributing instructions](CONTRIBUTING.md) and our [code of conduct](CODE_OF_CONDUCT.md),
for details on the process of submitting requests to us.

# Versioning
We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.

# Author
Francesco Racciatti
