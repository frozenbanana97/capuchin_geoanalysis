from typing import Dict
import gpxpy
import pandas as pd
import geopandas as gpd
import warnings
import os
from os import mkdir
from datetime import datetime, timedelta

import spatialFunctions
from spatialFunctions import *

import tkinter as tk
from tkinter import *
from tkinter import filedialog

# Remove warning message for future warnings / Remover mensagem de aviso para avisos futuros
warnings.filterwarnings(action='ignore',category=FutureWarning)
# Suppress warning for setting with copy, non-issue here / Suprimir aviso para configuração com cópia, não é problema aqui
pd.set_option('mode.chained_assignment',None)

# create root GUI window
root = Tk()

# root window title and dimension
root.title('Scan Sample Geoanalysis Settings')
# Set geometry (widthxheight)
root.geometry('550x350')

# varibales to be used by functions
scansButton = IntVar(value=1)  
obsButton = IntVar(value=1) 
user_button = IntVar()
format_button = IntVar(value=1)
gpxDict = dict()
userIn = ''
observer = ''
group = ''
weather = ''
gpxCSV = 1
dirpath = StringVar()
filepath = StringVar()

# class WrappingLabel(tk.Label):
#     '''a type of Label that automatically adjusts the wrap to the size'''
#     def __init__(self, master=None, **kwargs):
#         tk.Label.__init__(self, master, **kwargs)
#         self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

# Functions to be used by widgets

# Select working directory
def getdirectory():
    # Get a directory path by user / Obter um caminho de diretório por usuário
    dir_select=filedialog.askdirectory()
    dirpath.set(dir_select)
    label_path=Label(root,text=dir_select,font=('italic 8'), anchor=W, justify=LEFT, wraplength=300)
    label_path.grid(row=10,column=2,columnspan=2)
    print(dirpath)
    print(dir_select)
    return(dirpath)

def getEdgeFile():
    # Get a directory path by user / Obter um caminho de diretório por usuário
    file_select=filedialog.askopenfilename()
    filepath.set(file_select)
    label_path=Label(root,text=file_select,font=('italic 8'), anchor=W, justify=LEFT, wraplength=300)
    label_path.grid(row=11,column=2,columnspan=2)
    print(filepath)
    print(file_select)
    return(filepath)

# Have tab move to next widget
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

# function to display text when button is clicked
def run():
    usertoggle()
    toggleScans()
    toggleObservations()
    formatToggle()
    big_loop()

def usertoggle():
    val = user_button.get()
    if val == 1:
        print('user input on')
        userIn = 'yes'
        return(userIn)
    else:
        print('user input off')
        userIn = ''
        return(userIn)

def toggleScans():
    val = scansButton.get()
    if val == 1:
        print('scans on')
        scansToggle = 'yes'
        return(scansToggle)
    else:
        print('scans off')
        scansToggle=''
        return(scansToggle)

def toggleObservations():
    val = obsButton.get()
    if val == 1:
        print('observations on')
        obsToggle='yes'
        return(obsToggle)
    else:
        print('observations off')
        obsToggle=''
        return(obsToggle)

def formatToggle():
    val = format_button.get()
    if val == 1:
        print('Use GPX')
        gpxCSV = 1
        return(gpxCSV)
    if val == 0:
        print('Use CSV')
        gpxCSV = 0
        return(gpxCSV)

