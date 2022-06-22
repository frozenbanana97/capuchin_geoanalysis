import geopandas as gpd

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

    return(df)

def scanSpatial(gdf, i, spatialCounter):
    # spatialCounter = str(spatialCounter)
    # type(spatialCounter)
    centroid = gdf.dissolve().centroid

    # Calculate distance of each point to the centroid of the group
    for row in gdf['geometry']:
        gdf.loc[:,'distCentr'] = gdf.distance(centroid[0])

    # Create geodataframe for the area, perimeter, and polygon of each scan
    area = gdf.dissolve().convex_hull
    area = gpd.GeoDataFrame(gpd.GeoSeries(area))
    area = area.rename(columns={0:'geometry'}).set_geometry('geometry')
    area.loc[:,'area'] = area.area
    area.loc[:,'perimeter'] = area.length
    centroid.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter+'_centroid')
    area.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter+'_zone')
    gdf.to_file('gpkgData/'+i[:-4]+'scans.gpkg', driver="GPKG", layer=i[:-4]+'_scan'+spatialCounter)
    # spatialCounter = int(spatialCounter)
    # spatialCounter = spatialCounter+1