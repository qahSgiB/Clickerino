# -------------------------------- lib: Space/Engine.py --------------------------------
#
import math



class Engine32():
    def __init__(self):
        self.camera = None

    def setCamera(self, newCamera):
        self.camera = newCamera

    def calculatePoint(self, point):
        pointPlane = Plane(point, self.camera.viewVectors[0], self.camera.viewVectors[1])

        intersections = []
        for borderLine in self.camera.getBorderLines():

            p1 = pointPlane.point
            p2 = p1+pointPlane.vectors[0]
            p3 = p1+pointPlane.vectors[1]

            p4 = borderLine.point
            p5 = p4+borderLine.vectors[0]

            p6 = borderLine.vectors[0]

            t1 = (p2[0]*(p3[1]*p4[2]-p4[1]*p3[2])-p3[0]*(p2[1]*p4[2]-p4[1]*p2[2])+p4[0]*(p2[1]*p3[2]-p3[1]*p2[2]))-(p1[0]*(p3[1]*p4[2]-p4[1]*p3[2])-p3[0]*(p1[1]*p4[2]-p4[1]*p1[2])+p4[0]*(p1[1]*p3[2]-p3[1]*p1[2]))+(p1[0]*(p2[1]*p4[2]-p4[1]*p2[2])-p2[0]*(p1[1]*p4[2]-p4[1]*p1[2])+p4[0]*(p1[1]*p2[2]-p2[1]*p1[2]))-(p1[0]*(p2[1]*p3[2]-p3[1]*p2[2])-p2[0]*(p1[1]*p3[2]-p3[1]*p1[2])+p3[0]*(p1[1]*p2[2]-p2[1]*p1[2]))
            t2 = (p2[0]*(p3[1]*p6[2]-p6[1]*p3[2])-p3[0]*(p2[1]*p6[2]-p6[1]*p2[2])+p6[0]*(p2[1]*p3[2]-p3[1]*p2[2]))-(p1[0]*(p3[1]*p6[2]-p6[1]*p3[2])-p3[0]*(p1[1]*p6[2]-p6[1]*p1[2])+p6[0]*(p1[1]*p3[2]-p3[1]*p1[2]))+(p1[0]*(p2[1]*p6[2]-p6[1]*p2[2])-p2[0]*(p1[1]*p6[2]-p6[1]*p1[2])+p6[0]*(p1[1]*p2[2]-p2[1]*p1[2]))
            if t2 == 0:
                return None
            t = -t1/t2

            p = p4+p6*t
            intersections.append(p)

        planeCenter = Point(list(map(lambda a: (a[0]+a[1]+a[2]+a[3])/4, zip(intersections[0], intersections[1], intersections[2], intersections[3]))))
        planeDirection = planeCenter-self.camera.center

        def sameDir(a, b):
            if a <= 0.000001 or b == 0.000001:
                return True
            else:
                return a/abs(a) == b/abs(b)

        if not all(list(map(lambda a: sameDir(a[0], a[1]), zip(planeDirection.coords, self.camera.direction)))) or planeDirection.getLength() < 0.000001:
            return None
        else:
            sizeX = (intersections[0]-intersections[1]).getLength()
            sizeY = (intersections[0]-intersections[3]).getLength()

            dists = list(map(lambda a: (point-a).getLength(), intersections))

            if dists[0] == 0:
                rX = 0
                rY = 0
            elif dists[1] == 0:
                rX = 1
                rY = 0
            elif dists[2] == 0:
                rX = 1
                rY = 1
            elif dists[3] == 0:
                rX = 0
                rY = 1
            else:
                acosX = lambda a: math.acos(round(a, 5))

                if (dists[3]**2-dists[0]**2-sizeY**2)/(-2*dists[0]*sizeY) > 1 or (dists[1]**2-dists[2]**2-sizeY**2)/(-2*dists[2]*sizeY) > 1 or (dists[1]**2-dists[0]**2-sizeX**2)/(-2*dists[0]*sizeX) > 1 or (dists[3]**2-dists[2]**2-sizeX**2)/(-2*dists[2]*sizeX) > 1:
                    return None

                a = acosX((dists[3]**2-dists[0]**2-sizeY**2)/(-2*dists[0]*sizeY))
                v = math.sin(a)*dists[0]
                rXA = v/sizeX

                a = acosX((dists[1]**2-dists[2]**2-sizeY**2)/(-2*dists[2]*sizeY))
                v = math.sin(a)*dists[2]
                rXB = v/sizeX

                a = acosX((dists[1]**2-dists[0]**2-sizeX**2)/(-2*dists[0]*sizeX))
                v = math.sin(a)*dists[0]
                rYA = v/sizeY

                a = acosX((dists[3]**2-dists[2]**2-sizeX**2)/(-2*dists[2]*sizeX))
                v = math.sin(a)*dists[2]
                rYB = v/sizeY

                if rXB > 1 and rXA < rXB:
                    rX = 1-rXB
                else:
                    rX = rXA
                if rYB > 1 and rYA < rYB:
                    rY = 1-rYB
                else:
                    rY = rYA

            return Point([rY, rX])

    def drawMesh(self, mesh, canvas):
        triangles = mesh.getTriangles()

        trianglesComparable = list(map(lambda a: TriangleConnectComparable(a, self), triangles))
        trianglesDrawDone = [False for i in range(len(trianglesComparable))]
        triangleTrianglesNeededDones = {}

        for triangle1Index in range(len(trianglesComparable)):
            triangleTrianglesNeededDones[triangle1Index] = []
            triangle1 = trianglesComparable[triangle1Index]

            for triangle2Index in range(len(trianglesComparable)):
                triangle2 = trianglesComparable[triangle2Index]
                if triangle1Index != triangle2Index:
                    if triangle1.compare(triangle2) < 0:
                        triangleTrianglesNeededDones[triangle1Index].append(triangle2Index)

        triangleToDraws = []
        for triangle in triangles:
            triangle2D = TriangleConnect(self.calculatePoint(triangle.point1), self.calculatePoint(triangle.point2), self.calculatePoint(triangle.point3), fill=triangle.fill)

            if triangle2D.point1 != None and triangle2D.point2 != None and triangle2D.point3 != None:
                triangleToDraws.append(triangle2D)

        canvasSizeVector = Vector([canvas.winfo_width(), canvas.winfo_height()])

        while not all(trianglesDrawDone):
            triangleFoundIndex = None
            for triangleIndex in range(len(triangleToDraws)):
                if not trianglesDrawDone[triangleIndex]:
                    ok = True
                    for neededTraingleIndex in triangleTrianglesNeededDones[triangleIndex]:
                        if not trianglesDrawDone[neededTraingleIndex]:
                            ok = False
                            break

                    if ok:
                        triangleFoundIndex = triangleIndex
                        break

            trianglesDrawDone[triangleFoundIndex] = True
            triangleToDraw = triangleToDraws[triangleFoundIndex]

            point1 = triangleToDraw.point1*canvasSizeVector
            point2 = triangleToDraw.point2*canvasSizeVector
            point3 = triangleToDraw.point3*canvasSizeVector

            canvas.create_polygon(point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], fill=triangleToDraw.fill, outline='')

