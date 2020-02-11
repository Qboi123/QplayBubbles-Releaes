from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points

poly = Polygon([(0, 0), (2, 8), (14, 10), (6, 1)])
point = Point(12, 4).buffer(2)
# The points are returned in the same order as the input geometries:
p1, p2 = nearest_points(poly, point)
print(poly.distance(point))
print(p1.wkt)
# POINT (10.13793103448276 5.655172413793103)
