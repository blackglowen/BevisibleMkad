# A dummy MKAD distance calculator

MKAD distance calculator is a simple Flask application using a Blueprint to find the distance from the Moscow Ring Road to the specified address. The address is passed to the application in an HTTP request, then via the Yandex Geocoder HTTP API the distance from the MKAD to the specified address is calculated and returned to the user. Addresses inside the MKAD perimeter are their distances set zero.

## How to install and run the app?

We assume that your current working directory is the project root dir.

### Method 1: Installing the wheel distribution in a virtual environment

1- Create a python virtual environment with the following command:

    python -m venv ./venv

2- Activate the virtual envronment:

    source ./venv/bin/activate

3- Build and install the wheel distrubtion located in the dist directory inside the project root dir.
    
    pip install wheel setuptools
    python setup.py bdist_wheel sdist
    pip install ./dist/mkaddis-1.0.0-py3-none-any.whl

4- Finally run the application by simply typing the following command:

    mkaddis

### Method 2: Creating and running directly a docker image of the app

We assume that you have the docker engine and client installed and set up on your local machine. 
From the root directory of the project create a docker image called mkad-dist-calc, then run 
the app. To do so just run the following commads: 
 
    pip install wheel setuptools
    python setup.py bdist_wheel sdist
    docker build -t mkad-dist-calc .
    docker run -p 5000:5000  mkad-dist-calc mkaddis

 
## How to use the app?

Once the app is app and running, you will see a simple button that triggers a prompt asking the input address to which should calculate the distance from MKAD.

Gennerally the app follows a route pattern like this http://127.0.0.1:5000/mkad/api/<address> for searching matches to the specified address. Here you should replace <address> by any string with no special characters representing the input address.

### Examples

 http://127.0.0.1:5000/mkad/api/Istanbul

 http://127.0.0.1:5000/mkad/api/Reutov,Ivanovskoe

 http://127.0.0.1:5000/mkad/api/Novokosino


## Running the tests

To be able to run the tests you should make sure pytest is installed in your virtual environment. After that from the root directory just type:
    
    pytest 
    
If after installation the above command didn't work, try this one from the root directory:
    
    ./venv/bin/pytest

The above command should execute all the tests in tests directory and ouput the result.
 
## License

This project is under the MIT license. 
