This work has been transfered from my fork of [https://github.com/frozenbanana97/automacao](https://github.com/frozenbanana97/automacao)

For instructions scroll down.

# Contents

- [The Program](#the-program)
    - [Basic Quick Setup Step-by-Step](#basic-quick-setupstep-by-step)
- [Data Parsing, Prep, & Analysis](#data-parsing-prep--analysis)
    - [Instructions](#instructions)
    - [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    - [Installing Python Requirements](#installing-python-requirements)
- [Pre-Analysis Data Format](#pre-analysis-data-format)
    - [Issues & Limitations](#issues--limitations)
- [Software Installation Guide](#software-installation-guide)
    - [Python Installation](#python-installation)
    - [QGIS Installation](#qgis-installation)
    - [Visual Studio Code](#visual-studio-code)
      - [Opening the Project Files in VS Code (not using Git)](#opening-the-project-files-in-vs-code-not-using-git)
      - [Opening the Project Files in VS Code (using Git)](#opening-the-project-files-in-vs-code-using-git)
    - [To Git, or not to Git](#to-git-or-not-to-git)
      - [Not to Git](#not-to-git)
      - [To Git](#to-git)
- [Roadmap](#roadmap)

# The Program

This program is made to allow for quick analysis and data preperation in primate observation studies, such as scan sampling. To use this program you must have the minimum of Python and the project requiremtns installed as well as the proper type of data to analyze.

### Basic Quick Setup Step-by-Step

Follow this section alone to be able to use the program to analyze your GPX data, all aditional sections are for a more in-depth/advanced use.
To get started using the bare minimum to get the data analyzed, you will need Python installed and the raw data in the correct format.
<br>
* Collect data in the proper format, if you are using Locus Map the GPX export is already in the correct format. [See here](#pre-analysis-data-format) for more info.

##### Windows

* [Download Python](https://www.python.org/downloads/) and run the installer. **Make sure to add Python to PATH** by checking the box in bottom of the installation window. If your current Python is not in PATH please add it. You can always remove and re-install Python if you are having issues. Please see [here](#python-installation) for additional instruction.
* Download this repository (the files of the project) as a zip by clicking on the green box at the top of this page, see [here](#not-to-git) for additional help.
* Unzip the repository. You can do this by right clicking it and extracting. Open the new folder, in a blank area inside the folder open hold shift and right click. Choose either `Open Command Prompt window here` **OR** `Open PowerShell window here` to open the terminal in the project directory.
* In the terminal and run the following commands in this order:

```
pip install GDAL-3.4.2-cp310-cp310-win_amd64.whl
```

```
pip install Fiona-1.8.21-cp310-cp310-win_amd64.whl
```

```
pip install -r requirements.txt
```

* You can now close PowerShell and run main.py. You may need to right click and run with Python. The program will launch with a command prompt window and the user interface. You have to leave the associated command prompt window open, it will provide any debugging information needed.
* With the program window now open, you can select the directory with the GPX files in it.
* Then click **Run** and wait for it to finish, the command prompt window will say 'Done' and the Run button will go back to normal.
* Now you can open and view the CSV's as well as the GeoPakcage files.
* Everything passed this point is additional information for getting deeper into the project and not nexessary for just running the program.

##### Linux

* Python should already be installed, you can check in terminal with `python3 --version`. If it is not installed run `sudo apt install python3`.
* Download this repository as a zip, see [here](#not-to-git) for additional help.
* Unzip the repository and open terminal in the new directory.
* In terminal (cd'd in the correct directory) run:

```
pip install -r requirements.txt
```

* You can now run main.py by typing `python3 main.py` in the terminal and the program will launch! You have to leave the associated terminal open.

Note: These instructions do not include creating a virtual environment which is fine for using the program. If you wish to further develop, work on the code, modify, or add to the program I would highly recommend following the installation instruction that use a [virtual environment](#setting-up-the-virtual-environment).

# Data Parsing, Prep, & Analysis

This program was made for working with scan sampling data specifically for primatological purposes.

### Instructions

* To run the algorithm, you will need both `main.py` and `spatialFunctions.py` downloaded in your working directory.
* The GPX files to be analysed should all be copied into one directory, the program will create any additional required directories for data storage.
* You will need a Python environment, whether global (installed on your computer) or a virtual environment (recommended, see instructions in steps below, or see [here](https://github.com/frozenbanana97/documentation) for setting one up and troubleshooting), with the proper requirements from `requirements.txt` installed.
* Once everything is installed correctly, run `main.py` either by double clicking (Windows) or with `python3 main.py` (Linux) and choose the desired options, the analysed data will be exported in the selected directory under a sub directory gpkgData/ ready for use in GIS applications as well as the folder csvDayFiles/ in .csv format. See the installation instructions if Python and other programs are not yet installed.

##### Notes

The Jupyter Notebook Automation Notebook.ipynb is currently for development purposes and testing as it requires additional setup to run, but feel free to use it for your own purposes. I will keep it and the .py modules up to date with each other.

### Setting up the Virtual Environment

This is recommended whenever working on a coding project to ensure that everything installed for the project does not affect the system at large and therefore can be reset with ease if something goes wrong. However you can just install it all globally *not* in a virtual environemnt if you would like.

Follow these steps to create and enter a python virtual environment:

* First make sure you have python 3.8.10 or higher installed on your system, follow instructions above to download and install it.
* The `venv` (virtual environment) is installed with python on your system, this can be done by running the following code. You can also check the [official python documentation](https://docs.python.org/3/library/venv.html) if there are any problems. Your virtual environment should be created in the working directory for this project.
* To open the terminal in VS Code use \`Ctrl+\`\` (the same key with the \~ tilda right below escape), now you can create your virtual environment with the code below (make sure you are in the correct directory). In Linux you can simply open the terminal while in Windows you'll need to open command prompt

```
python3 -m venv ./venvName
```

* To start the virtual environment, navigate to its folder, locate either `/Scripts/` or `/bin/` depending on your OS and installation method. Within this folder locate the activate script, copy this directory into your python workspace (terminal window, VS Code terminal etc.) and run it as so:

##### Linux

Run in the terminal to activate the virtual environment:

```
. /venvName/bin/activate
```

##### Windows

Change permissions in the command line/terminal to allow the terminal to execte commands:

```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

Activate the virtual environment:

```
\venvName\Scripts\Activate.ps1
```
<br>
* Now you should see the virtual environements name on the command line of your terminal. This means all commands using that terminal are being executed through the virtual environment. If this does not work you can troubleshoot using with the [official python documentation](https://docs.python.org/3/library/venv.html) or [my own documentation](https://github.com/frozenbanana97/documentation), admittedly not as thorough but may come in handy.

### Installing Python Requirements

Next step is to install the requirements, this can be done by running:

##### Linux

```
pip install -r requirements.txt
```

The environment should now be ready to run the scripts!

##### Windows

Windows lacks some of the packages required so you'll have to download them manually, go to the `Windows Dependencies` folder at the top of this page and downlaod both the Fiona and GDAL files into the project directory. NOTE - these files are for a 64 bit version of Windows running Pyhon 3.10, if your system does not match this you should download the files yourself using instructions provided in [my documentation](https://github.com/frozenbanana97/documentation).

Now install them using the Python terminal running out of the directory the filesa re downloaded:

<br>
(if you downloaded different versions make sure to use those file names)
<br>
```
pip install Fiona-1.8.21-cp310-cp310-win_amd64.whl
pip install GDAL-3.4.2-cp310-cp310-win_amd64.whl
```

Next you can install the rest of the requirements using:
<br>
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

There is a major limitation however. If the age/sex part of the observation (ni, m, j2 etc) is not hard-coded into the algorith then it will break. This is due to the method of data collection that had already taken place for a while before this code was written, where a lack of seperator was used for the age/sex, strata, and observations. The nature of having different lengths of age/sex values and no seperator (i.e commas or consistent use of spaces) made it particularly difficult to automate the extraction of this data from the string. If anyone can figure out how to solve this issue please let me know and feel free to contribute!

The scan seperation segment of the code is also hard-coded in and is not fully scalable. I put in code to account for upwards of 10 scans per day, but again if this proves problematic it can be fixed by simply copy-pasting the existing code and changing the identifier values.
<br>
# Software Installation Guide

**Required Software**

* Python 3

**Optional Software**

* QGIS
* Visual Studio Code (or another IDE, my instructions will be for VS Code)
* Git

If you already have a version of the above installed then you can skip that section!

### Python Installation

##### Windows

First make sure you have python 3.8.10 or higher installed on your system, you can download Python [here](https://www.python.org/downloads/). Once the installer is downloaded run it and you will be greeted with a window similar to the image below. Ensure to click Add Python to PATH, and then click install now.
![Python Installation](https://github.com/frozenbanana97/documentation/blob/master/imgs/Py1_PATH.png)
Continue with the installation until it is complete.

##### Linux

Python should already be installed by default, you can check by running the following in your terminal.
<br>
```
python3 --version
```

If Python is *not* installed then you can install it by running (Ubuntu/Debian):
<br>
```
sudo apt install python3
```

Now python is installed!

### QGIS Installation

##### Windows

Go to the [QGIS download page](https://www.qgis.org/en/site/forusers/download.html) and download the Long term release standalone installer. Simply run the installer and thats it!

##### Linux

The instructions on the QGIS download page for Linux are very thorough, jsut make surenif using a distro spin of Debian/Ubuntu to use the corresponding distro name from either Ubuntu or Debian. For example I am running Linux Mint 20.3 Una, which corresponds to the Ubuntu Focal release so I would use Focal where it asks for your distro name.

### Visual Studio Code

VS Code is my preferred code editor, it has built in git intergration which is very handy as well as an extensive list of extensions. While not required to use this project it can make it more easily viewable and editable.
Simply download VS Code [from their website](https://code.visualstudio.com/Download) and run the installer. Once VS Code is installed some extensions will need to be added. Launch the program and navigate to the extensions tab on the left side. You will need both the Python and Jupyter extensions, optional is the Excel Viewer to make viewing csv files way easier.
![VS Code Extensions](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS2_Extensions.png)![Add Extensions](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS3_Py_Jup.png)![Excel Viewer](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS4_Excel.png)
(note: to set as the default viewer, right click a csv file and set default viewer as Excel Viewer)

#### Opening the Project Files in VS Code (not using Git)

In the explorer you will have the option to open a folder, click this and navigate to the extraced folder of the project files. When opening the folder you will be propmted to trust the authors of the folder, click yes.
![VS Code open folder](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS5_OpenFolder.png)![VS folder open](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS6.1.3_Open.png)![VS trust](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS6.1.4_Trust.png)
Now you are ready to continue using your local files!

#### Opening the Project Files in VS Code (using Git)

In the bottom left of VS Code above the gear you can login using your GitHub account. Once logged in, in the open folder section `Clone Repository` should now be clickable (restarting VS Code may be required).
Click on `Clone Repository` and past the link of the repo to clone (same areas as downlaoding the zip but copy the link), in this case [https://github.com/frozenbanana97/capuchin\_geoanalysis.git](https://github.com/frozenbanana97/capuchin_geoanalysis.git) and then choose the directory to clone it do. Now it should open up in VS Code and you're ready to get going!

### To Git, or not to Git

Using Git is completely optional, if you are going to be developing code further and wish to store it on GitHub and use the versioning systems built into Git then you can install it, otherwise you can just manually download the project files and run them. Most people will be fine not using Git.

#### Not to Git

First the project files will need to be downloaded from this webpage, you can download them as seen below. Save the zip file to the directory where you will be working out of and unzip it, the project files will now be accesible to run.
![Downlaod as zip](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS6.1_ZIP.png)![Extract here](https://github.com/frozenbanana97/documentation/blob/master/imgs/VS6.1.2.png)
From this point you can either skip ahead to [Data Parsing, Data Prep, & Analysis](#data-parsing-prep--analysis) and just run the Python (.py) files as instructed. If you want to install and use VS Code to be able to see the code, read comments to understand how it works etc then continue to [Visual Studio Code](#visual-studio-code) to install VS Code.

#### To Git

I will be using Git solely within VS Code so be sure to install it as well. You can use Git through the command line but this is beyond the scope of this tutorial.
First make yourself an account on GitHub (you're already here!!!), this is needed to use Git's functionality.

##### Windows

Next download Git from [their website](https://git-scm.com/downloads) and run the installer. After installation you need to set your username and email for Git on your computer. To do so open up Windows search and type `Git Bash` and open it.
![Run Git Bash](https://github.com/frozenbanana97/documentation/blob/master/imgs/GIT2.png)
Next to set your username run:
<br>
```
git config --global user.name "UserName"
```

Confirm that your username is correct:
<br>
```
git config --global user.name
```

Next set you email:
<br>
```
git config --global user.email youremail@mail.com
```

And conform that it is correct:
<br>
```
git config --global user.email
```

Now Git is set up! You can close the Git Bash window.

##### Linux

Open terminal and instll Git using your package manager i.e
<br>
```
sudo apt install git
```

Next you need to setup your username and email with Git to be able to use it, run:

```
git config --global user.name "UserName"
```

Confirm that your username is correct:
<br>
```
git config --global user.name
```

Next set you email:
<br>
```
git config --global user.email youremail@mail.com
```

And conform that it is correct:
<br>
```
git config --global user.email
```

Now Git is set up! You can close the terminal.

# Roadmap

* Area overlap between scans
* show 25% of group leading the movememnt
* Home range
* Automated map creation by day
* Create working .exe
