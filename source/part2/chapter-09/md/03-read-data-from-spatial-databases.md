---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Reading data from spatial databases

## Databases

Example syntax for reading and writing data from/to databases. 


### Read PostGIS database using psycopg2

```python
import geopandas as gpd
import psycopg2

# Create connection to database with psycopg2 module (update params according your db)
conn, cursor = psycopg2.connect(
    dbname="my_postgis_database",
    user="my_usrname",
    password="my_pwd",
    host="123.22.432.16",
    port=5432,
)

# Specify sql query
sql = "SELECT * FROM MY_TABLE;"

# Read data from PostGIS
data = gpd.read_postgis(sql=sql, con=conn)
```

### Read / write PostGIS database using SqlAlchemy + GeoAlchemy

```python
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import WKTElement, Geometry

# Update with your db parameters
HOST = "123.234.345.16"
DB = "my_database"
USER = "my_user"
PORT = 5432
PWD = "my_password"

# Database info
db_url = URL(
    drivername="postgresql+psycopg2",
    host=HOST,
    database=DB,
    username=USER,
    port=PORT,
    password=PWD,
)

# Create engine
engine = create_engine(db_url)

# Init Metadata
meta = MetaData()

# Load table definitions from db
meta.reflect(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# ========================
# Read data from PostGIS
# ========================

# Specify sql query
sql = "SELECT * FROM finland;"

# Pull the data
data = gpd.read_postgis(sql=sql, con=engine)

# Close session
session.close()

# =========================================
# Write data to PostGIS (make a copy table)
# =========================================

# Coordinate Reference System (srid)
crs = 4326

# Target table
target_table = "finland_copy"

# Convert Shapely geometries to WKTElements into column 'geom' (default in PostGIS)
data["geom"] = data["geometry"].apply(lambda row: WKTElement(row.wkt, srid=crs))

# Drop Shapely geometries
data = data.drop("geometry", axis=1)

# Write to PostGIS (overwrite if table exists, be careful with this! )
# Possible behavior: 'replace', 'append', 'fail'

data.to_sql(target_table, engine, if_exists="replace", index=False)
```

### Read / write Spatialite database 

```python
import geopandas as gpd
import sqlite3
import shapely.wkb as swkb
from sqlalchemy import create_engine, event

# DB path
dbfp = "L2_data/Finland.sqlite"

# Name for the table
tbl_name = "finland"

# SRID (crs of your data)
srid = 4326

# Parse Geometry type of the input Data
gtype = data.geom_type.unique()
assert len(gtype) == 1, "Mixed Geometries! Cannot insert into SQLite table."
geom_type = gtype[0].upper()

# Initialize database engine
engine = create_engine("sqlite:///{db}".format(db=dbfp), module=sqlite)

# Initialize table without geometries
geo = data.drop(["geometry"], axis=1)

with sqlite3.connect(dbfp) as conn:
    geo.to_sql(tbl_name, conn, if_exists="replace", index=False)

# Enable spatialite extension
with sqlite3.connect(dbfp) as conn:
    conn.enable_load_extension(True)
    conn.load_extension("mod_spatialite")
    conn.execute("SELECT InitSpatialMetaData(1);")
    # Add geometry column with specified CRS with defined geometry typehaving two dimensions
    conn.execute(
        "SELECT AddGeometryColumn({table}, 'wkb_geometry',\
        {srid}, {geom_type}, 2);".format(
            table=tbl_name, srid=srid, geom_type=geom_type
        )
    )

# Convert Shapely geometries into well-known-binary format
data["geometry"] = data["geometry"].apply(lambda geom: swkb.dumps(geom))

# Push to database (overwrite if table exists)
data.to_sql(tbl_name, engine, if_exists="replace", index=False)
```
