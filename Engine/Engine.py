import numpy
import numba
import queue

import math
import time
import tkinter



class Engine():
    def __init__(self):
        self.camera = None
        self.tre = 0.000005

    def setCamera(self, camera):
        self.camera = camera

    def calculatePoint(self, point):
        d = self.camera.directionVector
        v = self.camera.viewVector1
        u = self.camera.viewVector2
        q = self.camera.center
        p = point

        o = p-q

        det = numpy.linalg.det(numpy.stack([d, v, u]))

        aDet = numpy.linalg.det(numpy.stack([o, v, u]))
        bDet = numpy.linalg.det(numpy.stack([d, o, u]))
        cDet = numpy.linalg.det(numpy.stack([d, v, o]))

        a = aDet/det
        b = bDet/det
        c = cDet/det

        if a <= 0:
            return None
        else:
            xMultiplier = b/a
            yMultiplier = c/a

            return (numpy.array([xMultiplier, yMultiplier])+1)/2

    def calculatePoints(self, points):
        return numpy.stack([self.calculatePoint(point) for point in points])

    def calculateObject(self, object):
        cameraCenter = self.camera.center
        objectPoints2D = self.calculatePoints(object.points)

        def getOrder(face1, face2):
            # 1 = face1 first / -1 = face2 first / 0 = doesn't matter

            face12D = [objectPoints2D[face1[0]], objectPoints2D[face1[1]], objectPoints2D[face1[2]]]
            face13D = [object.points[face1[0]], object.points[face1[1]], object.points[face1[2]]]

            face22D = [objectPoints2D[face2[0]], objectPoints2D[face2[1]], objectPoints2D[face2[2]]]
            face23D = [object.points[face2[0]], object.points[face2[1]], object.points[face2[2]]]

            face12DX = [face12D[0][0], face12D[1][0], face12D[2][0]]
            face12DY = [face12D[0][1], face12D[1][1], face12D[2][1]]

            face22DX = [face22D[0][0], face22D[1][0], face22D[2][0]]
            face22DY = [face22D[0][1], face22D[1][1], face22D[2][1]]

            if abs(min(face12DX)-max(face22DX)) <= self.tre or abs(max(face12DX)-min(face22DX)) <= self.tre or abs(min(face12DY)-max(face22DY)) <= self.tre or abs(max(face12DY)-min(face22DY)) <= self.tre:
                return 0

            intersections = []

            combs = [
                ((0, 1), (0, 1)),
                ((0, 1), (1, 2)),
                ((0, 1), (0, 2)),

                ((1, 2), (0, 1)),
                ((1, 2), (1, 2)),
                ((1, 2), (0, 2)),

                ((0, 2), (0, 1)),
                ((0, 2), (1, 2)),
                ((0, 2), (0, 2)),
            ]

            order = 0

            for comb in combs:
                comb1, comb2 = comb

                v = face12D[comb1[1]]-face12D[comb1[0]]
                u = face22D[comb2[1]]-face22D[comb2[0]]
                o = face22D[comb2[0]]-face12D[comb1[0]]

                det = -v[0]*u[1]+v[1]*u[0]

                parallel = None
                if u[0] == 0:
                    parallel = v[0] == 0
                elif u[1] == 0:
                    parallel = v[1] == 0
                else:
                    parallel = abs((v[0]/u[0])-(v[1]/u[1])) < self.tre

                if det != 0 and not parallel:
                    aDet = -o[0]*u[1]+o[1]*u[0]
                    bDet = v[0]*o[1]-v[1]*o[0]

                    a = aDet/det
                    b = bDet/det

                    if a >= 0-self.tre and a <= 1+self.tre and b >= 0-self.tre and b <= 1+self.tre:
                        face1point = face13D[comb1[0]]+a*(face13D[comb1[1]]-face13D[comb1[0]])
                        face2point = face23D[comb2[0]]+b*(face23D[comb2[1]]-face23D[comb2[0]])

                        face1pointDistVector = cameraCenter-face1point
                        face1pointDist = face1pointDistVector[0]**2+face1pointDistVector[1]**2
                        face2pointDistVector = cameraCenter-face2point
                        face2pointDist = face2pointDistVector[0]**2+face2pointDistVector[1]**2

                        if abs(face1pointDist-face2pointDist) <= self.tre:
                            pass
                        elif face1pointDist < face2pointDist:
                            order = 1
                        elif face1pointDist > face2pointDist:
                            order = -1

                        if order != 0:
                            break

            if order == 0:
                points = []

                v = face22D[1]-face22D[0]
                u = face22D[2]-face22D[1]
                det = v[0]*u[1]-v[1]*u[0]

                if det != 0:
                    for face1PointIndex in range(3):
                        face12Dpoint = face12D[face1PointIndex]
                        o = face12Dpoint-face22D[0]

                        aDet = o[0]*u[1]-o[1]*u[0]
                        bDet = v[0]*o[1]-v[1]*o[0]

                        a = aDet/det
                        b = bDet/det

                        if a <= 1+self.tre and a >= 0-self.tre and b <= a and b >= 0-self.tre:
                            face1point = face13D[face1PointIndex]
                            face2point = face23D[0]*(1-a)+face23D[1]*(a-b)+face23D[2]*b

                            face1pointDistVector = cameraCenter-face1point
                            face1pointDist = face1pointDistVector[0]**2+face1pointDistVector[1]**2
                            face2pointDistVector = cameraCenter-face2point
                            face2pointDist = face2pointDistVector[0]**2+face2pointDistVector[1]**2

                            if abs(face1pointDist-face2pointDist) <= self.tre:
                                pass
                            elif face1pointDist < face2pointDist:
                                order = 1
                            elif face1pointDist > face2pointDist:
                                order = -1

                            if order != 0:
                                break

            if order == 0:
                v = face12D[1]-face12D[0]
                u = face12D[2]-face12D[1]
                det = v[0]*u[1]-v[1]*u[0]

                if det != 0:
                    for face2PointIndex in range(3):
                        face22Dpoint = face22D[face2PointIndex]
                        o = face22Dpoint-face12D[0]

                        aDet = o[0]*u[1]-o[1]*u[0]
                        bDet = v[0]*o[1]-v[1]*o[0]

                        a = aDet/det
                        b = bDet/det

                        if a <= 1+self.tre and a >= 0-self.tre and b <= a and b >= 0-self.tre:
                            face2point = face23D[face2PointIndex]
                            face1point = face13D[0]*(1-a)+face13D[1]*(a-b)+face13D[2]*b

                            face1pointDistVector = cameraCenter-face1point
                            face1pointDist = face1pointDistVector[0]**2+face1pointDistVector[1]**2
                            face2pointDistVector = cameraCenter-face2point
                            face2pointDist = face2pointDistVector[0]**2+face2pointDistVector[1]**2

                            if abs(face1pointDist-face2pointDist) <= self.tre:
                                pass
                            elif face1pointDist < face2pointDist:
                                order = 1
                            elif face1pointDist > face2pointDist:
                                order = -1

                            if order != 0:
                                break

            return order

        objectFaces = []
        objectMaterials = []
        for objectFaceIndex in range(len(object.faces)):
            objectFace = object.faces[objectFaceIndex]
            objectMaterial = object.materials[objectFaceIndex]

            point2Dexists = lambda pointIndex: objectPoints2D[pointIndex] is not None
            if point2Dexists(objectFace[0]) and point2Dexists(objectFace[1]) and point2Dexists(objectFace[2]):
                objectFaces.append(objectFace)
                objectMaterials.append(objectMaterial)
        objectFaces = numpy.array(objectFaces)
        objectMaterials = numpy.array(objectMaterials)

        facesCount = len(objectFaces)
        facesAfter = [[] for i in range(facesCount)]
        faceNeeded = numpy.array([0 for i in range(facesCount)])

        for face1index in range(facesCount-1):
            for face2index in range(face1index+1, facesCount):
                face1 = objectFaces[face1index]
                face2 = objectFaces[face2index]

                order = getOrder(face1, face2)

                if order == -1:
                    facesAfter[face1index].append(face2index)
                    faceNeeded[face2index] += 1
                elif order == 1:
                    facesAfter[face2index].append(face1index)
                    faceNeeded[face1index] += 1

        facesOrdered = []

        faceQueue = queue.Queue()
        for faceIndex in range(facesCount):
            if faceNeeded[faceIndex] == 0:
                faceQueue.put(faceIndex)

        while not faceQueue.empty():
            faceIndex = faceQueue.get()

            facesOrdered.append(faceIndex)

            for faceAfter in facesAfter[faceIndex]:
                faceNeeded[faceAfter] -= 1
                if faceNeeded[faceAfter] == 0:
                    faceQueue.put(faceAfter)

        for faceIndex in range(facesCount):
            if faceNeeded[faceIndex] != 0:
                print(faceIndex, faceNeeded[faceIndex], facesAfter[faceIndex])

        faces = []
        for faceIndex in facesOrdered:
            face = objectFaces[faceIndex]
            faces.append((numpy.array([objectPoints2D[face[0]], objectPoints2D[face[1]], objectPoints2D[face[2]]]), objectMaterials[faceIndex]))
        faces = numpy.stack(faces)

        return faces

