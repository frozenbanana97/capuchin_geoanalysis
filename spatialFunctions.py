from doctest import master
import os
from site import check_enableusersite
import pandas as pd
import geopandas as gpd
import numpy as np
from datetime import datetime, timedelta
from shapely import wkt
from shapely.geometry import LineString

def timeScan(df, scanMins):
    # Setup time variables for scan labeling / Variáveis de tempo de configuração para rotulagem de digitalização
    bufferMins = scanMins/4
    scanStart = df.at[0,'time']
    scanStart = datetime.strptime(scanStart,'%H:%M:%S')
    scanEnd = scanStart + timedelta(minutes = scanMins)
    df.insert(loc=2, column='scan', value=0, allow_duplicates=True)

    # Create list for temporary storage of scan ID's / Criar lista para armazenamento temporário de IDs de digitalização
    scanNum = []

    # Loop to check each time against the times for each day and assign scan ID
    # Faça um loop para verificar cada vez em relação aos horários de cada dia e atribuir a ID de verificação
    for row in df['time']:
        row = datetime.strptime(row,'%H:%M:%S')
        if scanStart <= row <= (scanEnd + timedelta(minutes = bufferMins)):
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

        # If no times fit, apply '' / Se nenhum tempo se encaixar, aplique ''
        else:
            scanNum.append('') 

    # Apply scan ID list to the dataframe / Aplicar lista de IDs de varredura ao dataframe
    df['scan'] = scanNum
    
