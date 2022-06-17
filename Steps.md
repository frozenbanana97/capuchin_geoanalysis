# Steps

Tue, Jun 7, 2022 12:14 PM
Create and start virtual environment.
python3 -m venv venvScanAutomation
source venvScanAutomation/bin/activate
<br>
# QGIS Analysis (Simone)

Vector - Geometry Tools - Collect Geometries: Merges points
Vector - Geometry Tools - Centroid (on collected): Finds centroid of merged points
Toolbox - Distance to nearest hub (line to point): Finds distance of un-merged points to centroid of group
Toolbox - Convex Hulls (on merged): Creates polygon for finding area of group spread