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

Done in `source/online-extras/data/prepare_digiroad_network_data.ipynb`:

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
- Sinebrychoffinkatu (`id` 1187) crosses Mallaskatu (`id` 1915) without a node and ends
  about 4 m past it (an overshoot), so its end is a dead end. Chapter 8.3 uses this as an
  example of an error that the automatic fixes do not remove.

## digiroad_topology_errors.gpkg

Street data with added topology errors, used in Chapter 8.3 to demonstrate how to check
and fix the topology of a network. A part of `digiroad_helsinki.gpkg` covering Kamppi,
Punavuori, Ruoholahti and Jätkäsaari: 733 `LineString` segments (2D), EPSG:3067, single
layer `digiroad_topology_errors`.

### Processing

Done in `source/online-extras/data/prepare_topology_errors_data.ipynb`:

1. Selected the segments of `digiroad_helsinki.gpkg` that intersect the bounding box
   lon 24.905–24.945, lat 60.157–60.170 (WGS84); segments crossing the box edge are kept
   whole (736 segments). Kept the columns `id` and `name` and dropped the Z coordinate.
2. Missing nodes: at three T-junctions, joined the two segments of the through street
   into one line, so that the side street ends on the middle of the line without a node:
   Messitytönkuja / Laivapojankuja (`id` 625 + 1813, side street 1075), Kellosaarenkatu /
   Loistokuja (1821 + 104, 1248) and Saukonlaituri / Saukonkatu (2043 + 1173, 1481).
3. Gaps: at three other T-junctions, joined the through street in the same way and cut
   3 m off the end of the side street at the junction: Lastenkodinkatu / Lastenkodin kuja
   (1869 + 2041, 254), Laivurinkatu / Sepänkatu (1870 + 1079, 1346) and Selkämerenkatu /
   Messitytönkatu (670 + 1342, 829). The joined line keeps the `id` of the first segment.
4. Duplicates: appended copies of the segments 1733 (Annankatu), 1317 (Laivurinkatu) and
   1687 (Salmisaarenkatu), which keep their `id`.

The data keep the errors that were already in `digiroad_helsinki.gpkg` within this area,
such as the overshoot of Sinebrychoffinkatu (see above).

### Checks

Built as an undirected graph from the line end points, the data have 588 nodes,
8 connected components (6 before the errors were added), 103 dead ends (97 before) and
3 duplicate segments. After `neatnet.extend_lines(tolerance=5)` and
`neatnet.fix_topology()` (neatnet 0.1.6), the result is the same as `fix_topology()` of the
original 736 segments: 516 segments, 368 nodes, 6 components, 97 dead ends, no
duplicates, and the same 12 pairs of lines crossing without a node.

### Columns

| column | description |
|---|---|
| `id` | `id` of the segment in `digiroad_helsinki.gpkg` (repeated for the three duplicates) |
| `name` | street name in Finnish; empty for unnamed segments |
| `geometry` | `LineString`, EPSG:3067 |

Derived from Digiroad (© Finnish Transport Infrastructure Agency, CC BY 4.0).

## Population_grid_2021_HSY.gpkg

Population grid of the Helsinki metropolitan area (Helsinki, Espoo, Vantaa and
Kauniainen) for 2021, used in Chapter 8.3. 5 853 cells of 250 m × 250 m, EPSG:3879
(ETRS-GK25), single layer. The file is identical to
`part2/chapter-06/nb/data/Helsinki/Population_grid_2021_HSY.gpkg`.

### Source

Helsinki Region Environmental Services Authority HSY, population grid
(`Vaestotietoruudukko_2021`):
<https://www.hsy.fi/en/environmental-information/open-data/avoin-data---sivut/population-grid-of-helsinki-metropolitan-area/>.
Licensed under Creative Commons Attribution 4.0 (CC BY 4.0).

### Notes

- Only cells with at least five inhabitants are included (HSY's privacy rule).
- The last cell (`id` `Vaestotietoruudukko_2021.5853`, 30 427 inhabitants) lies in the
  Gulf of Finland. HSY places there the institutional population and the residents who
  cannot be linked to any building. Chapter 8.3 removes it.
- `occupancy_rate` is 999999999 instead of a percentage for 56 cells; Chapter 8.3 does
  not use the column.

### Columns

| column | description |
|---|---|
| `id` | cell id |
| `inhabitants` | number of inhabitants in the cell |
| `occupancy_rate` | occupancy rate as percentage |
| `geometry` | `Polygon`, EPSG:3879 |
