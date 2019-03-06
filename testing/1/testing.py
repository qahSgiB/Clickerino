def test():
    import time

    import numpy as np
    from numba import jit, njit
    import imageio

    @njit
    def mandel(x, y, max_iters):
        """
        Given the real and imaginary parts of a complex number,
        determine if it is a candidate for membership in the Mandelbrot
        set given a fixed number of iterations.
        """
        i = 0
        c = complex(x,y)
        z = 0.0j
        for i in range(max_iters):
            z = z*z + c
            if (z.real*z.real + z.imag*z.imag) >= 16:
                return i*255/max_iters

        return 255

    @njit
    def create_fractal(min_x, max_x, min_y, max_y, image, iters):
        height = image.shape[0]
        width = image.shape[1]

        pixel_size_x = (max_x - min_x) / width
        pixel_size_y = (max_y - min_y) / height
        for x in range(width):
            real = min_x + x * pixel_size_x
            for y in range(height):
                imag = min_y + y * pixel_size_y
                color = mandel(real, imag, iters)
                image[y, x][0] = color
                distX = (np.power(real, 2)+np.power(imag, 2))/5
                image[y, x][1] = distX*255
                image[y, x][2] = 0

        return image

    image = np.zeros((500 * 2, 750 * 2, 3), dtype=np.uint8)
    s = time.time()
    create_fractal(-2.0, 1.0, -1.0, 1.0, image, 50)
    e = time.time()
    print(e - s)

    image = image.astype(np.uint8)

    imageio.imwrite('testing/1/mandelbrot.jpg', image)



if __name__ == '__main__':
    test()
