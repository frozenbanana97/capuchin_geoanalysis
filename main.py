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
Checkbutton1 = IntVar()  
Checkbutton2 = IntVar() 
user_button = IntVar()
gpxDict = dict()
userIn = ''
observer = ''
group = ''
weather = ''

# Functions to be used by widgets

# Select working directory
def directory():
    # get a directory path by user
    filepath=filedialog.askdirectory(initialdir=r"F:\python\pythonProject",
                                    title="Select Directory")
    label_path=Label(root,text=filepath,font=('italic 10'))
    label_path.grid(row=6,column=2)
    dir_path = filepath
    print(dir_path)

# Have tab move to next widget
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

# function to display text when button is clicked
def run():
    # gpx_read()
    usertoggle()
    # userInputVal()
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

def mytoggle1(event=None):
    val = Checkbutton1.get()
    if val == 1:
        print('1 on')
    else:
        print('1 off')

def mytoggle2(event=None):
    val = Checkbutton2.get()
    if val == 1:
        print('2 on')
    else:
        print('2 off')

# Run for loop to cover every gpx file in directory / Execute o loop para cobrir todos os arquivos gpx no diretório
def big_loop():
    print('big loop')
    for file in os.listdir():
        if file.endswith('.gpx'):
            gpxDict[file] = 'file_'+file
        print('GPX dict')
    
    for i in gpxDict:
        print('running')
        
        # Open and read in the .gpx to a dataframe / Abra e leia no .gpx para um dataframe
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
        print('usertoggle')
        print(usertoggle())
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
        timeScan(df)
        
        # Run the observations method in spatialFunctions / Execute o método de observações em spatialFunctions
        observations(df)

        # Make geographic and set CRS / Faça geográfica e defina CRS
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat)) 
        gdf = gdf.set_crs('EPSG:4326')
        gdf = gdf.to_crs('EPSG:31985')

        # Check and create save directory for gpkg files / Verifique e crie um diretório de salvamento para arquivos gpkg
        gpkgsavePath = './gpkgData'
        isDir = os.path.isdir(gpkgsavePath)
        if isDir == False:
            mkdir('gpkgData')
        
        # Export gdf into gpkg / Exportar gdf para gpkg
        gdf.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_wholeDay')
        
        # Export each scan as a separate layer using the scanExport and scanSpatial methods in spatialFunctions
        # Exporte cada varredura como uma camada separada usando os métodos scanExport e scanSpatial em spatialFunctions    
        scanExport(gdf, i)

        # Check and create save directory for csv files / Verifique e crie um diretório de salvamento para arquivos csv
        csvsavePath = './csvDayFiles'
        isDir = os.path.isdir(csvsavePath)
        if isDir == False:
            mkdir('csvDayFiles')
        
        # Save to csv / Salvar em csv
        gdf.to_csv('csvDayFiles/'+i[:-4]+'.csv')

        print('done')

# all widgets will be here
# adding a label to the root window
lbl = Label(root, text='Time to parse GPX data').grid()

# User Input
user_lbl = Label(root, text='Include user input?')
user_check = Checkbutton(root, text = 'Yes/No', 
                      variable = user_button,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 10,
                      command=usertoggle)
observer_lbl = Label(root, text='Observer')
group_lbl = Label(root, text='Group')
weather_lbl = Label(root, text='Weather')

observer = ''
group = ''
weather = ''

observer_input = Text(root, height=1,width=20)
observer_input.bind('<Tab>', focus_next_window)
group_input = Text(root, height=1,width=20)
group_input.bind('<Tab>', focus_next_window)
weather_input = Text(root, height=1,width=20)

# Button
# button widget with red color text inside
dir_btn = Button(root, text='Select Directory', command=directory)

run_btn = Button(root, text = 'Run' ,
             fg = 'black', command=run)

Button1 = Checkbutton(root, text = 'Test 1', 
                      variable = Checkbutton1,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 10,
                      command=mytoggle1)

Button2 = Checkbutton(root, text = 'Test 2', 
                      variable = Checkbutton2,
                      onvalue = 1,
                      offvalue = 0,
                      height = 1,
                      width = 5,
                      command=mytoggle2)

# Set Grid
user_lbl.grid(row=1)
user_check.grid(row=1,column=2)
observer_lbl.grid(row=2)
group_lbl.grid(row=3)
weather_lbl.grid(row=4)

observer_input.grid(row=2,column=2)
group_input.grid(row=3,column=2)
weather_input.grid(row=4,column=2)

Button1.grid()
Button2.grid()

dir_btn.grid()

run_btn.grid()



# Execute Tkinter
root.mainloop()