class Camera32():
    def __init__(self, center, direction, viewVectors):
        self.center = center
        self.direction = direction
        self.viewVectors = viewVectors

    def getBorderLines(self):
        borberLines = (
            Line(self.center, self.direction+self.viewVectors[0]+self.viewVectors[1]),
            Line(self.center, self.direction+self.viewVectors[0]-self.viewVectors[1]),
            Line(self.center, self.direction-self.viewVectors[0]-self.viewVectors[1]),
            Line(self.center, self.direction-self.viewVectors[0]+self.viewVectors[1]),
        )

        return borberLines

# -------------------------------- lib: Space/Geometry.py --------------------------------
#
class Vector():
    def __init__(self, coords):
        self.coords = coords

    def generate(size, generator):
        return Vector([generator(index) for index in range(size)])

    def get(self, index):
        return self.coords[index]

    def getSize(self):
        return len(self.coords)

    def getLength(self):
        return sum(map(lambda a: a**2, self.coords))**0.5

    def add(self, other):
        return Vector(list(map(lambda a: a[0]+a[1], zip(self.coords, other.coords))))

    def sub(self, other):
        return Vector(list(map(lambda a: a[0]-a[1], zip(self.coords, other.coords))))

    def addNumber(self, other):
        return self.add(Vector.generate(self.getSize(), lambda index: other))

    def subNumber(self, other):
        return self.sub(Vector.generate(self.getSize(), lambda index: other))

    def mult(self, other):
        return Vector(list(map(lambda a: a[0]*a[1], zip(self.coords, other.coords))))

    def div(self, other):
        return Vector(list(map(lambda a: a[0]/a[1], zip(self.coords, other.coords))))

    def multNumber(self, other):
        return self.mult(Vector.generate(self.getSize(), lambda index: other))

    def divNumber(self, other):
        return self.div(Vector.generate(self.getSize(), lambda index: other))

    def scalarMult(self, other):
        return sum(self.mult(other).coords)

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return self.addNumber(other)
        elif isinstance(other, Vector):
            return self.add(other)

    def __sub__(self, other):
        if isinstance(other, (float, int)):
            return self.subNumber(other)
        elif isinstance(other, Vector):
            return self.sub(other)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return self.multNumber(other)
        elif isinstance(other, Vector):
            return self.mult(other)

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return self.divNumber(other)
        elif isinstance(other, Vector):
            return self.div(other)

    def __len__(self):
        return self.getSize()

    def __getitem__(self, index):
        return self.get(index)

