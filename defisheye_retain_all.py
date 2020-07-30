import sys
import cv2
import numpy as np

import calibrate_config as my_config

def undistort(img_path, balance=1.0, dim2=None, dim3=None):
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort

    assert dim1[0]/dim1[1] == my_config.DIM[0]/my_config.DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = my_config.K * dim1[0] / my_config.DIM[0]  # The values of my_config.K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that my_config.K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final my_config.K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, my_config.D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, my_config.D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite('output.jpg', undistorted_img)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p, balance=1.0)
        # for i in range(11):
        #     undistort(p, balance=i/10)
