# functions here to perform analysis after data creation, such as distance to next centroid, map creation, etc.
# Things that require the gpkg's to already be created or for the data in a future scan to be created
# 
# Scan Interval Length
# Area overlap between scans
# Day Range (whole day convex hull)
# Month range
# year range
# show 25% of group leading the movememnt incluing age/sex
# Home range
# Automated map creation by day
# Heat map of monkey location density



# DISTANCE TO NEXT CENTROID

# Import gpkg for single day

# assign each layer to a gdf
# need to parse layernames scan1, scan1_centroid etc.
# keep track of how many layers

# calculate monkey (scanX) distance to next centroid (scanX+1_centroid) 
# if scanX+1 dos not exist, day is over