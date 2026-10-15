# -----------------------------------------------------------------------------
# classify dams in BC - rank I-II-II
# add SubId and DA_NM to classification file
# JWT October 2026
# -----------------------------------------------------------------------------
import geopandas as gpd
import pandas as pd

# all dam file, filtered to bc, and all that have coordinates
path = "C:/Users/TrubilowiczJ/OneDrive - EC-EC/Hydrotechnical Services/FHIMP/Strategic Projects/Student Projects/Olivia Rose/National Dam Inventory Project/5. Complete Dataset/"
dat = pd.read_excel(path + "final_dataset (1).xlsx")
bc_dat = dat[(dat["pt"] == "BC") & (dat["x"].notna()) & (dat["y"].notna())]

# get unique values for primary description
set(bc_dat["primary_description"])

# initial classification for testing
# note that there are many significant dams on list without coordinates
# Flood control, Water supply, or Hydroelectricity = level 1
# name contains "Dam" = level 2
# everything else = level 3
bc_dat["Level_I"] = 0
bc_dat["Level_II"] = 0
bc_dat["Level_III"] = 0

bc_dat.loc[bc_dat["primary_description"].isin(["Flood control", "Water supply", "Hydroelectricity"]), "Level_I"] = 1
bc_dat.loc[bc_dat["name"].str.contains("Dam", case=False, na=False) & (bc_dat["Level_I"] == 0), "Level_II"] = 1
bc_dat.loc[(bc_dat["Level_I"] == 0) & (bc_dat["Level_II"] == 0),  "Level_III"] = 1

# add the spatial info
#remove all da
# convert to geodataframe
dams_gdf = gpd.GeoDataFrame(bc_dat, geometry=gpd.points_from_xy(bc_dat.x, bc_dat.y), crs = "EPSG:4326").to_crs("ESRI:102001")


# BC could include: 08, 09, Mackenzie
# just do 08 for now
basin_08 = gpd.read_file("data/CLRH/08/finalcat_info_v1-1.gpkg").loc[:,["geometry", "SubId", "DA_NM"]]

# spatial join cols to dams
dams_sub = dams_gdf.sjoin(basin_08, how = "left")

#simplify columns: name, pt, Lat, Lon, Level 1-3, SubId, DA_NM
dams_out = dams_sub.rename(columns = {"x":"Lon", "y":"Lat"})
dams_out = dams_out[["name", "pt", "Lon", "Lat", "Level_I", "Level_II", "Level_III", "SubId", "DA_NM"]].dropna(axis = 0)

#SubID needs to be an integer, DA_NM needs to be a character
dams_out["SubId"] = dams_out["SubId"].astype(int)

# write output
dams_out.to_csv('data/CLRH_bc_alteration_signals.csv', index = False)