# Run for loop to cover every gpx file in directory / Execute o loop para cobrir todos os arquivos gpx no diretório
def big_loop():
    # Import fragment border
    # border = gpd.read_file('/home/kyle/Nextcloud/Monkey_Research/Data_Work/CapuchinExtraGIS/FragmentData.gpkg', layer='EdgeLine')

    dir_sel = dirpath.get()
    border = filepath.get()
    # borderdf = pd.DataFrame(border)
    sep = border.split('.')

    # Check if the kind of file the edge of the fragmet is
    if sep[-1] == 'gpkg':
        gpkglayer = layer_input.get(1.0, 'end-1c')
        print('gpkg', layer_input)
        borderLine = gpd.read_file(border, layer = gpkglayer)
        # Add check to ensure layer exists
    elif sep[-1] == 'shp':
        print('shp')
        borderLine = gpd.read_file(border)
    elif sep[-1] == 'kml':
        print('kml')
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
        borderLine = gpd.read_file(border)
        borderLine = borderLine.set_crs('EPSG:4326')
        borderLine = borderLine.to_crs('EPSG:31985')
    else:
        print('ERROR: unrecognized filetype, please use a GeoPackage, Shapefile, or KML')
        main()
    
    print('dir selected: ', dir_sel)
    print('edge file selected: ', border)

    # Remove old master file if it exists / Remova o arquivo mestre antigo, se existir
    if os.path.isfile('csvDayFiles/scansMaster.csv'):
        os.remove('csvDayFiles/scansMaster.csv')
    if os.path.isfile(dir_sel+'/csvDayFiles/scansMaster.csv'):
        os.remove(dir_sel+'/csvDayFiles/scansMaster.csv')

    # Read GPX files selected / 
    if formatToggle() == 1:
        gpxDict = dict()
        print('big loop GPX')
        
        if dir_sel:
            for file in os.listdir(dir_sel):
                if file.endswith('.gpx'):
                    gpxDict[file] = dir_sel+'_file_'+file
                    print('GPX dict')
                    print(gpxDict)
                    print('dir path')        
        else:
            for file in os.listdir():
                if file.endswith('.gpx'):
                    gpxDict[file] = 'file_'+file
                    print('GPX dict')
                    print(gpxDict)
                    print('not dir path')
    
    # Read CSV files selected
    if formatToggle() == 0:
        gpxDict = dict()
        print('big loop CSV')

        if dir_sel:
            for file in os.listdir(dir_sel):
                if file.endswith('.csv'):
                    gpxDict[file] = dir_sel+'_file_'+file
                    print('CSV dict')
                    print(gpxDict)
                    print('dir path')
        else:
            for file in os.listdir():
                if file.endswith('.csv'):
                    gpxDict[file] = 'file_'+file
                    print('CSV dict')
                    print(gpxDict)
                    print('not dir path')
               
    # Loop thorugh all GPX files and perform analysis / Percorra todos os arquivos GPX e realize análises
    for i in gpxDict:
        print('running')

        # Open and read in the .gpx to a dataframe / Abra e leia no .gpx para um dataframe
        if dir_sel:
            if formatToggle() == 1:
                gpxCurrent = i
                gpxCurrent = open(dir_sel+'/'+gpxCurrent)
                gpxCurrent = gpxpy.parse(gpxCurrent)
                gpxCurrent = gpxCurrent.to_xml()
                df = pd.read_xml(gpxCurrent)
            if formatToggle() == 0:
                gpxCurrent = i
                gpxCurrent = open(dir_sel+'/'+gpxCurrent)
                # gpxCurrent = gpxpy.parse(gpxCurrent)
                # gpxCurrent = gpxCurrent.to_xml()
                df = pd.read_csv(gpxCurrent)
                df.reset_index(inplace=True, drop=True)
        else:
            if formatToggle() == 1:
                gpxCurrent = i
                gpxCurrent = open(gpxCurrent)
                gpxCurrent = gpxpy.parse(gpxCurrent)
                gpxCurrent = gpxCurrent.to_xml()
                df = pd.read_xml(gpxCurrent)            
            if formatToggle() == 0:
                gpxCurrent = i
                gpxCurrent = open(gpxCurrent)
                # gpxCurrent = gpxpy.parse(gpxCurrent)
                # gpxCurrent = gpxCurrent.to_xml()
                df = pd.read_csv(gpxCurrent)
                df.reset_index(inplace=True, drop=True)
                

        if formatToggle() == 1:
            # Remove unecessary columns / Remova colunas desnecessárias
            df.pop('desc')
            df.pop('time')
            if 'hdop' in df.columns:
                df.pop('hdop')
            df = df.drop(index=0) # Locus adds an empty row here, remove this line if not needed
            df.reset_index(inplace=True, drop=True)

            # Reorganize columns / Reorganizar colunas
            shiftPos = df.pop('name')
            df.insert(0, 'name', shiftPos)

            # Split 'name' into date, time, and observations / Dividir 'nome' em data, hora e observações
            date = df['name'].str[:10]
            df.insert(loc=0, column='date', value=date, allow_duplicates=True)

            time = df['name'].str[11:19]
            df.insert(loc=1, column='time', value=time, allow_duplicates=True)

            obs = df['name'].str[19:]
            df.insert(loc=2, column='obs', value=obs, allow_duplicates=True)
            # Remove whitespace from observations column / Remover espaço em branco da coluna de observações
            df['obs'] = df['obs'].str.strip()

            df.pop('name')

        # Ask for observer, group, climate conditions / Pergunte por observador, grupo, condições climáticas
        if usertoggle() == 'yes':
            observer = observer_input.get(1.0, 'end-1c')
            group = group_input.get(1.0, 'end-1c')
            weather = weather_input.get(1.0, 'end-1c')
            # Insert user input columns if they have a value / Insira colunas de entrada do usuário se elas tiverem um valor
            if observer:
                df.insert(loc=3, column='observer', value=observer, allow_duplicates=True)
            if group:
                df.insert(loc=3, column='group', value=group, allow_duplicates=True)
            if weather:
                df.insert(loc=3, column='weather', value=weather, allow_duplicates=True)

        # Run the timeScan method in spatialFunctions to apply each point to its appropriate scan
        # Execute o método timeScan em spatialFunctions para aplicar cada ponto à sua varredura apropriada
        print(i)
        if toggleScans() == 'yes':
            # Get scan duration and convert to int / 
            scanMins = scanMins_input.get(1.0, 'end-1c')
            scanMins = int(scanMins)
            print('Scan mins:',scanMins)
            timeScan(df, scanMins)
            
        # Run the observations method in spatialFunctions / Execute o método de observações em spatialFunctions
        if toggleObservations() == 'yes':
            observations(df)

        # Make geographic and set CRS / Faça geográfica e defina CRS
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat)) 
        gdf = gdf.set_crs('EPSG:4326')
        gdf = gdf.to_crs('EPSG:31985')
            
        if dir_sel:    
            # Check and create save directory for gpkg files / Verifique e crie um diretório de salvamento para arquivos gpkg
            gpkgsavePath = dir_sel+'/gpkgData'
            isDir = os.path.isdir(gpkgsavePath)
            if isDir == False:
                mkdir(dir_sel+'/gpkgData')
            
            # Check and create save directory for csv files / Verifique e crie um diretório de salvamento para arquivos csv
            csvsavePath = dir_sel+'/csvDayFiles'
            isDir = os.path.isdir(csvsavePath)
            if isDir == False:
                mkdir(dir_sel+'/csvDayFiles')

        else:
            gpkgsavePath = './gpkgData'
            isDir = os.path.isdir(gpkgsavePath)
            if isDir == False:
                mkdir('gpkgData')
            
            # Check and create save directory for csv files / Verifique e crie um diretório de salvamento para arquivos csv
            csvsavePath = './csvDayFiles'
            isDir = os.path.isdir(csvsavePath)
            if isDir == False:
                mkdir('csvDayFiles')

        # Export each scan as a separate layer using the scanExport and scanSpatial methods in spatialFunctions
        # Exporte cada varredura como uma camada separada usando os métodos scanExport e scanSpatial em spatialFunctions   
        if toggleScans() == 'yes':
                scanExport(gdf, i, dir_sel, borderLine)
        
        if dir_sel:
            # Save to csv / Salvar em csv
            gdf.to_csv(dir_sel+'/csvDayFiles/'+i[:-4]+'.csv')

            # Export gdf into gpkg / Exportar gdf para gpkg
            gdf.to_file(dir_sel+'/gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_wholeDay')
        
        else:
            # Save to csv / Salvar em csv
            gdf.to_csv('csvDayFiles/'+i[:-4]+'.csv')

            # Export gdf into gpkg / Exportar gdf para gpkg
            gdf.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_wholeDay')

    centroidDist(dir_sel)

    print('done')
    main()