class Point(Vector):
    pass

# -------------------------------- lib: Space/LinearGeometry.py --------------------------------
#
class LinearObject():
    def __init__(self, point, vectors):
        self.point = point
        self.vectors = vectors

    def getSize():
        return self.point.getSize()

class Line(LinearObject):
    def __init__(self, point, vector1):
        super().__init__(point, [vector1])

class Plane(LinearObject):
    def __init__(self, point, vector1, vector2):
        super().__init__(point, [vector1, vector2])

# -------------------------------- lib: Space/Mesh.py --------------------------------
#
class Fillable():
    def __init__(self, fill):
        self.fill = fill

class TriangleConnectComparable():
    def __init__(self, triangle, engine):
        self.triangle = triangle
        self.engine = engine

    def compare(self, other):
        aPoints = list(map(self.engine.calculatePoint, [self.triangle.point1, self.triangle.point2, self.triangle.point3]))
        bPoints = list(map(self.engine.calculatePoint, [other.triangle.point1, other.triangle.point2, other.triangle.point3]))

        aInB = False

        # s = lambda linePoint1, linePoint2, point:
        #
        # a0InB =

        if aInB:
            return 0
        else:
            intersections = []
            for aPoint1Index in range(len(aPoints)-1):
                aPoint1 = aPoints[aPoint1Index]
                for aPoint2Index in range(aPoint1Index+1, len(aPoints)):
                    aPoint2 = aPoints[aPoint2Index]

                    for bPoint1Index in range(len(bPoints)-1):
                        bPoint1 = bPoints[bPoint1Index]
                        for bPoint2Index in range(bPoint1Index+1, len(bPoints)):
                            bPoint2 = bPoints[bPoint2Index]

                            a = aPoint1
                            b = aPoint2
                            c = bPoint1
                            d = bPoint2

                            n1 = (c[0]-d[0])*(a[1]-b[1])-(c[1]-d[1])*(a[0]-b[0])
                            n2 = ((d[1]-b[1])*(a[0]-b[0])-(d[0]-b[0])*(a[1]-b[1]))
                            if n1 != 0:
                                n = n2/n1
                                m = ((b[1]-d[1])*(c[0]-d[0])-(b[0]-d[0])*(c[1]-d[1]))/(a[0]-b[0])*(c[1]-d[1])-(a[1]-b[1])*(c[0]-d[0])

                                intersection = d+(c-d)*n
                                m = (intersection-b)[0]/(a-b)[0]

                                if n >= 0.0001 and n <= 1-0.0001 and m >= 0.0001 and m <= 1-0.0001:
                                    intersections.append(intersection)

            if len(intersections) == 0:
                return 0
            else:
                for intersection in intersections:
                    v = self.engine.camera.direction+self.engine.camera.viewVectors[0]*(intersection[0]-0.5)+self.engine.camera.viewVectors[1]*(intersection[1]-0.5)

                    p1 = self.triangle.point1
                    p2 = self.triangle.point2
                    p3 = self.triangle.point3

                    p4 = self.engine.camera.center
                    p5 = p4+v
                    p6 = v

                    t1 = (p2[0]*(p3[1]*p4[2]-p4[1]*p3[2])-p3[0]*(p2[1]*p4[2]-p4[1]*p2[2])+p4[0]*(p2[1]*p3[2]-p3[1]*p2[2]))-(p1[0]*(p3[1]*p4[2]-p4[1]*p3[2])-p3[0]*(p1[1]*p4[2]-p4[1]*p1[2])+p4[0]*(p1[1]*p3[2]-p3[1]*p1[2]))+(p1[0]*(p2[1]*p4[2]-p4[1]*p2[2])-p2[0]*(p1[1]*p4[2]-p4[1]*p1[2])+p4[0]*(p1[1]*p2[2]-p2[1]*p1[2]))-(p1[0]*(p2[1]*p3[2]-p3[1]*p2[2])-p2[0]*(p1[1]*p3[2]-p3[1]*p1[2])+p3[0]*(p1[1]*p2[2]-p2[1]*p1[2]))
                    t2 = (p2[0]*(p3[1]*p6[2]-p6[1]*p3[2])-p3[0]*(p2[1]*p6[2]-p6[1]*p2[2])+p6[0]*(p2[1]*p3[2]-p3[1]*p2[2]))-(p1[0]*(p3[1]*p6[2]-p6[1]*p3[2])-p3[0]*(p1[1]*p6[2]-p6[1]*p1[2])+p6[0]*(p1[1]*p3[2]-p3[1]*p1[2]))+(p1[0]*(p2[1]*p6[2]-p6[1]*p2[2])-p2[0]*(p1[1]*p6[2]-p6[1]*p1[2])+p6[0]*(p1[1]*p2[2]-p2[1]*p1[2]))
                    t = -t1/t2

                    triangle1Distance = (p6*t).getLength()

                    p1 = other.triangle.point1
                    p2 = other.triangle.point2
                    p3 = other.triangle.point3

                    p4 = self.engine.camera.center
                    p5 = p4+v
                    p6 = v

                    t1 = (p2[0]*(p3[1]*p4[2]-p4[1]*p3[2])-p3[0]*(p2[1]*p4[2]-p4[1]*p2[2])+p4[0]*(p2[1]*p3[2]-p3[1]*p2[2]))-(p1[0]*(p3[1]*p4[2]-p4[1]*p3[2])-p3[0]*(p1[1]*p4[2]-p4[1]*p1[2])+p4[0]*(p1[1]*p3[2]-p3[1]*p1[2]))+(p1[0]*(p2[1]*p4[2]-p4[1]*p2[2])-p2[0]*(p1[1]*p4[2]-p4[1]*p1[2])+p4[0]*(p1[1]*p2[2]-p2[1]*p1[2]))-(p1[0]*(p2[1]*p3[2]-p3[1]*p2[2])-p2[0]*(p1[1]*p3[2]-p3[1]*p1[2])+p3[0]*(p1[1]*p2[2]-p2[1]*p1[2]))
                    t2 = (p2[0]*(p3[1]*p6[2]-p6[1]*p3[2])-p3[0]*(p2[1]*p6[2]-p6[1]*p2[2])+p6[0]*(p2[1]*p3[2]-p3[1]*p2[2]))-(p1[0]*(p3[1]*p6[2]-p6[1]*p3[2])-p3[0]*(p1[1]*p6[2]-p6[1]*p1[2])+p6[0]*(p1[1]*p3[2]-p3[1]*p1[2]))+(p1[0]*(p2[1]*p6[2]-p6[1]*p2[2])-p2[0]*(p1[1]*p6[2]-p6[1]*p1[2])+p6[0]*(p1[1]*p2[2]-p2[1]*p1[2]))
                    t = -t1/t2

                    triangle2Distance = (p6*t).getLength()

                    if triangle1Distance-triangle2Distance != 0:
                        return triangle1Distance-triangle2Distance

            return 0