class Camera():
    def __init__(self, center, directionVector, viewVector1, viewVector2):
        self.center = center
        self.directionVector = directionVector
        self.viewVector1 = viewVector1
        self.viewVector2 = viewVector2

class Object():
    def __init__(self, points, faces, materials):
        self.points = points
        self.faces = faces
        self.materials = materials

    def loadFromFile(folderPath):
        points = []
        faces = []
        materials = []

        with open(folderPath+'/object.obj', 'r') as file:
            lines = file.read().split('\n')

            materialsDict = None
            activeMaterial = None

            for line in lines:
                if len(line) > 0:
                    infos = line.split(' ')
                    infoType = infos[0]

                    if infoType == 'mtllib':
                        materialsDict = Material.loadFromFile(folderPath)
                    if infoType == 'usemtl':
                        activeMaterial = infos[1]
                    if infoType == 'v':
                        points.append(numpy.array([float(infos[1]), float(infos[2]), float(infos[3])]))
                    elif infoType == 'f':
                        faces.append(numpy.array([int(infos[1])-1, int(infos[2])-1, int(infos[3])-1]))

                        if activeMaterial != None:
                            materials.append(materialsDict[activeMaterial])
                        else:
                            materials.append(None)

        return Object(numpy.stack(points), numpy.stack(faces), materials)