# all widgets will be here
# Labels
lbl = Label(root, text='See LINK for help').grid()
layer_lbl = Label(root, text='GPKG Layer Name')
layer_input = Text(root, height=1,width=20)

# User Input
observer_lbl = Label(root, text='Observer')
group_lbl = Label(root, text='Group')
weather_lbl = Label(root, text='Weather')
scansMins_lbl = Label(root, text='Scans Length (min):')

observer_input = Text(root, height=1,width=20)
observer_input.bind('<Tab>', focus_next_window)
group_input = Text(root, height=1,width=20)
group_input.bind('<Tab>', focus_next_window)
weather_input = Text(root, height=1,width=20)
weather_input.bind('<Tab>', focus_next_window)
scanMins_input = Text(root, height=1, width=5)


# Buttons
dir_btn = Button(root, text='Select Directory', command=getdirectory)

file_btn = Button(root, text='Select Edge File', command=getEdgeFile)

run_btn = Button(root, text = 'Run' ,
             fg = 'black', command=run)

userIn_btn = Checkbutton(root, text='Include user input?',
                      variable = user_button,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 15,
                      command=usertoggle)

scans_btn = Checkbutton(root, text = 'Analyze Scans', 
                      variable = scansButton,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 15,
                      command=toggleScans)

obs_btn = Checkbutton(root, text = 'Parse Observations', 
                      variable = obsButton,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 15,
                      command=toggleObservations)

gpx_btn = Checkbutton(root, text = 'Use GPX', 
                      variable = format_button,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 15,
                      command=formatToggle)

csv_btn = Checkbutton(root, text = 'Use CSV', 
                      variable = format_button,
                      onvalue = 0,
                      offvalue = 1,
                      height = 1,
                      width = 15,
                      command=formatToggle)

def main():
    # Set Grid for GUI. Some widgets may be located elsewhere (dir output)
    userIn_btn.grid(row=1)
    observer_lbl.grid(row=2)
    group_lbl.grid(row=3)
    weather_lbl.grid(row=4)

    observer_input.grid(row=2,column=2)
    group_input.grid(row=3,column=2)
    weather_input.grid(row=4,column=2)

    scans_btn.grid(row=5)
    scansMins_lbl.grid(row=6)
    scanMins_input.grid(row=6, column=2)
    obs_btn.grid(row=7)
    gpx_btn.grid(row=8)
    csv_btn.grid(row=9)

    dir_btn.grid(row=10)
    file_btn.grid(row=11)
    layer_lbl.grid(row=12)
    layer_input.grid(row=12, column=2)

    # Path in the directory choosing function
    run_btn.grid()
    # Execute Tkinter
    root.mainloop()

if __name__ == '__main__':
    main()