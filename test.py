from lib.base import Point2D

if __name__ == '__main__':
    point1 = Point2D(32, 105)
    point2 = Point2D(18, 83)
    point3 = point1 + point2
    print(point3)
    print(point3.x, point3.y)
