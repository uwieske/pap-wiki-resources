# Getting started

## Start using conversion program...
After having cloned this repo, you can run script `run_convert_to_pandas.sh` in order to convert a dump file into a Pandas DataFrame.
The converted file is stored on your local filesystem in the same directory where your dump file is located.
This directory should be passed as the first argument of the `run_convert_to_pandas.sh` script in order to tell the script running in a Docker container where to find the dump file.

````
sh run_convert_to_pandas.sh <local director path containing dump file> <the file path of dump file>
````

Example:

````
sh run_convert_to_pandas ~/docker_data_volumes/papwikires papwiki-20230501-pages-meta-history.xml.bz2
````

## Start developing...
After having cloned this repository from GitHub, it is recommended to create an environment.
We use conda as package manager and will use conda to create a conda environment.
If you have not conda installed on your local machine, you can find instructions on the website of conda how to install and setup conda on your specific machine.
First, make sure you have already updated your local conda program.

At this point you have conda installed locally.
Create the environment named `papenv` by entering the command below in a console window.

Make sure you are in the project's root directoy.

````
conda env create -f environment-dev.yml
````

Activate the environment:

````
conda activate papenv
````

Follow the instructions how to start or automatically switch to `papenv` when working in this project.


Checkout DEVELOPMENT.md how to start developing.