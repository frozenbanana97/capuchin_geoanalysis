from doctest import master
import os
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
from shapely import wkt
from shapely.geometry import LineString

def timeScan(df):
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
    
def observations(df):
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

def scanExport(gdf, i, dir_sel, CenList, BordList):

    gdfs1 = gdf[(gdf['scan'].isin(['1']))]
    if not gdfs1.empty:
        scanSpatial(gdfs1, i, '1', dir_sel, gdf, CenList, BordList)
        # gdfCen1 = CenList
        # print(type(gdfCen1))

    gdfs2 = gdf[(gdf['scan'].isin(['2']))]
    if not gdfs2.empty:
        scanSpatial(gdfs2, i, '2', dir_sel, gdf, CenList, BordList)
        # gdfCen2 = CenList
        # print(type(gdfCen2))

    gdfs3 = gdf[(gdf['scan'].isin(['3']))]
    if not gdfs3.empty:
        scanSpatial(gdfs3, i, '3', dir_sel, gdf, CenList, BordList)

    gdfs4 = gdf[(gdf['scan'].isin(['4']))]
    if not gdfs4.empty:
        scanSpatial(gdfs4, i, '4', dir_sel, gdf, CenList, BordList)

    gdfs5 = gdf[(gdf['scan'].isin(['5']))]
    if not gdfs5.empty:
        scanSpatial(gdfs5, i, '5', dir_sel, gdf, CenList, BordList)

    gdfs6 = gdf[(gdf['scan'].isin(['6']))]
    if not gdfs6.empty:
        scanSpatial(gdfs6, i, '6', dir_sel, gdf, CenList, BordList)

    gdfs7 = gdf[(gdf['scan'].isin(['7']))]
    if not gdfs7.empty:
        scanSpatial(gdfs7, i, '7', dir_sel, gdf, CenList, BordList)

    gdfs8 = gdf[(gdf['scan'].isin(['8']))]
    if not gdfs8.empty:
        scanSpatial(gdfs8, i, '8', dir_sel, gdf, CenList, BordList)

    gdfs9 = gdf[(gdf['scan'].isin(['9']))]
    if not gdfs9.empty:
        scanSpatial(gdfs9, i, '9', dir_sel, gdf, CenList, BordList)

    gdfs10 = gdf[(gdf['scan'].isin(['10']))]
    if not gdfs10.empty:
        scanSpatial(gdfs10, i, '10', dir_sel, gdf, CenList, BordList)

    # Create layers for non-scan data / Crie camadas para dados não digitalizados
    gdfago = gdf[(gdf['scan'].isin(['ago']))]
    if not gdfago.empty:
        scanSpatial(gdfago, i, 'ago', dir_sel, gdf, CenList, BordList)

    gdfother = gdf[(gdf['scan'].isin(['other']))]
    if not gdfother.empty:
        scanSpatial(gdfago, i, 'other', dir_sel, gdf, CenList, BordList)


def scanSpatial(gdfscan, i, spatialCounter, dir_sel, gdfFull, CenList, BordList):
    # Get centroid value of all points in scan / Obtenha o valor do centroide de todos os pontos na varredura
    centroid = gdfscan.dissolve().centroid
    borderLine = gpd.read_file('/home/kyle/Nextcloud/Monkey_Research/Data_Work/CapuchinExtraGIS/FragmentData.gpkg', layer='EdgeLine')
    border = borderLine.unary_union

    CenList = []

    # Calculate distance of each point in the group to the centroid and border
    # Calcular a distância de cada ponto no grupo para o centroide e fronteira
    for row in gdfscan['geometry']:
        # Apply to the scan geodataframe / 
        gdfscan.loc[:,'distCentr'] = gdfscan.distance(centroid[0])
        gdfscan.loc[:,'distBorder'] = gdfscan.distance(border)

    # Create geodataframe for the area incuding perimeter, and polygon of each scan / 
    zone = gdfscan.dissolve().convex_hull
    zone = gpd.GeoDataFrame(gpd.GeoSeries(zone))
    zone = zone.rename(columns={0:'zone'}).set_geometry('zone')
    zone.loc[:,'area(m2)'] = zone.area
    zone.loc[:,'perimeter(m)'] = zone.length
    zone.loc[:,'individuals'] = len(gdfscan)
    zone.loc[:,'ind/m2*100'] = (len(gdfscan)/zone['area(m2)'])*100
    zone.loc[:,'ind/perim(m)*100'] = (len(gdfscan)/zone['perimeter(m)'])*100

    #Append to master CSV with scan by scan data NON-geographic / Anexar ao CSV mestre com varredura por varredura de dados NÃO geográficos
    mastercsv = zone.copy()
    mastercsv.insert(loc=0, column='scan', value = i[:-4]+'scan'+spatialCounter)
    mastercsv.loc[:,'centroid'] = centroid
    mastercsv.loc[:,'centBorder(m)'] = mastercsv['centroid'].distance(border)

    date = mastercsv['scan'].str[:8]
    scan = mastercsv['scan'].str[12:]
    mastercsv.pop('scan')

    mastercsv.insert(loc=0, column='date', value=date, allow_duplicates=True)
    mastercsv.insert(loc=1, column='scan', value=scan, allow_duplicates=True)
    
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

def centroidDist(dir_sel):
    if dir_sel:
        mastercsv = pd.read_csv(dir_sel+'/csvDayFiles/scansMaster.csv',)
    else:
        mastercsv = pd.read_csv('csvDayFiles/scansMaster.csv',)

    mastercsv['centroid'] = mastercsv['centroid'].apply(wkt.loads)
    master = gpd.GeoDataFrame(mastercsv, geometry='centroid', crs='EPSG:31985')

    dfmaster = master[master['scan'].apply(lambda x: str(x).isdigit())]
    dfmaster = dfmaster.sort_values('date').reset_index(drop=True)

    groupmaster = dfmaster.groupby(['date']).agg({'centroid':list})
    groupmaster['centroid'] = groupmaster['centroid'].apply(lambda x: LineString(x))
    groupedmaster = gpd.GeoDataFrame(groupmaster)
    groupedmaster.to_csv('grouped.csv')

    lines = pd.read_csv('grouped.csv',)
    lines.rename(columns={'centroid':'geometry'}, inplace=True)
    lines['geometry'] = lines['geometry'].apply(wkt.loads)
    lines = gpd.GeoDataFrame(lines, geometry='geometry', crs='EPSG:31985')
    lines = lines.reset_index()

    for i, row in lines.iterrows():
        date = str(row['date'])
        dateline = lines.loc[[i]]
        dateline.loc[:,'length'] = dateline.length

        mastercsv.loc[:,'dist(m)'] = dateline['length']
        if dir_sel:
            dateline.to_file(dir_sel+'/gpkgData/'+date+'scans.gpkg', driver="GPKG", layer=date+'_route')
        else:
            dateline.to_file('gpkgData/'+date+'scans.gpkg', driver="GPKG", layer=date+'_route')

    if dir_sel:
        mastercsv.to_csv(dir_sel+'/csvDayFiles/scansMaster.csv')
    else:
        mastercsv.to_csv('csvDayFiles/scansMaster.csv')

        os.remove('grouped.csv')
    
    
    
