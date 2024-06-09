import numpy as np
import cv2

img = cv2.imread('IMG_7052.JPG')

# Show the image, let the user select 8 points and show the next image
p1list = []

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p1list.append([x, y])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        print(f"Point {len(p1list)}: {x}, {y}")

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_click)
# cv2.imshow('image', img)
# show the image scaled down
scale = 0.5
cv2.imshow('image', cv2.resize(img, (0, 0), fx=scale, fy=scale))


while True:
    if len(p1list) == 8 or cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break


img2 = cv2.imread('IMG_7054.JPG')

p2list = []

def mouse_click2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        p2list.append([x, y])
        cv2.circle(img2, (x, y), 5, (0, 0, 255), -1)

cv2.namedWindow('image2')
cv2.setMouseCallback('image2', mouse_click2)
cv2.imshow('image2', cv2.resize(img2, (0, 0), fx=scale, fy=scale))

while True:
    if len(p2list) == 8 or cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

p1 = np.array(p1list).astype(np.float32).reshape(-1, 1, 2)
p2 = np.array(p2list).astype(np.float32).reshape(-1, 1, 2)


fx = fy = f = 4680
cx = img.shape[1] / 2
cy = img.shape[0] / 2
K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])


E, mask = cv2.findEssentialMat(p1, p2, K, method=cv2.RANSAC)

_, R, t, _ = cv2.recoverPose(E, p1, p2, K, mask=mask)
P1 = np.hstack((np.eye(3), np.zeros((3, 1))))
P2 = np.hstack((R, t))

P1 = np.dot(K, P1)
P2 = np.dot(K, P2)

print(f"{P1.shape=}, {P2.shape=}, {p1.shape=}, {p2.shape=}")
print(f"{P1=}, {P2=}, {p1=}, {p2=}")
points3D = cv2.triangulatePoints(P1, P2, p1, p2)
points3D /= points3D[3]

points3D = points3D[:3,:].T

print(f"3D points: {points3D}")

# lewy górny lewego zdjecia


