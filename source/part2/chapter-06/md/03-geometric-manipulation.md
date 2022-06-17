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

# Geometric data manipulations

- Buffer
- Centroid
- Convex hull / bounding box / envelope
- Unary union
- Simplify?
- Dissolving and merging geometries

## Buffer

## Centroid

## Unary union

## Convex hull, bounding box and envelope

Convex hull refers to the smalles possible polygon that contains all objects in a collection. Alongside with the minimum bounding box, convex hull is a useful shape when aiming to describe the extent of your data.  

Let's create a convex hull around our multi_point object:

```python
# Check input geometry
multi_point
```

```python
# Convex Hull (smallest polygon around the geometry collection)
multi_point.convex_hull
```

```python
# Envelope (smalles rectangular polygon around the geometry collection):
multi_point.envelope
```

## Simplification


## Dissolving and merging geometries





