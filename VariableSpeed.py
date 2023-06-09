import cv2
import numpy as np
import matplotlib.pyplot as plt


class Circle:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, img):
        cv2.circle(img, (self.x, self.y), self.r, self.color, -1)


radius = 20
color_c1 = (0, 255, 0)
color_c2 = (120, 255, 0)
color_c3 = (0, 255, 255)
color_c4 = (100, 0, 255)
color_c5 = (255, 0, 255)
start = 200
end_x = 1200

move_c1 = start
move_c2 = start
move_c3 = start
move_c4 = start
move_c5 = start

h_c1 = 200
h_c2 = 300
h_c3 = 400
h_c4 = 500
h_c5 = 600

vel_c1 = 1/(end_x - start)

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []

cnt = 0
whole_time = 1000
duration = 1000


def calcPos(t, type, param):
    pos = 0
    v0 = 0
    v1 = 0
    a1 = 0
    a2 = 0

    if type == 'triangle':
        v0 = duration/whole_time * (1-param)
        v1 = 2*duration/whole_time - v0
        a1 = 4*duration/(whole_time**2) - (4/whole_time)*v0
        a2 = -a1

    elif type == 'trapezoid':
        T = whole_time
        k = T * 0.6
        p = (T - k) * 0.5

        v0 = 0
        v1 = duration/(k+p)
        a1 = v1/p
        a2 = -a1
        constant = 0

        if t >= 0 and t < p:
            pos = start + v0*t + 0.5*a1*t**2
        elif t >= p and t < T-p:
            pos = start + 0.5*p*v1 + v1*(t-p) - constant
        else:
            pos = start + 0.5*p*v1 + v1*(t-p) + 0.5*a2*(t-p-k)**2 - constant
        return pos

    half = whole_time * 0.5
    constant = 0.25*whole_time*(v1-v0)

    if t < half:
        pos = start + v0*t + 0.5*a1*t**2
    else:
        pos = start + v1*t + 0.5*a2*(t-half)**2 - constant

    return pos


def calcZoom(t, start_zoom, end_zoom):
    zoom = 0
    interval = end_zoom - start_zoom
    v0 = interval/whole_time * 0
    v1 = 2*interval/whole_time - v0
    a1 = 4*interval/(whole_time**2) - (4/whole_time)*v0
    a2 = -a1

    half = whole_time * 0.5
    constant = 0.25*whole_time*(v1-v0)

    if t < half:
        zoom = radius + v0*t + 0.5*a1*t**2
    else:
        zoom = radius + v1*t + 0.5*a2*(t-half)**2 - constant

    return zoom


# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (1400, 600))


# velocity test
# while True:
#     img = np.zeros((700, 1400, 3), np.uint8)

#     circle1 = Circle(int(move_c1), h_c1, radius, color_c1)
#     circle2 = Circle(int(move_c2), h_c2, radius, color_c2)
#     circle3 = Circle(int(move_c3), h_c3, radius, color_c3)
#     circle4 = Circle(int(move_c4), h_c4, radius, color_c4)
#     circle5 = Circle(int(move_c5), h_c5, radius, color_c5)

#     circle1.draw(img)
#     circle2.draw(img)
#     circle3.draw(img)
#     circle4.draw(img)
#     circle5.draw(img)
#     cv2.imshow('Circle', img)
#     # out.write(img)
#     cv2.waitKey(1)

#     alpha = cnt * vel_c1

#     move_c1 = int(start + (end_x - start)*alpha)        # 등속운동
#     move_c2 = calcPos(cnt, 'triangle', 0.4)               # 가속운동
#     move_c3 = calcPos(cnt, 'triangle', 0.8)               # 가속운동
#     move_c4 = calcPos(cnt, 'triangle', 1)
#     move_c5 = calcPos(cnt, 'trapezoid', 0)

#     # print(cnt, move_c4)

#     x.append(cnt)
#     y1.append(move_c1)
#     y2.append(move_c2)
#     y3.append(move_c3)
#     y4.append(move_c4)
#     y5.append(move_c5)

#     if cnt > whole_time:
#         # break
#         print(cnt)
#         cnt = 0
#     cnt += 1


# out.release()
# cv2.destroyAllWindows()
# zoom test
while True:
    img = np.zeros((1200, 1400, 3), np.uint8)
    r = int(radius*(1 + 4*(cnt / whole_time)))
    r3 = int(calcZoom(cnt, radius, radius*5))
    print(r, r3)

    circle1 = Circle(int(move_c1), 300, r, color_c1)
    circle1.draw(img)
    circle2 = Circle(int(move_c2), 600, r, color_c2)
    circle2.draw(img)
    circle3 = Circle(int(move_c2), 900, r3, color_c3)
    circle3.draw(img)

    cv2.imshow('Circle', img)
    cv2.waitKey(1)

    alpha = cnt * vel_c1

    move_c1 = int(start + (end_x - start)*alpha)
    move_c2 = calcPos(cnt, 'triangle', 0.5)
    move_c3 = int(start + (end_x - start)*alpha)
    # x.append(cnt)
    # y1.append(move_c1)

    if cnt > whole_time:
        # break
        print(cnt)
        cnt = 0
        r = radius
        r3 = radius
    cnt += 1


# draw Graphs
fig, axs = plt.subplots(2, 4, figsize=(18, 8))

axs[0][0].plot(x, y1, 'g')
axs[0][0].set_title('constant velocity')

axs[0][1].plot(x, y2, 'y')
axs[0][1].set_title('easy ease')

axs[0][2].plot(x, y3, 'pink')
axs[0][2].set_title('more faster')

axs[0][3].plot(x, y4, 'purple')
axs[0][3].set_title('flatten the middle')

y1_deriv = np.gradient(y1, x)
axs[1][0].plot(x, y1_deriv, 'g')

y2_deriv = np.gradient(y2, x)
axs[1][1].plot(x, y2_deriv, 'y')
axs[1][1].set_ylim([0, None])

y3_deriv = np.gradient(y3, x)
axs[1][2].plot(x, y3_deriv, 'pink')

y4_deriv = np.gradient(y4, x)
axs[1][3].plot(x, y4_deriv, 'purple')

plt.show()
