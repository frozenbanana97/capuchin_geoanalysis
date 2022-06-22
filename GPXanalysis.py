import gpxpy
import pandas as pd
import geopandas as gpd
import warnings
import os
from os import mkdir
from datetime import datetime, timedelta

import spatialFunctions
from spatialFunctions import *

# Remove warning message for future warnings / Remover mensagem de aviso para avisos futuros
warnings.filterwarnings(action='ignore',category=FutureWarning)
# Suppress warning for setting with copy, non-issue here / Suprimir aviso para configuração com cópia, não é problema aqui
pd.set_option('mode.chained_assignment',None)

# Get user decision for input fields and state the variables / Obtenha a decisão do usuário para campos de entrada e indique as variáveis
userInput = input('To add observer, group, and weather information for each day type \'yes\'. Otherwise hit escape')
observer = ''
group = ''
weather = ''

# Create a dictionary with all gpx files in dictionary / Crie um dicionário com todos os arquivos gpx no dicionário

gpxDict = dict()

for file in os.listdir():
    if file.endswith('.gpx'):
       gpxDict[file] = 'file_'+file

# Run for loop to cover every gpx file in directory / Execute o loop para cobrir todos os arquivos gpx no diretório

for i in gpxDict:
    
    # Open and read in the .gpx to a dataframe / Abra e leia no .gpx para um dataframe
    gpxCurrent = i
    gpxCurrent = open(gpxCurrent)
    gpxCurrent = gpxpy.parse(gpxCurrent)
    gpxCurrent = gpxCurrent.to_xml()
    df = pd.read_xml(gpxCurrent)

    # Ask for observer, group, climate conditions / Pergunte por observador, grupo, condições climáticas
    if userInput:
        observer = input('Input for '+i+': Observer/Observador? ')
        group = input('Input for '+i+': Group/Grupo? (if both, mark 0) ') # or leave blank?
        weather = input('Input for '+i+': Weather conditions/Condição do clima? ')
    
    # Remove unecessary columns / Remova colunas desnecessárias
    df.pop('desc')
    df.pop('time')
    if 'hdop' in df.columns:
        df.pop('hdop')
    df = df.drop(index=0)

    # Reorganize columns / Reorganizar colunas
    shiftPos = df.pop('name')
    df.insert(0, 'name', shiftPos)

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