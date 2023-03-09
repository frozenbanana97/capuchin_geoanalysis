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

import pandas as pd
import geopandas as gpd
import os
import fiona

dir_gpkg = '/home/kyle/Nextcloud/Monkey_Research/Data_Work/AllData/3-AllParsed/MergedGPKG'


gpkgDict = dict()

for file in os.listdir(dir_gpkg):
	if file.endswith('.gpkg'):
		gpkgDict[file] = dir_gpkg+'_file_'+file
		# print(dir_gpkg + '/' + file)

# print('GPX dict')
# gpkgDict

for i in gpkgDict:
	date = i[:10]
	print('File: ' + i)

	gpkgCurrent = dir_gpkg + '/' + i

	layers = fiona.listlayers(gpkgCurrent)

	# check for layers that are not counted as scans
	scans = 0
	agoScans = 0
	otherScans = 0
	wholeScans = 0
	routeScans = 0

	for x in layers:
		if 'ago' in x:
			agoScans =+ 1
		if 'other' in x:
			otherScans =+ 1
		if 'wholeDay' in x:
			wholeScans =+ 1
		if 'route' in x:
			routeScans =+ 1

	# count layers that are not scans
	notScans = 0
	if agoScans >= 1:
		notScans = notScans + 3*agoScans
	
	if otherScans >= 1:
		notScans = notScans + 3*otherScans
	
	if wholeScans >= 1:
		notScans = notScans + wholeScans
	
	if routeScans >= 1:
		notScans = notScans + routeScans
	
	print('notScans:' + str(notScans))
	# calculate actual number of scans
	scans = (len(layers)-notScans)/3
	print(gpkgCurrent[:-10]+' total scans: '+ str(scans))

	# check if scan exists
	# if scan exists apply var with scan layer
	# needs better automating.... like auto insert layer names with date in loop etc
	y = 1
	if scans >= y:
		print('scan '+ str(y))
		scan1_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan1_centroid')
		scan1 = gpd.read_file(gpkgCurrent, layer = date + '_scan1')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan2_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan2_centroid')
		scan2 = gpd.read_file(gpkgCurrent, layer = date + '_scan2')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan3_centroid = gpd.read_file(gpkgCurrent, layer =  date + '_scan3_centroid')
		scan3 = gpd.read_file(gpkgCurrent, layer = date + '_scan3')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan4_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan4_centroid')
		scan4 = gpd.read_file(gpkgCurrent, layer = date + '_scan4')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan5_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan5_centroid')
		scan5 = gpd.read_file(gpkgCurrent, layer = date + '_scan5')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan6_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan6_centroid')
		scan6 = gpd.read_file(gpkgCurrent, layer = date + '_scan6')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan7_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan7_centroid')
		scan7 = gpd.read_file(gpkgCurrent, layer = date + '_scan7')
		y = y +1

	if scans >= y:
		print('scan '+ str(y))
		scan8_centroid = gpd.read_file(gpkgCurrent, layer = date + '_scan8_centroid')
		scan8 = gpd.read_file(gpkgCurrent, layer = date + '_scan8')
		y = y +1


	# NEEDS TO BE A LOOP TO ITERATE, THIS BRUTE FORCE METHOD IS TEMPORARY
	# parse next centroid
	y = 1
	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan2_centroid.dissolve().centroid
		# insert distances to next centroid
		scan1.insert(loc = 11, column='distNextCen', value = scan1.distance(centroid[0]))
		# scan1.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan1')
		scan1.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False)
		y = y + 1

	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan3_centroid.dissolve().centroid
		# insert distances to next centroid
		scan2.insert(loc = 11, column='distNextCen', value = scan2.distance(centroid[0]))
		# scan2.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan2')
		scan2.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False, mode = 'a', header = False)
		y = y + 1
	
	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan4_centroid.dissolve().centroid
		# insert distances to next centroid
		scan3.insert(loc = 11, column='distNextCen', value = scan3.distance(centroid[0]))
		# scan3.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan3')
		scan3.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False, mode = 'a', header = False)
		y = y + 1

	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan5_centroid.dissolve().centroid
		# insert distances to next centroid
		scan4.insert(loc = 11, column='distNextCen', value = scan4.distance(centroid[0]))
		# scan4.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan4')
		scan4.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False, mode = 'a', header = False)
		y = y + 1

	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan6_centroid.dissolve().centroid
		# insert distances to next centroid
		scan5.insert(loc = 11, column='distNextCen', value = scan5.distance(centroid[0]))
		# scan5.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan5')
		scan5.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False, mode = 'a', header = False)
		y = y + 1

	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan7_centroid.dissolve().centroid
		# insert distances to next centroid
		scan6.insert(loc = 11, column='distNextCen', value = scan6.distance(centroid[0]))
		# scan6.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan6')
		scan6.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False, mode = 'a', header = False)
		y = y + 1

	if scans > y:
		print('scan '+ str(y) + ' to centroid ' + str((y+1)))
		centroid = scan8_centroid.dissolve().centroid
		# insert distances to next centroid
		scan7.insert(loc = 11, column='distNextCen', value = scan7.distance(centroid[0]))
		# scan7.to_file(dir_gpkg + '/NEW' + i, driver='GPKG', layer=i[:-4]+'_scan7')
		scan7.to_csv(dir_gpkg + '/csvs/' + i[:-5] +'.csv', index=False, mode = 'a', header = False)
		y = y + 1