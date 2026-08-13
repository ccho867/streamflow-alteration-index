# Add subbasin ids and region from CLRH to the ontario dam data
import geopandas as gpd
import pandas as pd

# read in datafile
dams = pd.read_csv("data/ontario_alteration_signals.csv", encoding = "latin-1")

# convert to geodataframe
dams_gdf = gpd.GeoDataFrame(dams, geometry=gpd.points_from_xy(dams.Lon, dams.Lat), crs = "EPSG:4326")

# remove region and SubId for replacement
dams_gdf = dams_gdf.drop(columns = ["Region", "SubId"]).to_crs("ESRI:102001")

# 02O basin file
clrh_02_02 = gpd.read_file("data/CLRH/02O/finalcat_info_v1-1.shp")
clrh_02_02_small = clrh_02_02[["SubId", "SSDA_NM", "SDA_NM", "geometry"]]

## 02h basin file
# clrh_02_01 = gpd.read_file("data/CLRH/02H/finalcat_info_v1-1.shp")
# clrh_02_01_small = clrh_02H[["SubId", "SSDA_NM", "SDA_NM", "geometry"]]

# spatial join cols to dams
dams_sub = dams_gdf.sjoin(clrh_02_02_small, how = "left")

# filter NAs, reorder cols
dams_out = dams_sub.dropna(axis = 0).drop(columns = ["index_right", "geometry"])

# write output
dams_out.to_csv('data/CLRH_ontario_alteration.csv', index = False)