class Material():
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def loadFromFile(folderPath):
        materials = {}

        with open(folderPath+'/object.mtl', 'r') as file:
            lines = file.read().split('\n')

            name = None
            color = None

            for line in lines:
                if len(line) > 0:
                    infos = line.split(' ')
                    infoType = infos[0]

                    if infoType == 'newmtl':
                        if name != None:
                            materials[name] = Material(name, color)

                        name = infos[1]
                    elif infoType == 'Kd':
                        red, green, blue = int(float(infos[1])*255), int(float(infos[2])*255), int(float(infos[3])*255)
                        color = f'#{red:02x}{green:02x}{blue:02x}'

            materials[name] = Material(name, color)

        return materials



class Demo():
    def __init__(self, canvasSize, object, cameraDistance, printDelay=False, period=60):
        self.canvasSize = canvasSize
        self.object = object
        self.cameraDistance = cameraDistance

        self.printDelay = printDelay
        self.lastTime = None

        self.running = False
        self.after = None
        self.period = period

        self.state = 0
        self.stateVel = 1

        self.engine = Engine()

        self.tk = tkinter.Tk()
        self.tk.title('_')

        self.canvas = tkinter.Canvas(self.tk, width=self.canvasSize[0], height=self.canvasSize[1], bg='#FFFFFF', highlightthickness=0)
        self.canvas.bind('<1>', lambda event: self.pause())
        self.canvas.bind('<2>', lambda event: self.reverse())
        self.canvas.bind('<3>', lambda event: self.step())
        self.canvas.pack()

    def run(self):
        self.start()
        self.tk.mainloop()

    def start(self):
        self.lastTime = None

        self.running = True
        self.loop()

    def stop(self):
        self.running = False
        self.tk.after_cancel(self.after)

    def pause(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def reverse(self):
        self.stateVel *= -1

    def step(self):
        if not self.running:
            self.update()

    def update(self):
        self.state += self.stateVel

        self.canvas.delete('all')

        angle = math.radians((5*self.state)%360)
        h = math.sin(angle*2)*2

        direction0 = numpy.sin(angle)*self.cameraDistance
        direction1 = numpy.cos(angle)*self.cameraDistance
        cameraCenter = numpy.array([-direction0, -direction1, h])
        cameraDirectionVector = numpy.array([direction0, direction1, 0])
        cameraViewVector0 = numpy.array([direction1, -direction0, 0])
        cameraViewVector1 = numpy.array([0, 0, self.cameraDistance])

        self.engine.setCamera(Camera(cameraCenter, cameraDirectionVector, cameraViewVector0, cameraViewVector1))

        faces = self.engine.calculateObject(self.object)

        for face in faces:
            objectFace2D, material = face

            point1 = objectFace2D[0]*self.canvasSize
            point2 = objectFace2D[1]*self.canvasSize
            point3 = objectFace2D[2]*self.canvasSize

            color = None
            if material == None:
                color = '#222222'
            else:
                color = material.color

            self.canvas.create_polygon(point1[0], point1[1], point2[0], point2[1], point3[0], point3[1], outline='', fill=color, width=5)

    def loop(self):
        self.update()

        if self.printDelay:
            actualTime = time.time()
            if self.lastTime != None:
                period = actualTime-self.lastTime
                periodMs = period*1000
                delay = periodMs-self.period
                fps = 1/period

                print()
                print(f'fps: {fps:.4f}')
                print(f'period: {periodMs:.4f} ms')
                print(f'delay: {delay:.4f} ms')

            self.lastTime = actualTime

        if self.running:
            self.after = self.tk.after(self.period, self.loop)



def test():
    import tkinter

    cube = Object.loadFromFile('3DObjects/spaceShip')

    canvasSize = numpy.array([500, 500])

    demo = Demo(canvasSize, cube, 20, True, 5).run()



if __name__ == '__main__':
    test()
