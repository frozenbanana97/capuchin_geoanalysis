This work has been transfered from my fork of [https://github.com/frozenbanana97/automacao](https://github.com/frozenbanana97/automacao)
<br>
# GPX Parsing, Data Prep, & Analysis
<br>
Optimized for working with scan sampling data specifically for primatological purposes.

### Instructions

* To run the algorithm, you will need both `GPXanalysis.py` and `dataprep.py` downloaded in your working directory.
* The GPX files to be analysed should be copied into this same directory, the scripts will create any additional required directories for data storage.
* You will need a Python environment, whether global (installed on your computer) or a virtual environment (recommended, see instructions in steps below, or see [here](https://github.com/frozenbanana97/documentation) for setting one up and troubleshooting), with the proper requirements from `requirements.txt` installed.
* Once everything is installed correctly, run `GPXanalysis.py` and follow the prompts, the analysed data will be exported to the folder `gpkgData/` ready for use in GIS applications as well as the folder `csvDayFiles/` in .csv format.

### Notes

* The Jupyter Notebook `Automation Notebook.ipynb` is for development purposes and testing as it requires additional setup to run, but feel free to use it for your own purposes. I will keep it and the .py modules up to date with each other.
* `dataprep.py` is a backup of the main chunk of code before I implemented modules and functions. It is also from before the spatial analysis functions were developed and is used solely as a backup in case no spatial properties are wanted for a certain analysis. This will **not** be kept updated.

### Steps

#### Creating a Virtual Environment

This is recommended whenever working on a coding project to ensure that everything installed for the project does not affect the system at large and therefore can be reset with ease if something goes wrong.

<br>
Follow these steps to create and enter a python virtual environment:

* First make sure you have python 3.8.10 or higher installed on your system, follow instructions [here](https://www.python.org/downloads/) to download and install it.
* The `venv` is installed with python on your system, this can be done by running the following code. You can also check the [official python documentation](https://docs.python.org/3/library/venv.html) if there are any problems. Your virtual environment should be created in the working directory for this project.

```
python3 -m venv /path/to/new/virtual/environment
```

* To start the virtual environment, navigate to its folder, locate either `/Scripts/` or `/bin/` depending on your OS and installation method. Within this folder locate the activate script, copy this directory into your python workspace (terminal window, VS Code terminal etc.) and run it as so:

```
#Linux
. venvFolder/bin/activate
```

```
#Windows
\venvFolder\Scripts\Activate.ps1
```

* Now you should see the virtual environements name on the command line of your terminal. This means all commands using that terminal are being executed through the virtual environment. If this does not work you can troubleshoot using eith the [official python documentation](https://docs.python.org/3/library/venv.html) or [my own documentation](https://github.com/frozenbanana97/documentation), admittedly not as thorough but may come in handy.
* Next step is to install the requirements, this can be done (after downloading all the required files) by running:

```
pip install -r requirements.txt
```

The environment should now be ready to run the scripts!