# Get user decision for input fields and state the variables / Obtenha a decisão do usuário para campos de entrada e indique as variáveis
# userInput = input('To add observer, group, and weather information for each day type \'yes\'. Otherwise leave blank and hit enter')
# observer = ''
# group = ''
# weather = ''

# Declare required vars
# dir_path = ''

# Create a dictionary with all gpx files in dictionary / Crie um dicionário com todos os arquivos gpx no dicionário
def gpx_read():
    for file in os.listdir():
        if file.endswith('.gpx'):
            gpxDict[file] = 'file_'+file

# # Run for loop to cover every gpx file in directory / Execute o loop para cobrir todos os arquivos gpx no diretório
# def big_loop():
#     print('big loop')
#     for file in os.listdir():
#         if file.endswith('.gpx'):
#             gpxDict[file] = 'file_'+file
#         print('GPX dict')
    
#     for i in gpxDict:
#         print('running')
        
#         # Open and read in the .gpx to a dataframe / Abra e leia no .gpx para um dataframe
#         gpxCurrent = i
#         gpxCurrent = open(gpxCurrent)
#         gpxCurrent = gpxpy.parse(gpxCurrent)
#         gpxCurrent = gpxCurrent.to_xml()
#         df = pd.read_xml(gpxCurrent)

#         # Ask for observer, group, climate conditions / Pergunte por observador, grupo, condições climáticas
#         if userInput:
#             observer = input('Input for '+i+': Observer/Observador? ')
#             group = input('Input for '+i+': Group/Grupo? (if both, mark 0) ') # or leave blank?
#             weather = input('Input for '+i+': Weather conditions/Condição do clima? ')
        
#         # Remove unecessary columns / Remova colunas desnecessárias
#         df.pop('desc')
#         df.pop('time')
#         if 'hdop' in df.columns:
#             df.pop('hdop')
#         df = df.drop(index=0)

#         # Reorganize columns / Reorganizar colunas
#         shiftPos = df.pop('name')
#         df.insert(0, 'name', shiftPos)

#         # Insert user input columns if they have a value / Insira colunas de entrada do usuário se elas tiverem um valor
#         if observer:
#             df.insert(loc=1, column='observer', value=observer, allow_duplicates=True)
#         if group:
#             df.insert(loc=1, column='group', value=group, allow_duplicates=True)
#         if weather:
#             df.insert(loc=1, column='weather', value=weather, allow_duplicates=True)

#         # Split 'name' into date, time, and observations / Dividir 'nome' em data, hora e observações
#         date = df['name'].str[:10]
#         df.insert(loc=0, column='date', value=date, allow_duplicates=True)

#         time = df['name'].str[11:19]
#         df.insert(loc=1, column='time', value=time, allow_duplicates=True)

#         obs = df['name'].str[19:]
#         df.insert(loc=2, column='obs', value=obs, allow_duplicates=True)
#         # Remove whitespace from observations column / Remover espaço em branco da coluna de observações
#         df['obs'] = df['obs'].str.strip()

#         df.pop('name')

#         # Run the timeScan method in spatialFunctions to apply each point to its appropriate scan
#         # Execute o método timeScan em spatialFunctions para aplicar cada ponto à sua varredura apropriada
#         timeScan(df)
        
#         # Run the observations method in spatialFunctions / Execute o método de observações em spatialFunctions
#         observations(df)

#         # Make geographic and set CRS / Faça geográfica e defina CRS
#         gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat)) 
#         gdf = gdf.set_crs('EPSG:4326')
#         gdf = gdf.to_crs('EPSG:31985')

#         # Check and create save directory for gpkg files / Verifique e crie um diretório de salvamento para arquivos gpkg
#         gpkgsavePath = './gpkgData'
#         isDir = os.path.isdir(gpkgsavePath)
#         if isDir == False:
#             mkdir('gpkgData')
        
#         # Export gdf into gpkg / Exportar gdf para gpkg
#         gdf.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_wholeDay')
        
#         # Export each scan as a separate layer using the scanExport and scanSpatial methods in spatialFunctions
#         # Exporte cada varredura como uma camada separada usando os métodos scanExport e scanSpatial em spatialFunctions    
#         scanExport(gdf, i)

#         # Check and create save directory for csv files / Verifique e crie um diretório de salvamento para arquivos csv
#         csvsavePath = './csvDayFiles'
#         isDir = os.path.isdir(csvsavePath)
#         if isDir == False:
#             mkdir('csvDayFiles')
        
#         # Save to csv / Salvar em csv
#         gdf.to_csv('csvDayFiles/'+i[:-4]+'.csv')