class TriangleConnect(Fillable):
    def __init__(self, point1, point2, point3, fill=None):
        Fillable.__init__(self, fill)

        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

class LineConnect():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

class Mesh():
    def __init__(self, points, triangles):
        self.points = points
        self.triangles = triangles

    def getTriangles(self):
        trianglesX = []

        for triangle in self.triangles:
            trianglesX.append(TriangleConnect(self.points[triangle.point1], self.points[triangle.point2], self.points[triangle.point3], triangle.fill))

        return trianglesX

# -------------------------------- Game.py --------------------------------
#
class Game():
    def __init__(self):
        pass



def main():
    pass

def demo1():
    import tkinter

    engine = Engine32()

    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width=500, height=500, bg='#FFFFFF', highlightthickness=0)
    canvas.pack()

    def pause(event):
        nonlocal resume

        resume = not resume

        if resume:
            update()

    def reverseCamera(event):
        nonlocal vel

        vel *= -1

    def step(event):
        update()

    canvas.bind('<1>', pause)
    canvas.bind('<2>', step)
    canvas.bind('<3>', reverseCamera)
    canvas.focus_set()

    resume = True
    pos = 0
    vel = 5

    def update():
        nonlocal pos, vel

        pos += vel

        angle = math.radians(pos)

        centerX = math.cos(angle)*10
        centerY = math.sin(angle)*10
        center = Point([centerX, centerY, 0])

        vectorToCenter = Point([0, 0, 0])-center

        engine.setCamera(Camera32(center, vectorToCenter, [Vector([vectorToCenter[1], -vectorToCenter[0], 0]), Vector([0, 0, vectorToCenter.getLength()])]))

        canvas.delete('all')

        for offset in [6, 4, 2, 0]:
            n = 1

            points = {}
            for pointX in [[n, 1, 1], [n, -1, 1], [-n, 1, 1] ,[-n, -1, 1], [n, 1, -1], [-n, 1, -1], [n, -1, -1] ,[-n, -1, -1]]:
                point = engine.calculatePoint(Point(pointX)+Vector([abs(offset), 0, offset]))
                points[tuple(pointX)] = point

            for pointAX in [[n, 1, 1], [n, -1, 1], [-n, 1, 1] ,[-n, -1, 1], [n, 1, -1], [-n, 1, -1], [n, -1, -1] ,[-n, -1, -1]]:
                for pointBX in [[n, 1, 1], [n, -1, 1], [-n, 1, 1] ,[-n, -1, 1], [n, 1, -1], [-n, 1, -1], [n, -1, -1] ,[-n, -1, -1]]:
                    dist = list(map(lambda a: abs(a[0]-a[1]), zip(pointAX, pointBX)))
                    if dist.count(0) == len(dist)-1:
                        pointA = points[tuple(pointAX)]
                        pointB = points[tuple(pointBX)]

                        if pointA != None and pointB != None:
                            pointAXX = pointA*500
                            pointBXX = pointB*500
                            canvas.create_line(pointAXX[0], pointAXX[1], pointBXX[0], pointBXX[1], fill='#000000')

        centerX = engine.calculatePoint(Point([0, 0, 0]))
        if centerX != None:
            center = centerX*500
            canvas.create_oval(center[0]-5, center[1]-5, center[0]+5, center[1]+5, fill='#FF0000')

        if resume:
            canvas.after(25, update)

    update()

    root.mainloop()