def observations(df):
    # Create lists to store observations / Crie listas para armazenar observações
    scanAgeSex = []
    scanStrata = []
    scanBehaviour = []

    # Run loop to parse observations and store in lists / Executar loop para analisar observações e armazenar em listas
    for row in df['obs'].astype(str):
            # Check the two character codes first to avoid conflicts and any misidentified lines such as 'mf' and 'ff' going to 'm' and 'f'
            # Verifique os dois códigos de caracteres primeiro para evitar conflitos e quaisquer linhas mal identificadas, como 'mf' e 'ff' indo para 'm' e 'f'
            if row[:2].lower() == 'j1':
                    # Append relevant values to appropriate lists / Anexar valores relevantes a listas apropriadas
                    scanAgeSex.append('j1')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2].lower() == 'j2':
                    scanAgeSex.append('j2')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2].lower() == 'j3':
                    scanAgeSex.append('j3')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2].lower() == 'ff':
                    scanAgeSex.append('ff')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2].lower() == 'mf':
                    scanAgeSex.append('mf')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2].lower() == 'sa':
                    scanAgeSex.append('sa')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:2].lower() == 'ni':
                    scanAgeSex.append('ni')
                    scanStrata.append(row[2:3])
                    if row[3:]:
                            scanBehaviour.append(row[3:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:1].lower() == 'f':
                    scanAgeSex.append('f')
                    scanStrata.append(row[1:2])
                    if row[3:]:
                            scanBehaviour.append(row[2:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:1].lower() == 'm':
                    scanAgeSex.append('m')
                    scanStrata.append(row[1:2])
                    if row[3:]:
                            scanBehaviour.append(row[2:])
                    else:
                            scanBehaviour.append('lof')
            elif row[:3].lower() == 'ago':
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

def scanExport(gdf, i, dir_sel, borderLine):
    cenList = []
    borList = []
    cenAppend = []
    borAppend = []

    gdfs1 = gdf[(gdf['scan'].isin(['1']))]
    if not gdfs1.empty:
        cenList, borList = scanSpatial(gdfs1, i, '1', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs2 = gdf[(gdf['scan'].isin(['2']))]
    if not gdfs2.empty:
        cenList, borList = scanSpatial(gdfs2, i, '2', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs3 = gdf[(gdf['scan'].isin(['3']))]
    if not gdfs3.empty:
        cenList, borList = scanSpatial(gdfs3, i, '3', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs4 = gdf[(gdf['scan'].isin(['4']))]
    if not gdfs4.empty:
        cenList, borList = scanSpatial(gdfs4, i, '4', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs5 = gdf[(gdf['scan'].isin(['5']))]
    if not gdfs5.empty:
        cenList, borList = scanSpatial(gdfs5, i, '5', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs6 = gdf[(gdf['scan'].isin(['6']))]
    if not gdfs6.empty:
        cenList, borList = scanSpatial(gdfs6, i, '6', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs7 = gdf[(gdf['scan'].isin(['7']))]
    if not gdfs7.empty:
        cenList, borList = scanSpatial(gdfs7, i, '7', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs8 = gdf[(gdf['scan'].isin(['8']))]
    if not gdfs8.empty:
        cenList, borList = scanSpatial(gdfs8, i, '8', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs9 = gdf[(gdf['scan'].isin(['9']))]
    if not gdfs9.empty:
        cenList, borList = scanSpatial(gdfs9, i, '9', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfs10 = gdf[(gdf['scan'].isin(['10']))]
    if not gdfs10.empty:
        cenList, borList = scanSpatial(gdfs10, i, '10', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    # Create layers for non-scan data / Crie camadas para dados não digitalizados
    gdfago = gdf[(gdf['scan'].isin(['ago']))]
    if not gdfago.empty:
        cenList, borList = scanSpatial(gdfago, i, 'ago', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    gdfother = gdf[(gdf['scan'].isin(['other','']))]
    if not gdfother.empty:
        cenList, borList = scanSpatial(gdfother, i, 'other', dir_sel, borderLine, cenList, borList)
        cenAppend.extend(cenList)
        borAppend.extend(borList)

    # print('cenAppend Lenght: ',len(cenAppend))
    # print('cenAppend: ',cenAppend)
        
    # Write lists to columns in the current dataframe / Gravar listas em colunas no dataframe atual
    gdf.insert(loc=7, column='distBorder', value=borAppend, allow_duplicates=True)
    gdf.insert(loc=7, column='distCentroid', value=cenAppend, allow_duplicates=True)
    


def scanSpatial(gdfscan, i, spatialCounter, dir_sel, borderLine, cenList, borList):

    # Get number of each age/sex type / 
    m = gdfscan.loc[(gdfscan['age/sex']=='m')].shape[0]
    f = gdfscan.loc[(gdfscan['age/sex']=='f')].shape[0]
    j1 = gdfscan.loc[(gdfscan['age/sex']=='j1')].shape[0]
    j2 = gdfscan.loc[(gdfscan['age/sex']=='j2')].shape[0]
    j3 = gdfscan.loc[(gdfscan['age/sex']=='j3')].shape[0]
    sa = gdfscan.loc[(gdfscan['age/sex']=='sa')].shape[0]
    mf = gdfscan.loc[(gdfscan['age/sex']=='mf')].shape[0]
    ff = gdfscan.loc[(gdfscan['age/sex']=='ff')].shape[0]
    ni = gdfscan.loc[(gdfscan['age/sex']=='ni')].shape[0]
    tot = gdfscan.shape[0]

    # Get centroid value of all points in scan / Obtenha o valor do centroide de todos os pontos na varredura
    centroid = gdfscan.dissolve().centroid
    border = borderLine.unary_union

    # Calculate distance of each point in the group to the centroid and border
    # Calcular a distância de cada ponto no grupo para o centroide e fronteira
    for row in gdfscan['geometry']:
        # Apply to the scan geodataframe / Aplicar ao geodataframe de varredura
        gdfscan.loc[:,'distCentr'] = gdfscan.distance(centroid[0])
        gdfscan.loc[:,'distBorder'] = gdfscan.distance(border)
    
    cenList = gdfscan['distCentr'].tolist()
    borList = gdfscan['distBorder'].tolist()
    
    # Create geodataframe for the area incuding perimeter, and polygon of each scan / Crie geodataframe para a área incluindo o perímetro e o polígono de cada varredura
    zone = gdfscan.dissolve().convex_hull
    zone = gpd.GeoDataFrame(gpd.GeoSeries(zone))
    zone = zone.rename(columns={0:'zone'}).set_geometry('zone')
    zone.loc[:,'area(m2)'] = zone.area
    zone.loc[:,'perimeter(m)'] = zone.length
    zone.loc[:,'individuals'] = len(gdfscan)
    zone.loc[:,'ind/ha'] = (len(gdfscan)/zone['area(m2)'])*1000
    zone.loc[:,'ind/perim(km)'] = (len(gdfscan)/zone['perimeter(m)'])*1000

    # Append to master CSV with scan by scan data NON-geographic / Anexar ao CSV mestre com varredura por varredura de dados NÃO geográficos
    mastercsv = zone.copy()
    mastercsv.insert(loc=0, column='scan', value = i[:-4]+'scan'+spatialCounter)
    mastercsv.loc[:,'centroid'] = centroid
    mastercsv.loc[:,'centBorder(m)'] = mastercsv['centroid'].distance(border)

    date = mastercsv['scan'].str[:10]
    scan = mastercsv['scan'].str[14:]
    time = gdfscan['time'].loc[gdfscan.index[0]]
    mastercsv.pop('scan')

    mastercsv.insert(loc=0, column='date', value=date, allow_duplicates=True)
    mastercsv.insert(loc=1, column='scan', value=scan, allow_duplicates=True)
    mastercsv.insert(loc=2, column='time', value=time, allow_duplicates=True)

    mastercsv['m %'] = m/tot
    mastercsv['f %'] = f/tot
    mastercsv['j1 %'] = j1/tot
    mastercsv['j2 %'] = j2/tot
    mastercsv['j3 %'] = j3/tot
    mastercsv['sa %'] = sa/tot
    mastercsv['mf %'] = mf/tot
    mastercsv['ff %'] = ff/tot
    mastercsv['ni %'] = ni/tot
    
    if dir_sel:
        centroid.to_file(dir_sel+'/gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter+'_centroid')
        zone.to_file(dir_sel+'/gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter+'_zone')
        gdfscan.to_file(dir_sel+'/gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter)
        if os.path.isfile(dir_sel+'/csvDayFiles/scansMaster.csv'):
            mastercsv.to_csv(dir_sel+'/csvDayFiles/scansMaster.csv', index=False, mode='a', header=False)
        else:
            mastercsv.to_csv(dir_sel+'/csvDayFiles/scansMaster.csv', index=False, mode='w', header=True)
    else:
        centroid.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter+'_centroid')
        zone.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter+'_zone')
        gdfscan.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter)
        if os.path.isfile('csvDayFiles/scansMaster.csv'):
            mastercsv.to_csv('csvDayFiles/scansMaster.csv', index=False, mode='a', header=False)
        else:
            mastercsv.to_csv('csvDayFiles/scansMaster.csv', index=False, mode='w', header=True)
    
    print(spatialCounter)

    return cenList, borList


def centroidDist(dir_sel,crs):
    if dir_sel:
        mastercsv = pd.read_csv(dir_sel+'/csvDayFiles/scansMaster.csv')
    else:
        mastercsv = pd.read_csv('csvDayFiles/scansMaster.csv')

    mastercsv['centroid'] = mastercsv['centroid'].apply(wkt.loads)
    master = gpd.GeoDataFrame(mastercsv, geometry='centroid', crs=crs)

    dfmaster = master[master['scan'].apply(lambda x: str(x).isdigit())]
    dfmaster = dfmaster.sort_values(by = ['date', 'scan'], ascending = [True, True]).reset_index(drop=True)

    groupmaster = dfmaster.groupby(['date']).agg({'centroid':list})

    # Check if there are enough centroids to perform line calcs / 
    groupmaster['length'] = groupmaster['centroid'].str.len()
    dropped = groupmaster[groupmaster['length'] == 1]
    groupmaster.drop(groupmaster.index[groupmaster['length'] == 1], inplace=True)

    if not dropped.empty:
        numdrop = dropped.shape[0]
        if dir_sel:
            dropped.to_csv(dir_sel+'/csvDayFiles/dropped.csv')
        else:
            dropped.to_csv('csvDayFiles/dropped.csv')

        print('ATTENTION:',numdrop,'days were not included in centorid distance calculations due to too few centroids. See \'dropped.csv\' and other related files.')

    groupmaster['centroid'] = groupmaster['centroid'].apply(lambda x: LineString(x))
    groupedmaster = gpd.GeoDataFrame(groupmaster)
    groupedmaster.to_csv('temp.csv')

    lines = pd.read_csv('temp.csv',)
    lines.rename(columns={'centroid':'geometry'}, inplace=True)
    lines['geometry'] = lines['geometry'].apply(wkt.loads)
    lines = gpd.GeoDataFrame(lines, geometry='geometry', crs=crs)
    lines = lines.reset_index()

    for i, row in lines.iterrows():
        date = str(row['date'])
        dateline = lines.loc[[i]]
        dateline.loc[:,'length'] = dateline.length

        if dir_sel:
            dateline.to_file(dir_sel+'/gpkgData/'+date+'scans.gpkg', driver="GPKG", layer=date+'_route')
        else:
            dateline.to_file('gpkgData/'+date+'scans.gpkg', driver="GPKG", layer=date+'_route')
    
    point2 = mastercsv['centroid'].shift(-1)
    point2 = gpd.GeoDataFrame(point2, geometry='centroid', crs=crs)
    
    mastercsv = gpd.GeoDataFrame(mastercsv, geometry='centroid', crs=crs)
    mastercsv['distCenCen(m)'] = mastercsv['centroid'].distance(point2)

    mastercsv = mastercsv.sort_values(by = ['date', 'scan'], ascending = [True, True]).reset_index(drop=True)
    shiftPos = mastercsv.pop('zone')
    mastercsv['zone'] = shiftPos
    shiftPos = mastercsv.pop('centroid')
    mastercsv['centroid'] = shiftPos
    shiftPos = mastercsv.pop('distCenCen(m)')
    mastercsv.insert(9, 'distCenCen(m)', shiftPos)
    print('centroidDist end')
    print(mastercsv)


    if dir_sel:
        mastercsv.to_csv(dir_sel+'/csvDayFiles/scansMaster.csv', index=False)
    else:
        mastercsv.to_csv('csvDayFiles/scansMaster.csv', index=False)

    os.remove('temp.csv')
    
def cenCleanup(dir_sel):
    
    if dir_sel:
        mcsv = pd.read_csv(dir_sel+'/csvDayFiles/scansMaster.csv')
    else:
        mcsv = pd.read_csv('/csvDayFiles/scansMaster.csv')

    mcsv['shift'] = mcsv['distCenCen(m)'].shift(1)
    mcsv.loc[mcsv['scan'] == 'ago', 'shift'] = np.nan
    mcsv.loc[mcsv['scan'] == 'other', 'shift'] = np.nan

    mcsv['shift'] = mcsv['shift'].shift(-1)
    mcsv.loc[mcsv['scan'] == 'ago', 'shift'] = np.nan
    mcsv.loc[mcsv['scan'] == 'other', 'shift'] = np.nan
    mcsv['distCenCen(m)']=mcsv['shift']
    mcsv.pop('shift')
    mcsv.loc[mcsv['scan'] == 'ago', 'centBorder(m)'] = np.nan
    mcsv.loc[mcsv['scan'] == 'other', 'centBorder(m)'] = np.nan
    mcsv.loc[mcsv['scan'] == 'ago', 'time'] = np.nan
    mcsv.loc[mcsv['scan'] == 'other', 'time'] = np.nan
    if dir_sel:
        mcsv.to_csv(dir_sel+'/csvDayFiles/scansMaster.csv', index=False)
    else:
        mcsv.to_csv('/csvDayFiles/scansMaster.csv', index=False)
    print('cenCleanup end')
    print(mcsv)
    
