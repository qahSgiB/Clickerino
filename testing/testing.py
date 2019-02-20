def test():
    import math

    import numpy
    import imageio

    image = imageio.imread('testing/bugar.jpg')

    image = image.astype(float)

    imageWidth = image.shape[1]
    imageHeight = image.shape[0]

    # sinArray = numpy.arange(imageWidth, dtype=float)
    # for el in numpy.nditer(sinArray, op_flags=['readwrite']):
    #     x = (el/(imageWidth/2))*math.pi
    #     sin = math.sin(x+(math.pi/2))/2+0.5
    #     el[...] = sin/2+0.25

    image[:, :, 0] = (numpy.sin(image[:, :, 0]*2*math.pi/255)+1)*255/2
    image[:, :, 1] = 255-(numpy.sin(image[:, :, 1]*2*math.pi/255)+1)*255/2
    image[:, :, 2] = 0.5*(numpy.sin(image[:, :, 2]*2*math.pi/255)+1)*255/2
    # image[:, :, 1] *= 0
    # image[:, :, 2] *= 0
    # image[:, :, 2] = 255-image[:, :, 2]

    image = image.astype(numpy.uint8)

    imageio.imwrite('testing/bugarX.jpg', image)

    # x = numpy.array([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]])
    #
    # print(x[:, :, 1].shape)



if __name__ == '__main__':
    test()
