import cv2
import numpy as np


class Circle:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, img):
        cv2.circle(img, (self.x, self.y), self.r, self.color, -1)


def calcPos(t, start, v0, v1, a1, a2):
    pos = 0
    constant = 250*(v1-v0)
    if t < 500:
        pos = start + v0*t + 0.5*a1*t**2
    else:
        pos = start + v1*t + 0.5*a2*(t-500)**2 - constant

    return pos


radius = 20
color_c1 = (0, 255, 0)
color_c2 = (0, 255, 255)
color_c3 = (100, 0, 255)
color_c4 = (255, 0, 255)
start_x = 200
end_x = 1200
move_c1 = start_x
move_c2 = start_x
move_c3 = start_x
move_c4 = start_x

h_c1 = 200
h_c2 = 300
h_c3 = 400
h_c4 = 500

vel_c1 = 1/(end_x - start_x)


cnt = 0
while True:
    img = np.zeros((600, 1400, 3), np.uint8)

    circle1 = Circle(move_c1, h_c1, radius, color_c1)
    circle2 = Circle(move_c2, h_c2, radius, color_c2)
    circle3 = Circle(move_c3, h_c3, radius, color_c3)
    circle4 = Circle(move_c4, h_c4, radius, color_c4)

    circle1.draw(img)
    circle2.draw(img)
    circle3.draw(img)
    circle4.draw(img)
    cv2.imshow('Circle', img)
    cv2.waitKey(1)

    alpha = cnt * vel_c1

    move_c1 = int(start_x + (end_x - start_x)*alpha)        # 등속운동
    move_c2 = int(calcPos(cnt, start_x, 0.5, 1.5, 0.002, -0.002))  # 가속운동
    move_c3 = int(calcPos(cnt, start_x, 0, 2, 0.004, -0.004))  # 가속운동
    move_c4 = int(calcPos(cnt, start_x, 0.8, 1.5, 0.0014, -0.0026))  # 가속운동

    print(cnt, move_c3)

    if move_c1 > end_x:
        print(cnt)
        move_c1 = start_x
        move_c2 = start_x
        move_c3 = start_x
        move_c4 = start_x
        cnt = 0
    cnt += 1


cv2.destroyAllWindows()
