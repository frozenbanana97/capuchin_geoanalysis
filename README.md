This work has been transfered from my fork of [https://github.com/frozenbanana97/automacao](https://github.com/frozenbanana97/automacao)
<br>
# Contents

- [Contents](#contents)
- [GPX Parsing, Data Prep, & Analysis](#gpx-parsing-data-prep--analysis)
    - [Instructions](#instructions)
    - [Notes](#notes)
    - [Steps](#steps)
      - [Creating a Virtual Environment](#creating-a-virtual-environment)
- [Pre-Analysis Data Format](#pre-analysis-data-format)
    - [Issues & Limitations](#issues--limitations)
- [Roadmap](#roadmap)

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

# Pre-Analysis Data Format

Here is a snippet from a `.gpx` made and exported using Locus Map v4, all data will have to match this format to not require tweaking of the code to succesfully parse the information.
<br>
```
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<gpx version="1.1" creator="Locus Map, Android"
xmlns="http://www.topografix.com/GPX/1/1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"
xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"
xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"
xmlns:locus="http://www.locusmap.eu">
    <metadata>
        <desc>File with points/tracks from Locus Map/4.10.0</desc>
        <time>2022-06-21T15:31:54.073Z</time>
    </metadata>
<wpt lat="-7.519585" lon="-34.965436">
    <ele>90.00</ele>
    <time>2022-06-10T12:45:02.777Z</time>
    <name>2022-06-10 09:44:17 ni3 sleeping</name>
</wpt>
```

The initial dataframe after import and conversion is builtas follows, with all observations from the field appended to the name column in Locus Map, whether with or without spaces, see column `name` row `1`, which contains `2022-06-10 09:44:17 ni3 sleeping` where `ni3 sleeping` are the observations made by the field worker. This format is crucial for the script to work at its full extent. The full format is: `'age/sex'+'strata'+'additional observations/notes'`. Note that the `hdop` column may or may not be present and that is okay.
<br>
|  | desc | time | lat | lon | ele | name | hdop |
| --- | ---- | ---- | --- | --- | --- | ---- | ---- |
| 0 | File with points/tracks from Locus Map/4.10.0 | 2022-06-21T15:31:54.073000Z | NaN | NaN | NaN | None | NaN |
| 1 | None | 2022-06-10T12:45:02.777000Z | -7.519585 | -34.965436 | 90.0 | 2022-06-10 09:44:17 ni3 sleeping | NaN |
| 2 | None | 2022-06-10T12:45:57.017000Z | -7.519684 | -34.965638 | 90.0 | 2022-06-10 09:45:46m3 | NaN |
| 3 | None | 2022-06-10T12:46:31.088000Z | -7.519624 | -34.965603 | 90.0 | 2022-06-10 09:46:28 f4 | NaN |
| 4 | None | 2022-06-10T12:46:46.679000Z | -7.519653 | -34.965601 | 90.0 | 2022-06-10 09:46:42j23cane | NaN |

Once your data resembles this, the algorithms will work properly and output the csv's and geopackage files for further study and analysis.

Please see the roadmap for further developmment plans!

### Issues & Limitations

There is a major limitation however. If the age/sex part of the observation (ni, m, j2 etc) is not hard-coded intp the algorith then it will break. This is due to the methd of data collection that had already taken place for a while before this code was written, where a lack of seperator was used for the age/sex, strata, and observations. The nature of having different lengths of age/sex values and no seperator (i.e commas or consistent use of spaces) made it particularly difficult to automate the extraction of this data from the string. If anyone can figure out how to solve this issue please let me know and feel free to contribute!

The scan seperation segment of the code is also hard-coded in and is not fully scalable. I put in code to account for upwards of 10 scans per day, but again if this proves problematic it can be fixed by simply copy-pasting the existing code and changing the identifier values.

# Roadmap

* Create a more clear and complete installation guide at the start of the readme. Python, QGIS, VS Code, and Git (as optinal, ad signing into git here)
* Open links in new tabs.
* Mention adding Python to PATH
* Make tutorial to creating a repo to work in.
* Show how to open the terminal in VS Code.
* Add how to use .gitignore
* Add a location for GPX data to run the code with.
* Distance from each individual to the border.
* Size of the group.
* Home range.
* Centroid to centroid, scan by scan distance in temporal order.
* Area overlap
* Automated map creation by day
    * Tool to view scan by scan
* Aggregate all data and make a webmap tool to view it with a time slider day by day, hour by hour averages of monkey location