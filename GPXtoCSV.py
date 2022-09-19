import os
import pandas as pd
import gpxpy
from os import mkdir

gpxDict = dict()

# Put directoy with GPX files here
dir_sel = input('Path to GPX files: ')

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
if not gpxDict:
    print('ERROR: no GPX files found in selected directory.')

csvsavePath = dir_sel+'/csvData'
isDir = os.path.isdir(csvsavePath)
if isDir == False:
    mkdir(dir_sel+'/csvData')

for i in gpxDict:
    gpxCurrent = i
    gpxCurrent = open(dir_sel+'/'+gpxCurrent)
    gpxCurrent = gpxpy.parse(gpxCurrent)
    gpxCurrent = gpxCurrent.to_xml()
    df = pd.read_xml(gpxCurrent)

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
    print(i)
    df.to_csv(dir_sel+'/csvData/'+i[:-4]+'.csv', index=False)
