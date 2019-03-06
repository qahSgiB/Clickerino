def timeit(f):
    import time

    startTime = time.time()

    fResult = f()

    endTime = time.time()
    totalTime = endTime-startTime

    return totalTime, fResult

def test():
    import math

    import numpy
    import imageio
    import numba

    @numba.njit()
    def editImageCPU(image):
        image[:, :, 0] = (numpy.sin(image[:, :, 0]*2*math.pi/255)+1)*255/2
        image[:, :, 1] = 255-(numpy.sin(image[:, :, 1]*2*math.pi/255)+1)*255/2
        image[:, :, 2] = 0*(numpy.sin(image[:, :, 2]*2*math.pi/255)+1)*255/2

    image = imageio.imread('testing/bugar.jpg')

    image = image.astype(float)

    totalTime, result = timeit(lambda : editImageCPU(image))
    print('time: {time} ms'.format(time=totalTime))

    image = image.astype(numpy.uint8)

    imageio.imwrite('testing/bugarX.jpg', image)



if __name__ == '__main__':
    test()
