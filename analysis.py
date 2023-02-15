# functions here to perform analysis after data creation
# functions such as distance to next centroid, map creation, etc.
# Things that require the gpkg's to already be created or for the data in a future scan to be created
# heat map of monkey location


# DISTANCE TO NEXT CENTROID

# Import gpkg for single day

# assign each layer to a gdf
# need to parse layernames scan1, scan1_centroid etc.
# keep track of how many layers

# calculate monkey (scanX) distance to next centroid (scanX+1_centroid) 
# if scanX+1 dos not exist, day is over