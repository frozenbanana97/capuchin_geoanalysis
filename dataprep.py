import gpxpy
import pandas as pd
import geopandas as gpd
import warnings
import os
from os import mkdir
from datetime import datetime, timedelta

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

    # Setup time variables for scan labeling / Variáveis de tempo de configuração para rotulagem de digitalização
    scanStart = df.at[1,'time']
    scanStart = datetime.strptime(scanStart,'%H:%M:%S')
    scanEnd = scanStart + timedelta(minutes=20)
    df.insert(loc=2, column='scan', value=0, allow_duplicates=True)
    scanMins = 20
    bufferMins = 5

    # Create list for temporary storage of scan ID's / Criar lista para armazenamento temporário de IDs de digitalização
    scanNum = []

    # Loop to check each time against the times for each day and assign scan ID
    # Faça um loop para verificar cada vez em relação aos horários de cada dia e atribuir a ID de verificação
    for row in df['time']:
        row = datetime.strptime(row,'%H:%M:%S')
        if scanStart <= row <= scanEnd:
            scanNum.append('1')
        elif (scanStart + timedelta(minutes=scanMins*2-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*2+bufferMins)):
            scanNum.append('2')
        elif (scanStart + timedelta(minutes=scanMins*4-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*4+bufferMins)):
            scanNum.append('3')
        elif (scanStart + timedelta(minutes=scanMins*6-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*6+bufferMins)):
            scanNum.append('4')
        elif (scanStart + timedelta(minutes=scanMins*8-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*8+bufferMins)):
            scanNum.append('5')
        elif (scanStart + timedelta(minutes=scanMins*10-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*10+bufferMins)):
            scanNum.append('6')
        elif (scanStart + timedelta(minutes=scanMins*12-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*12+bufferMins)):
            scanNum.append('7')
        elif (scanStart + timedelta(minutes=scanMins*14-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*14+bufferMins)):
            scanNum.append('8')
        elif (scanStart + timedelta(minutes=scanMins*16-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*16+bufferMins)):
            scanNum.append('9')
        elif (scanStart + timedelta(minutes=scanMins*18-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*18+bufferMins)):
            scanNum.append('10')
        elif (scanStart + timedelta(minutes=scanMins*20-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*20+bufferMins)):
            scanNum.append('11')
        elif (scanStart + timedelta(minutes=scanMins*22-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*22+bufferMins)):
            scanNum.append('12')
        elif (scanStart + timedelta(minutes=scanMins*24-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*24+bufferMins)):
            scanNum.append('13')
        elif (scanStart + timedelta(minutes=scanMins*26-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*26+bufferMins)):
            scanNum.append('14')
        elif (scanStart + timedelta(minutes=scanMins*28-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*28+bufferMins)):
            scanNum.append('15')
        elif (scanStart + timedelta(minutes=scanMins*30-bufferMins)) <= row <= (scanEnd + timedelta(minutes=scanMins*30+bufferMins)):
            scanNum.append('16')

        # If no times fit, apply N/A / Se nenhum tempo se encaixar, aplique N/A
        else:
            scanNum.append('') 

    # Apply scan ID list to the dataframe / Aplicar lista de IDs de varredura ao dataframe
    df['scan'] = scanNum

    # Create lists to store observations / Crie listas para armazenar observações
    scanAgeSex = []
    scanStrata = []
    scanBehaviour = []

    # Run loop to parse observations and store in lists / Executar loop para analisar observações e armazenar em listas
    for row in df['obs']:
            # Check the two character codes first to avoid conflicts and any misidentified lines such as 'mf' and 'ff' going to 'm' and 'f'
            # Verifique os dois códigos de caracteres primeiro para evitar conflitos e quaisquer linhas mal identificadas, como 'mf' e 'ff' indo para 'm' e 'f'
            if row[:2] == 'j1':
                    # Append relevant values to appropriate lists / Anexar valores relevantes a listas apropriadas
                    scanAgeSex.append('j1')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2] == 'j2':
                    scanAgeSex.append('j2')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2] == 'j3':
                    scanAgeSex.append('j3')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2] == 'ff':
                    scanAgeSex.append('ff')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2] == 'mf':
                    scanAgeSex.append('mf')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2] == 'sa':
                    scanAgeSex.append('sa')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2] == 'ni':
                    scanAgeSex.append('ni')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:1] == 'f':
                    scanAgeSex.append('f')
                    scanStrata.append(row[1:2])
                    if row[3:]:
                            scanBehaviour.append(row[2:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:1] == 'm':
                    scanAgeSex.append('m')
                    scanStrata.append(row[1:2])
                    if row[3:]:
                            scanBehaviour.append(row[2:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:3] == 'ago':
                    scanAgeSex.append('ago')
                    scanStrata.append('')
                    scanBehaviour.append('')
            else:
                    scanAgeSex.append('')
                    scanStrata.append('')
                    scanBehaviour.append('')

    # Write lists to columns in the current dataframe / Gravar listas em colunas no dataframe atual
    df.insert(loc=2, column='strata', value=scanStrata, allow_duplicates=True)
    df.insert(loc=2, column='behaviour', value=scanBehaviour, allow_duplicates=True)
    df.insert(loc=2, column='age/sex', value=scanAgeSex, allow_duplicates=True)

    # Remove whitespace from observations column / Remover espaço em branco da coluna de observações
    df['behaviour'] = df['behaviour'].str.strip()

    # Remove scan number from any non-behaviour based observations, such as ago or other misc points
    # Remova o número de varredura de qualquer observação não baseada em comportamento, como atrás ou outros pontos diversos
    df.loc[df['age/sex']=='', 'scan'] = 'other'
    df.loc[df['age/sex']=='ago', 'scan'] = 'ago'

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
    
    # Scan by scan export CURRENTLY MANUAL, want to make auto in loop in future
    # This currently does NOT account for missing scan data i.e. just outside of scan times
    # Scan by scan export ATUALMENTE MANUAL, deseja fazer auto in loop no futuro
    # Atualmente, isso NÃO considera dados de varredura ausentes, ou seja, fora dos horários de varredura
    gdfs1 = gdf[(gdf['scan'].isin(['1']))]
    if not gdfs1.empty:
        gdfs1.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan1')
    gdfs2 = gdf[(gdf['scan'].isin(['2']))]
    if not gdfs2.empty:
        gdfs2.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan2')
    gdfs3 = gdf[(gdf['scan'].isin(['3']))]
    if not gdfs3.empty:
        gdfs3.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan3')
    gdfs4 = gdf[(gdf['scan'].isin(['4']))]
    if not gdfs4.empty:
        gdfs4.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan4')
    gdfs5 = gdf[(gdf['scan'].isin(['5']))]
    if not gdfs5.empty:
        gdfs5.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan5')
    gdfs6 = gdf[(gdf['scan'].isin(['6']))]
    if not gdfs6.empty:
        gdfs6.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan6')
    gdfs7 = gdf[(gdf['scan'].isin(['7']))]
    if not gdfs7.empty:
        gdfs7.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan7')
    gdfs8 = gdf[(gdf['scan'].isin(['8']))]
    if not gdfs8.empty:
        gdfs8.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan8')
    gdfs9 = gdf[(gdf['scan'].isin(['9']))]
    if not gdfs9.empty:
        gdfs9.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan9')
    gdfs10 = gdf[(gdf['scan'].isin(['10']))]
    if not gdfs10.empty:
        gdfs10.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan10')
    gdfago = gdf[(gdf['scan'].isin(['ago']))]
    if not gdfago.empty:
        gdfago.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_ago')
    gdfother = gdf[(gdf['scan'].isin(['other']))]
    if not gdfother.empty:
        gdfother.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_other')

    # Spatial analysis section
    
    # Calculate the centroid of the group
    centroid = gdf.dissolve().centroid
    
    # Calculate distance of each point to the centroid of the group
    for row in gdf['geometry']:
        gdfs1.loc[:,'distCentr'] = gdfs1.distance(centroid[0])

    # Create geodataframe for the area, perimeter, and polygon of each scan
    area = gdfs1.dissolve().convex_hull
    area = gpd.GeoDataFrame(gpd.GeoSeries(area))
    area = area.rename(columns={0:'geometry'}).set_geometry('geometry')
    area.loc[:,'area'] = area.area
    area.loc[:,'perimeter'] = area.length



    # Check and create save directory for csv files / Verifique e crie um diretório de salvamento para arquivos csv
    csvsavePath = './csvDayFiles'
    isDir = os.path.isdir(csvsavePath)
    if isDir == False:
        mkdir('csvDayFiles')
    
    # Save to csv / Salvar em csv
    gdf.to_csv('csvDayFiles/'+i[:-4]+'.csv')