def demo2():
    import tkinter
    import time

    engine = Engine32()

    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width=500, height=500, bg='#FFFFFF', highlightthickness=0)
    canvas.pack()

    def pause(event):
        nonlocal resume

        resume = not resume

        if resume:
            update()

    def reverseCamera(event):
        nonlocal vel

        vel *= -1

    def step(event):
        update()

    canvas.bind('<1>', pause)
    canvas.bind('<2>', step)
    canvas.bind('<3>', reverseCamera)
    canvas.focus_set()

    resume = True
    pos = 0
    vel = 5

    lasttime = 0

    cube = Mesh(
        [
            Point([1, 1, 1]),
            Point([1, 1, -1]),
            Point([1, -1, 1]),
            Point([1, -1, -1]),

            Point([-1, 1, 1]),
            Point([-1, 1, -1]),
            Point([-1, -1, 1]),
            Point([-1, -1, -1]),
        ],
        [
            TriangleConnect(0, 1, 2, '#00FFFF'),
            TriangleConnect(3, 1, 2, '#00FFFF'),
            TriangleConnect(4, 5, 6, '#FF0000'),
            TriangleConnect(7, 5, 6, '#FF0000'),

            TriangleConnect(0, 1, 4, '#00FF00'),
            TriangleConnect(5, 1, 4, '#00FF00'),
            TriangleConnect(2, 3, 6, '#0000FF'),
            TriangleConnect(7, 3, 6, '#0000FF'),

            TriangleConnect(0, 2, 4, '#FF00FF'),
            TriangleConnect(6, 2, 4, '#FF00FF'),
            TriangleConnect(1, 3, 5, '#FFFF00'),
            TriangleConnect(7, 3, 5, '#FFFF00'),
        ])

    def update():
        nonlocal pos, vel, lasttime

        pos += vel

        angle = math.radians(pos)

        centerX = math.cos(angle)*10
        centerY = math.sin(angle)*10
        center = Point([centerX, centerY, 5])

        vectorToCenter = Point([0, 0, 0])-center

        engine.setCamera(Camera32(center, vectorToCenter, [Vector([vectorToCenter[1], -vectorToCenter[0], 0]), Vector([0, 0, vectorToCenter.getLength()])]))

        canvas.delete('all')

        engine.drawMesh(cube, canvas)

        if resume:
            timeNow = time.time()
            print(1/(timeNow-lasttime))
            lasttime = timeNow

            canvas.after(25, update)

    update()

    root.mainloop()



if __name__ == '__main__':
    demo2()
