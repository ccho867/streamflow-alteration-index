# Add subbasin ids and region from CLRH to the ontario dam data
import geopandas as gpd
import pandas as pd

# read in datafile
dams = pd.read_csv("data/ontario_alteration_signals.csv", encoding = "latin-1")

# convert to geodataframe
dams_gdf = gpd.GeoDataFrame(dams, geometry=gpd.points_from_xy(dams.Lon, dams.Lat), crs = "EPSG:4326")

# remove region and SubId for replacement
dams_gdf = dams_gdf.drop(columns = ["Region", "SubId"]).to_crs("ESRI:102001")

#ontario could include: nelson, 04, 03, 02
#read all basins in and merge
basin_02 = gpd.read_file("data/CLRH/02/finalcat_info_v1-1.gpkg").loc[:,["geometry", "SubId", "DA_NM"]]
basin_04 = gpd.read_file("data/CLRH/04/finalcat_info_v1-1.gpkg").loc[:,["geometry", "SubId", "DA_NM"]]
basin_nelson = gpd.read_file("data/CLRH/nelson/finalcat_info_v1-1.gpkg").loc[:,["geometry", "SubId", "DA_NM"]]

# combine them
merged = pd.concat([basin_02, basin_04, basin_nelson])

# spatial join cols to dams
dams_sub = dams_gdf.sjoin(merged, how = "left")

# filter NAs, reorder cols
# unsure why there would be na's, look into this
dams_out = dams_sub.dropna(axis = 0).drop(columns = ["index_right", "geometry"])

#SubID needs to be an integer
dams_out["SubId"] = dams_out["SubId"].astype(int)

# write output
dams_out.to_csv('data/CLRH_ontario_alteration.csv', index = False)
