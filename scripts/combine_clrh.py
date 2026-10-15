# script combines clrh layers from: https://hydrology.uwaterloo.ca/CLRH/Hydrofabric.html
# creates on layer per wsc DA with one clean output field for use in SAI calculation
# JWT October 2026 from Olivia Rose ipynb
##################################################

import glob
import os
import zipfile

import geopandas as gpd
import pandas as pd

zip_folder = "C:/Users/TrubilowiczJ/OneDrive - EC-EC/Hydrotechnical Services/FHIMP/Strategic Projects/Student Projects/Olivia Rose/Canadian Lake River Hydrofabric/Raw zip files/"

extract_folder = "data/extracted/"
output_folder = "data/CLRH/"

os.makedirs(extract_folder, exist_ok=True)

# folders to merge
# note that Nelson (05) is just called nelson and is only 1 in clrh
# mackenzie is listed on its own as well even though it is technically 07 and part of 10
# das = ["01", "02", "03", "04", "06", "08", "09", "10", "11", "Mackenzie", "Nelson"]
das = ["08"]
shpnames = ["finalcat_info_v1-1.shp", "finalcat_info_riv_v1-1.shp", "poi_v1-1.shp", "CanHydroFabric_SSDA.shp", "CanHydroFabric_SDA.shp"]


for da in das:
    # Lists to hold each layer type
    finalcat_gdfs = []
    riv_gdfs = []
    poi_gdfs = []
    outer_gdfs = []
    
    zip_extract_folder = extract_folder + da
    
    for zip_path in glob.glob(os.path.join(zip_folder + da, "*.zip")):
        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        print(zip_name)
        zip_extract_subfolder = os.path.join(zip_extract_folder, zip_name)
        os.makedirs(zip_extract_subfolder, exist_ok=True)

        # Extract ZIP
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(zip_extract_subfolder)

        # Find shapefiles
        shp_files = glob.glob(os.path.join(zip_extract_subfolder, "**", "*.shp"), recursive=True)

        for shp in shp_files:
            shp_name = os.path.basename(shp)
            
            if shp_name not in shpnames:
                continue

            gdf = gpd.read_file(shp)

            # Optional: track source ZIP
            gdf["source_zip"] = zip_name

            if shp_name == "finalcat_info_v1-1.shp":
                finalcat_gdfs.append(gdf)

            elif shp_name == "finalcat_info_riv_v1-1.shp":
                riv_gdfs.append(gdf)

            elif shp_name == "poi_v1-1.shp":
                poi_gdfs.append(gdf)

            elif (shp_name == "CanHydroFabric_SSDA.shp" or shp_name == "CanHydroFabric_SDA.shp"):
                outer_gdfs.append(gdf)

    # Combine each layer type
    finalcat_combined = gpd.GeoDataFrame(pd.concat(finalcat_gdfs, ignore_index=True), crs=finalcat_gdfs[0].crs)
    riv_combined = gpd.GeoDataFrame(pd.concat(riv_gdfs, ignore_index=True), crs=riv_gdfs[0].crs)
    poi_combined = gpd.GeoDataFrame(pd.concat(poi_gdfs, ignore_index=True), crs=poi_gdfs[0].crs)

    # union the outer_boundary
    outer_combined = gpd.GeoDataFrame(pd.concat(outer_gdfs, ignore_index=True), crs=outer_gdfs[0].crs).union_all()
    bounds = gpd.GeoDataFrame({"DA_NM":[da]}, geometry=[outer_combined], crs=outer_gdfs[0].crs)

    # add a drainage area name field to each file\
    finalcat_combined["DA_NM"] = da
    riv_combined["DA_NM"] = da
    poi_combined["DA_NM"] = da

    # Save.gpkgs
    os.makedirs(output_folder + da, exist_ok=True)
    finalcat_combined.to_file(os.path.join(output_folder + da , "finalcat_info_v1-1.gpkg"), driver = "GPKG")
    riv_combined.to_file(os.path.join(output_folder + da, "finalcat_info_riv_v1-1.gpkg"), driver = "GPKG")
    poi_combined.to_file(os.path.join(output_folder + da, "poi_v1-1.gpkg"), driver = "GPKG")
    bounds.to_file(os.path.join(output_folder + da, "outerbounds.gpkg"), driver = "GPKG")


