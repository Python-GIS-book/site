# Datasets

## digiroad_helsinki.gpkg

Street network of the Helsinki city centre used in Chapter 8. One `LineString Z` per
street segment (2 050 segments, ~150 km), EPSG:3067 (ETRS-TM35FIN), single layer
`digiroad_helsinki`.

### Source

Digiroad – the national road and street database of Finland, maintained by the
Finnish Transport Infrastructure Agency (Väylävirasto). Downloaded as the Uusimaa
regional extract (`UUSIMAA_2` package), layers:

- `DR_LINKKI_K` – road links (geometry, functional class, permitted driving direction, street names)
- `DR_NOPEUSRAJOITUS_K` – speed limits (linearly referenced onto the links via `LINK_ID`)

Digiroad is open data licensed under Creative Commons Attribution 4.0 (CC BY 4.0).
Attribution: © Finnish Transport Infrastructure Agency, Digiroad.

### Processing

Done in `source/data/prepare_digiroad_network_data.ipynb`:

1. From `DR_LINKKI_K` kept `LINK_ID`, `TOIMINN_LK`, `AJOSUUNTA`, `TIENIMI_SU` and the
   geometry; joined the speed limit value (`ARVO`) from `DR_NOPEUSRAJOITUS_K` on `LINK_ID`.
2. Selected the segments intersecting the bounding box
   lon 24.8964–24.9836, lat 60.1440–60.1796 (WGS84) with a spatial join. Segments
   crossing the box edge are kept whole (not cut).
3. Removed 24 segments by hand that fall outside the area of interest or are not in
   real use (e.g. isolated stubs).
4. Renamed the columns (see below) and reprojected to EPSG:3067.
5. Removed duplicated segments. The speed-limit layer holds several records per link
   (one per driving direction and per stretch where the limit changes), so the join in
   step 1 repeated the link geometry once per record: 512 of the 2 562 rows were exact
   geometric copies of another row, differing at most in `maxspeed`. One row per
   geometry was kept, with the most common speed limit of the copies (the lower value
   on ties); `direction`, `road_class` and `name` were identical within every group of
   copies. `id` was renumbered afterwards. (2 562 → 2 050 segments.)

Because of step 5 each street has a single speed limit for its whole length; limits
that change partway along a link, or differ by driving direction, are simplified.

### Columns

| column | Digiroad field | description |
|---|---|---|
| `id` | – | running number 0…2049 |
| `direction` | `AJOSUUNTA` | permitted driving direction: `2` = both directions, `3` = only against the digitizing direction (last vertex → first vertex), `4` = only along the digitizing direction (first vertex → last vertex) |
| `maxspeed` | `ARVO` | speed limit, km/h |
| `road_class` | `TOIMINN_LK` | Digiroad functional road class (1 = highest-order road … 6 = local access street) |
| `name` | `TIENIMI_SU` | street name in Finnish; empty for 159 unnamed segments |
| `geometry` | – | `LineString Z`, EPSG:3067; the Z coordinate is the elevation and is not used in the book |

### Notes

- The network is not fully connected: besides the main component there are five small
  disconnected pieces (24, 10, 3, 2 and 2 nodes), two of them on an island in the
  south-east corner reachable only by ferry, the rest clipping artefacts at the edge of
  the area.
- Eight pairs of intersections are connected by two different segments (e.g. a direct
  link and a loop around a square, or the two carriageways of a divided street). A
  `networkx.Graph` keeps only one of them; use `MultiGraph`/`MultiDiGraph` to keep both.
