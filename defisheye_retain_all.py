import sys
import cv2
import numpy as np

# You should replace these 3 lines with the output in calibration step
# DIM=(1922, 1081)
# K=np.array([[714.0734752341677, 0.0, 953.1323254551422], [0.0, 723.9055759320266, 594.4937664229687], [0.0, 0.0, 1.0]])
# D=np.array([[-0.02369904544126501], [0.05711302902082911], [-0.12576024940661643], [0.08817835211303647]])

DIM=(1920, 1080)
K=np.array([[715.1254125025503, 0.0, 952.3850662898742], [0.0, 723.7772147130605, 595.9377980413541], [0.0, 0.0, 1.0]])
D=np.array([[-0.04134504735594926], [0.1492954041959826], [-0.32110264903514607], [0.239792648774292]])

def undistort(img_path, balance=1.0, dim2=None, dim3=None):
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort

    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    print(new_K)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p, balance=1.0)
        # for i in range(10):
        #     undistort(p, balance=i/10)
