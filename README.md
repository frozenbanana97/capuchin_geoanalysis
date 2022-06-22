This work has been transfered from my fork of [https://github.com/frozenbanana97/automacao](https://github.com/frozenbanana97/automacao)
<br>
# GPX Parsing, Data Prep, & Analysis
<br>
Optimized for working with scan sampling data specifically for primatological purposes.

### Instructions

* To run the algorithm, you will need both `GPXanalysis.py` and `dataprep.py` downloaded in your working directory.
* The GPX files to be analysed should be copied into this same directory, the scripts will create any additional required directories for data storage.
* You will need a Python environment, whether global (installed on your computer) or a virtual environment (recommended, see instructions in `Steps.md` or [here](https://github.com/frozenbanana97/documentation) for setting one up and troubleshooting), with the proper requirements from `requirements.txt` installed.
* Once everything is installed correctly, run `GPXanalysis.py` and follow the prompts, the analysed data will be exported to the folder `gpkgData/` ready for use in GIS applications as well as the folder `csvDayFiles/` in .csv format.

### Notes

* The Jupyter Notebook `Automation Notebook.ipynb` is for development purposes and testing as it requires additional setup to run, but feel free to use it for your own purposes. I will keep it and the .py modules up to date with each other.
* `dataprep.py` is a backup of the main chunk of code before I implemented modules and functions. It is also from before the spatial analysis functions were developed and is used solely as a backup in case no spatial properties are wanted for a certain analysis. This will **not** be kept updated.