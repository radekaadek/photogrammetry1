import cv2
import numpy as np

img = cv2.imread('724.tif')
gImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def print_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x // 9 + param[0], y // 9 + param[1])

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
        dsize = (image_cut.shape[1] * 9, image_cut.shape[0] * 9)
        output = cv2.resize(image_cut, dsize)
        cv2.imshow('img', output)
        # on double click print the coordinates
        cv2.setMouseCallback('img', print_coordinates, right_bottom)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()

    # # take minmax locs
    # for location in loc:
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(location)
    #     top_left = max_loc
    #     right_bottom = (top_left[0] + w, top_left[1] + h)
    #
    #     for tl, rb in zip(top_left, right_bottom):
    #         # show the image cut by the template
    #         image_cut = img[tl:rb, tl:rb]
    #         cv2.imshow('img', image_cut)
    #         if cv2.waitKey(0) & 0xff == 27:
    #             cv2.destroyAllWindows()

# show the image reduced by to minumum screen size
# 16:10 1080p
# screen_res = (1920, 1080)
# scale_percent = min(screen_res[0] / img.shape[1], screen_res[1] / img.shape[0]) * 100
#
# width = int(img.shape[1] * scale_percent / 100)
# height = int(img.shape[0] * scale_percent / 100)
#
# # dsize
# dsize = (width, height)
#
# # resize image
# output = cv2.resize(img, dsize)
#
# cv2.imshow('img', output)
# if cv2.waitKey(0) & 0xff == 27:
#   cv2.destroyAllWindows()


