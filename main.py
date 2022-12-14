from PIL import Image
import numpy as np
import math

def image_gen(figure):
    pixel_image = np.full(shape=(540, 960, 3), fill_value = [255, 255, 255], dtype=np.uint8)
    pixel_image[figure[:, 0], figure[:, 1]] = [0, 0, 255]

    return pixel_image

def project(data, vp=(540, 960), distanse=15):
    start_point = (540, 0)
    data[:, 0] -= vp[0] - start_point[0]
    data[:, 0] = distanse * data[:, 0] / (distanse + data[:, 2])
    data[:, 0] += vp[0] - start_point[0]
    data[:, 1] -= vp[1] - start_point[1]
    data[:, 1] = distanse * data[:, 1] / (distanse + data[:, 2])
    data[:, 1] += vp[1] - start_point[1]
    return data

def load_data(path):
    data = np.loadtxt(path, dtype=int)
    data[:, 0] = 959 - data[:, 0]
    data = np.insert(data, 2, [100] * len(data), axis=1)

    return data

if __name__ == '__main__':
    canvas_width, canvas_height = 960, 960
    x0, y0 = 480, 480
    n = 8
    alpha = 10 * (n + 1) * math.pi / 180
    arr = np.zeros([canvas_height, canvas_width, 3], dtype=np.uint8)
    for x in range(canvas_width):
        for y in range(canvas_height):
            arr[y, x, 0] = 255
            arr[y, x, 1] = 255
            arr[y, x, 2] = 255
    i = 0
    with open('datasets/DS8.txt') as ds:
        with open('datasets/ds_new.txt',mode = "wt" ) as ds_new:
            for line in ds:
                [y, x] = list(map(int, line.split()))
                x, y = x - x0, y - y0
                x, y = x * math.cos(alpha) - y * math.sin(alpha), x * math.sin(alpha) + y * math.cos(alpha)
                x, y = int(x + x0), int(y + y0)
                ds_new.write(f"{y} {x}\n") # збереження нових координат датасету для використання в лаботраторній роботі номер 4
                y = canvas_height - y - 1
                i += 1
                if 0 <= x < canvas_width and 0 <= y < canvas_height:
                    arr[y, x, 0] = 0
                    arr[y, x, 1] = 0
                    arr[y, x, 2] = 255
    print(i)
    # img = Image.fromarray(arr)
    # img.save('images/canvas.png')
    # перетворення згідно лабораторної номер 4
    image_projection = image_gen(project(load_data('datasets/ds_new.txt')))
    img = Image.fromarray(image_projection, 'RGB')
    img.save('images/perspective_projection.png')




