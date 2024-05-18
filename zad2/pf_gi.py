import cv2
import numpy as np
import itertools

print(cv2.__version__)

# read black and white image
img = cv2.imread(r'7ac599_56eff02023de4662aaff896e0d87553d~mv2.webp')
# print(img)

# cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('image', img)
# k = cv2.waitKey(0)
# if k == 27:  # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('z'):
#     cv2.imwrite('g.png', img)
imgRGB = cv2.imread(r'7ac599_56eff02023de4662aaff896e0d87553d~mv2.webp')
row, col, channel = imgRGB.shape

# row, col = img.shape

print(f"Img RGB shape: {imgRGB.shape}")
print(f"Img shape: {img.shape}")

# # now set pixels from 100, 200 to 300, 800 to white
# img[100:300, 200:800] = 255
# # now for an image with 3 channels
# imgRGB[100:300, 200:800, 0] = 255
# imgRGB[100:300, 200:800, 1] = 255
# imgRGB[100:300, 200:800, 2] = 255

# cv2.imshow('image', img)
# k = cv2.waitKey(0)
# if k == 27:  # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('z'):
#     cv2.imwrite('g.png', img)
#
# cv2.imshow('image', imgRGB)
# k = cv2.waitKey(0)
# if k == 27:  # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('z'):
#     cv2.imwrite('g.png', imgRGB)

# b, g, r = cv2.split(imgRGB)
# def show_image(b, g, r):
#     imgRGB = cv2.merge((b, g, r))
#     cv2.imshow('image', imgRGB)
#     k = cv2.waitKey(0)
#     if k == 27:  # wait for ESC key to exit
#         cv2.destroyAllWindows()
#     elif k == ord('z'):
#         cv2.imwrite('g.png', imgRGB)
#
# # iterate over all permutations of b, g, r
# for i, perm in enumerate(itertools.permutations([b, g, r])):
#     show_image(*perm)

# # now show the image grayscale but reverse black and white
# img = cv2.bitwise_not(img)
# cv2.imshow('image', img)

# imgRGB[0:w, 0:k,:]
# new_img = cv2.addWeighted(imgRGB[0:row, 0:col, :], 0.5, img[0:row, 0:col, :], 0.5, 0)
# cv2.imshow('image', new_img)
#
# cv2.setMouseCallback('image', draw_circle)
# k = cv2.waitKey(0)
# if k == 27:  # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('z'):
#     cv2.imwrite('g.png', new_img)
#     cv2.destroyAllWindows()

# img = np.zeros((512, 512, 3), np.uint8)

# cv2 window with a zoom param

# global img_zoom
def zooms(images=[], add_img=None, zoom=True, x=0, y=0, extents=[], ret_xy_pos=False):
    if ret_xy_pos:
        # walk through extents and return the x, y coordinates on the first image
        x_ret = 0
        y_ret = 0
        for extent in extents:
            x_ret += extent[0]
            y_ret += extent[1]
        x_ret += x
        y_ret += y
        return x_ret, y_ret
    if add_img is not None:
        images.append(img)
        extents.append((0, 0, img.shape[1], img.shape[0]))
    if zoom:
        # zoom into the images[-1]
        last_img = images[-1]
        shape = last_img.shape

        # cut image in half around the x, y coordinates
        x_start = max(x - shape[0] // 4, 0)
        x_end = min(x + shape[0] // 4, shape[0])
        y_start = max(y - shape[1] // 4, 0)
        y_end = min(y + shape[1] // 4, shape[1])
        # check if x_start == x_end or y_start == y_end
        if x_start > x_end:
            x_start, x_end = x_end, x_start
        if y_start > y_end:
            y_start, y_end = y_end, y_start
        if x_start == 0:
            x_end = shape[0] // 2
        if y_start == 0:
            y_end = shape[1] // 2
        if x_end == shape[0]:
            x_start = max(x_end - shape[0] // 2, 0)
            x_start = min(x_start, x)
        if y_end == shape[1]:
            y_start = max(y_end - shape[1] // 2, 0)
            y_start = min(y_start, y)
        img_zoom = last_img[y_start:y_end, x_start:x_end]
        if x_start == x_end:
            img_zoom = last_img[y_start:y_end, x_start:]
        if y_start == y_end:
            img_zoom = last_img[y_start:, x_start:x_end]
        if x_start == x_end and y_start == y_end:
            return last_img


        images.append(img_zoom)
        extents.append((x_start, y_start, x_end, y_end))
        return images[-1]
    else:
        # zoom out to the images[-2]
        if len(images) > 1:
            images.pop()
            return images[-1]
        elif len(images) == 1:
            return images[-1]
        else:
            return None

zooms(add_img=imgRGB)

def print_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(zooms(ret_xy_pos=True, x=x, y=y))
    #scroll
    elif event == cv2.EVENT_MBUTTONDOWN:
        img_zoom = zooms(zoom=True, x=x, y=y)
        cv2.destroyAllWindows()
        cv2.namedWindow('zoom')
        cv2.setMouseCallback('zoom', print_coordinates)
        cv2.imshow(f'zoom', img_zoom)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
        elif k == ord('z'):
            cv2.imwrite('g.png', img_zoom)
            cv2.destroyAllWindows()
    elif event == cv2.EVENT_RBUTTONDOWN:
        # zoom out
        img_zoom = zooms(zoom=False)
        cv2.destroyAllWindows()
        cv2.namedWindow('zoom')
        cv2.setMouseCallback('zoom', print_coordinates)
        cv2.imshow(f'zoom', img_zoom)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
        elif k == ord('z'):
            cv2.imwrite('g.png', img_zoom)
            cv2.destroyAllWindows()


cv2.namedWindow('image')
cv2.setMouseCallback('image', print_coordinates)

cv2.imshow('image', img)
while True:
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

