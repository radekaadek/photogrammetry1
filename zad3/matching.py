import cv2
import numpy as np

img = cv2.imread('724.tif')
img2 = cv2.imread('724.tif')
gImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img2_coords = """1	110.0210000000	0.0000000000
2	-109.9880000000	-0.0080000000
3	0.0190000000	110.0000000000
4	0.0120000000	-110.0140000000
5	110.0250000000	110.0000000000
6	-109.9890000000	-110.0040000000
7	-109.9800000000	110.0040000000
8	110.0100000000	-110.0030000000"""

img2_coords = img2_coords.split('\n')
img2_coords = [x.split('\t') for x in img2_coords]
img2_coords = [(float(x[2]), float(x[1])) for x in img2_coords]
print(img2_coords)

img1_coords = []

scale = 3

def print_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x // scale + param[0], y // scale + param[1])
        img1_coords.append((x // scale + param[0], y // scale + param[1]))

templates = [cv2.imread('cross.png', 0), cv2.imread('cross2.png', 0)]
for template in templates:
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(gImg, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)

    # detect connected components
    _, labels = cv2.connectedComponents(np.uint8(res >= threshold))

    for label in range(1, np.max(labels) + 1):
        loc = np.where(labels == label)
        top_left = (np.min(loc[1]), np.min(loc[0]))
        right_bottom = (np.max(loc[1]) + w, np.max(loc[0]) + h)

        # show the image cut by the template
        image_cut = img[top_left[1]:right_bottom[1], top_left[0]:right_bottom[0]]
        cv2.imshow('img', image_cut)
        # resize image to be larger by 9x
        dsize = (image_cut.shape[1] * scale, image_cut.shape[0] * scale)
        output = cv2.resize(image_cut, dsize)
        cv2.imshow('img', output)
        # on double click print the coordinates
        cv2.setMouseCallback('img', print_coordinates, right_bottom)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()

print(img1_coords)

def print_coordinates2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x // scale + param[0], y // scale + param[1])
        img2_coords.append((x // scale + param[0], y // scale + param[1]))

# # now img2
# gImg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# img2_coords = []
#
# for template in templates:
#     w, h = template.shape[::-1]
#
#     res = cv2.matchTemplate(gImg2, template, cv2.TM_CCOEFF_NORMED)
#     threshold = 0.7
#     loc = np.where(res >= threshold)
#
#     # detect connected components
#     _, labels = cv2.connectedComponents(np.uint8(res >= threshold))
#
#     for label in range(1, np.max(labels) + 1):
#         loc = np.where(labels == label)
#         top_left = (np.min(loc[1]), np.min(loc[0]))
#         right_bottom = (np.max(loc[1]) + w, np.max(loc[0]) + h)
#
#         # show the image cut by the template
#         image_cut = img2[top_left[1]:right_bottom[1], top_left[0]:right_bottom[0]]
#         cv2.imshow('img', image_cut)
#         # resize image to be larger by 9x
#         dsize = (image_cut.shape[1] * scale, image_cut.shape[0] * scale)
#         output = cv2.resize(image_cut, dsize)
#         cv2.imshow('img', output)
#         # on double click print the coordinates
#         cv2.setMouseCallback('img', print_coordinates2, right_bottom)
#         if cv2.waitKey(0) & 0xff == 27:
#             cv2.destroyAllWindows()

# sort based on x
img1_coords.sort(key=lambda x: x[0])

A = []
for point1, point2 in zip(img1_coords, img2_coords):
    A.append([1, point1[0], point1[1], 0, 0, 0])
    A.append([0, 0, 0, 1, point1[0], point1[1]])
    A.append([1, point2[0], point2[1], 0, 0, 0])
    A.append([0, 0, 0, 1, point2[0], point2[1]])
L = []
for point1, point2 in zip(img1_coords, img2_coords):
    L.append(point1[0])
    L.append(point1[1])
    L.append(point2[0])
    L.append(point2[1])

A = np.array(A)
L = np.array(L)
Xn = np.linalg.lstsq(A, L, rcond=None)[0]
print(Xn)


