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
root.title('Capuchin Geoanalysis Settings')
# Set geometry (widthxheight)
root.geometry('500x300')

# varibales to be used by functions
scansButton = IntVar(value=1)  
obsButton = IntVar(value=1) 
user_button = IntVar()
gpxDict = dict()
userIn = ''
observer = ''
group = ''
weather = ''
dirpath = StringVar()

class WrappingLabel(tk.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

# Functions to be used by widgets

# Select working directory
def getdirectory():
    # Get a directory path by user / Obter um caminho de diretório por usuário
    dir_select=filedialog.askdirectory()
    dirpath.set(dir_select)
    label_path=WrappingLabel(root,text=dir_select,font=('italic 9'))
    label_path.grid(row=7,column=2)
    print(dirpath)
    print(dir_select)
    return(dirpath)

# Have tab move to next widget
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

# function to display text when button is clicked
def run():
    usertoggle()
    toggleScans()
    toggleObservations()
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

# Run for loop to cover every gpx file in directory / Execute o loop para cobrir todos os arquivos gpx no diretório
def big_loop():   
    gpxDict = dict()
    print('big loop')
    dir_sel = dirpath.get()
    print('dir selected')
    print(dir_sel)

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
    
    # Import fragment border
    # border = gpd.read_file('/home/kyle/Nextcloud/Monkey_Research/Data_Work/CapuchinExtraGIS/FragmentData.gpkg', layer='EdgeLine')

    # Remove old master file if it exists / Remova o arquivo mestre antigo, se existir
    if os.path.isfile('csvDayFiles/scansMaster.csv'):
        os.remove('csvDayFiles/scansMaster.csv')
    if os.path.isfile(dir_sel+'/csvDayFiles/scansMaster.csv'):
        os.remove(dir_sel+'/csvDayFiles/scansMaster.csv')
    
    # Loop thorugh all GPX files and perform analysis / Percorra todos os arquivos GPX e realize análises
    for i in gpxDict:
        print('running')

        # Open and read in the .gpx to a dataframe / Abra e leia no .gpx para um dataframe
        if dir_sel:
            gpxCurrent = i
            gpxCurrent = open(dir_sel+'/'+gpxCurrent)
            gpxCurrent = gpxpy.parse(gpxCurrent)
            gpxCurrent = gpxCurrent.to_xml()
            df = pd.read_xml(gpxCurrent)
        else:
            gpxCurrent = i
            gpxCurrent = open(gpxCurrent)
            gpxCurrent = gpxpy.parse(gpxCurrent)
            gpxCurrent = gpxCurrent.to_xml()
            df = pd.read_xml(gpxCurrent)

              
        # Remove unecessary columns / Remova colunas desnecessárias
        df.pop('desc')
        df.pop('time')
        if 'hdop' in df.columns:
            df.pop('hdop')
        df = df.drop(index=0)

        # Reorganize columns / Reorganizar colunas
        shiftPos = df.pop('name')
        df.insert(0, 'name', shiftPos)

        # Ask for observer, group, climate conditions / Pergunte por observador, grupo, condições climáticas
        if usertoggle() == 'yes':
            observer = observer_input.get(1.0, 'end-1c')
            group = group_input.get(1.0, 'end-1c')
            weather = weather_input.get(1.0, 'end-1c')
            # Insert user input columns if they have a value / Insira colunas de entrada do usuário se elas tiverem um valor
            if observer:
                df.insert(loc=1, column='observer', value=observer, allow_duplicates=True)
            if group:
                df.insert(loc=1, column='group', value=group, allow_duplicates=True)
            if weather:
                df.insert(loc=1, column='weather', value=weather, allow_duplicates=True)

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

        # Run the timeScan method in spatialFunctions to apply each point to its appropriate scan
        # Execute o método timeScan em spatialFunctions para aplicar cada ponto à sua varredura apropriada
        print(i)
        if toggleScans() == 'yes':
            timeScan(df)
        
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
                scanExport(gdf, i, dir_sel)
        
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
    
    print('done')

# all widgets will be here
# Labels
lbl = Label(root, text='Time to parse GPX data').grid()
dir_path=Label(root,text=dirpath,font=('italic 10'))

# User Input
observer_lbl = Label(root, text='Observer')
group_lbl = Label(root, text='Group')
weather_lbl = Label(root, text='Weather')

observer_input = Text(root, height=1,width=20)
observer_input.bind('<Tab>', focus_next_window)
group_input = Text(root, height=1,width=20)
group_input.bind('<Tab>', focus_next_window)
weather_input = Text(root, height=1,width=20)


# Buttons
dir_btn = Button(root, text='Select Directory', command=getdirectory)

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

def main():
    # Set Grid for GUI. Some widgets may be located elsewhere (dir output)
    userIn_btn.grid(row=1)
    observer_lbl.grid(row=2)
    group_lbl.grid(row=3)
    weather_lbl.grid(row=4)

    observer_input.grid(row=2,column=2)
    group_input.grid(row=3,column=2)
    weather_input.grid(row=4,column=2)

    scans_btn.grid()
    obs_btn.grid()

    dir_btn.grid()
    # Path in the directory choosing function
    run_btn.grid()
    # Execute Tkinter
    root.mainloop()

if __name__ == '__main__':
    main()