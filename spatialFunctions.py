import geopandas as gpd

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