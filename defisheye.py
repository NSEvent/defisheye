import sys
import cv2
import numpy as np

# You should replace these 3 lines with the output in calibration step
# DIM=(1922, 1081)
# K=np.array([[714.0734752341677, 0.0, 953.1323254551422], [0.0, 723.9055759320266, 594.4937664229687], [0.0, 0.0, 1.0]])
# D=np.array([[-0.02369904544126501], [0.05711302902082911], [-0.12576024940661643], [0.08817835211303647]])
DIM=(1920, 1080)
K=np.array([[716.5477493748554, 0.0, 955.165561818763], [0.0, 724.2142473355927, 606.3715727996763], [0.0, 0.0, 1.0]])
D=np.array([[-0.018740595050951596], [0.02537719264075746], [-0.03532122209635207], [0.010744030748271913]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
