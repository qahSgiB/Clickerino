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
            # a = pointPlane.point
            # b = pointPlane.vectors[0]
            # c = pointPlane.vectors[1]
            #
            # d = borderLine.point
            # e = borderLine.vectors[0]
            #
            # if c[1]*e[0]-e[1]*c[0] == 0:
            #     if c[2]*e[0]-e[2]*c[0] == 0:
            #         f = 1
            #     else:
            #         return None
            # else:
            #     f = (c[2]*e[0]-e[2]*c[0])/(c[1]*e[0]-e[1]*c[0])
            # k = (d[2]*e[0]-e[2]*d[0]-a[2]*e[0]+e[2]*a[0]-f*(d[1]*e[0]-e[1]*d[0]-a[1]*e[0]+e[1]*a[0]))/(b[2]*e[0]-e[2]*b[0]-f*(b[1]*e[0]-e[1]*b[0]))
            # if c[2]*e[0]-e[2]*c[0] == 0:
            #     if d[2]*e[0]-e[2]*d[0]-a[2]*e[0]+e[2]*a[0]-k*(b[2]*e[0]-e[2]*b[0]) != 0:
            #         return None
            #     else:
            #         l = (d[1]*e[0]-e[1]*d[0]-a[1]*e[0]+e[1]*a[0]-k*(b[1]*e[0]-e[1]*b[0]))/(c[1]*e[0]-e[1]*c[0])
            # else:
            #     l = (d[2]*e[0]-e[2]*d[0]-a[2]*e[0]+e[2]*a[0]-k*(b[2]*e[0]-e[2]*b[0]))/(c[2]*e[0]-e[2]*c[0])
            #
            # x = a[0]+b[0]*k+c[0]*l
            # y = a[1]+b[1]*k+c[1]*l
            # z = a[2]+b[2]*k+c[2]*l
            #
            # intersections.append(Point([x, y, z]))

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

            p = p4+p6.mult(t)
            intersections.append(p)

        planeCenter = Point(list(map(lambda a: (a[0]+a[1]+a[2]+a[3])/4, zip(intersections[0], intersections[1], intersections[2], intersections[3]))))
        planeDirection = planeCenter-self.camera.center

        def sameDir(a, b):
            if a == 0 or b == 0:
                return True
            else:
                return a/abs(a) == b/abs(b)

        if not all(list(map(lambda a: sameDir(a[0], a[1]), zip(planeDirection.coords, self.camera.direction)))) or planeDirection.getSize() < 0.000001:
            return None
        else:
            sizeX = (intersections[0]-intersections[1]).getSize()
            sizeY = (intersections[0]-intersections[3]).getSize()

            dists = list(map(lambda a: (point-a).getSize(), intersections))

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

    def get(self, index):
        return self.coords[index]

    def __getitem__(self, index):
        return self.get(index)

    def add(self, other):
        return Vector(list(map(lambda a: a[0]+a[1], zip(self.coords, other.coords))))

    def __add__(self, other):
        return self.add(other)

    def sub(self, other):
        return Vector(list(map(lambda a: a[0]-a[1], zip(self.coords, other.coords))))

    def __sub__(self, other):
        return self.sub(other)

    def mult(self, n):
        return Vector(list(map(lambda a: a*n, self.coords)))

    def __mult__(self, other):
        return self.mult(other)

    def getSize(self):
        return (sum(list(map(lambda a: a**2, self.coords))))**0.5

    def __len__(self):
        return self.getSize()

    def getDimensions(self):
        return len(self.coords)

class Point(Vector):
    pass

class LinearObject():
    def __init__(self, point, vectors):
        self.point = point
        self.vectors = vectors
        self.dimensions = self.point.getDimensions()

class Line(LinearObject):
    def __init__(self, point, vector1):
        super().__init__(point, [vector1])

class Plane(LinearObject):
    def __init__(self, point, vector1, vector2):
        super().__init__(point, [vector1, vector2])

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

        engine.setCamera(Camera32(center, vectorToCenter, [Vector([vectorToCenter[1], -vectorToCenter[0], 0]), Vector([0, 0, vectorToCenter.getSize()])]))
        # engine.setCamera(Camera32(Point([0, 10, 0]), Vector([0, -10, 0]), [Vector([10, 0, 0]), Vector([0, 0, 10])]))

        canvas.delete('all')

        for offset in [-6, -4, -2, 0, 2, 4, 6]:
            points = {}
            for pointX in [[1, 1, 1], [1, -1, 1], [-1, 1, 1] ,[-1, -1, 1], [1, 1, -1], [-1, 1, -1], [1, -1, -1] ,[-1, -1, -1]]:
                point = engine.calculatePoint(Point(pointX)+Vector([6-abs(offset), 0, offset]))
                points[tuple(pointX)] = point

            for pointAX in [[1, 1, 1], [1, -1, 1], [-1, 1, 1] ,[-1, -1, 1], [1, 1, -1], [-1, 1, -1], [1, -1, -1] ,[-1, -1, -1]]:
                for pointBX in [[1, 1, 1], [1, -1, 1], [-1, 1, 1] ,[-1, -1, 1], [1, 1, -1], [-1, 1, -1], [1, -1, -1] ,[-1, -1, -1]]:
                    if sum(list(map(lambda a: abs(a[0]-a[1]), zip(pointAX, pointBX)))) == 2:
                        pointA = points[tuple(pointAX)]
                        pointB = points[tuple(pointBX)]

                        if pointA != None and pointB != None:
                            pointAXX = pointA.mult(500)
                            pointBXX = pointB.mult(500)
                            canvas.create_line(pointAXX[0], pointAXX[1], pointBXX[0], pointBXX[1], fill='#000000')

        centerX = engine.calculatePoint(Point([0, 0, 0]))
        if centerX != None:
            center = centerX.mult(500)
            canvas.create_oval(center[0]-5, center[1]-5, center[0]+5, center[1]+5, fill='#FF0000')
        #
        # centerX = engine.calculatePoint(Point([0, 1, 0]))
        # if centerX != None:
        #     center = centerX.mult(500)
        #     canvas.create_oval(center[0]-5, center[1]-5, center[0]+5, center[1]+5, fill='#FF0000')

        if resume:
            canvas.after(50, update)

    update()

    root.mainloop()



if __name__ == '__main__':
    demo1()
