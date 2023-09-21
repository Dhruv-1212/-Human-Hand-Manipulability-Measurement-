from Camera_init import *
from camera_inp import dc
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


var=False
def dist_status():
    global var
    return var
def take_dist(coordinates_calc, coordinates_game ):
    min_x=min(coordinates_game[0][0], coordinates_game[1][0], coordinates_game[2][0], coordinates_game[3][0])
    max_x = max(coordinates_game[0][0], coordinates_game[1][0], coordinates_game[2][0], coordinates_game[3][0])
    min_y=min(coordinates_game[0][1], coordinates_game[1][1], coordinates_game[2][1], coordinates_game[3][1])
    max_y = max(coordinates_game[0][1], coordinates_game[1][1], coordinates_game[2][1], coordinates_game[3][1])
  
    columns = [str(i) for i in range(1, max_x+1)]
 
    arr = np.zeros((max_x+2, max_y+2))
    model = LinearRegression()
    X=[]
    y=[]
    for i in range(len(coordinates_calc)):
        X.append(coordinates_calc[i])
        ret, depth_frame, depth_img, color_frame = dc.get_frame()
        distance = depth_img[coordinates_calc[i][1], coordinates_calc[i][0]]
        y.append(distance)
    X_arr=np.array(X)
    y_arr=np.array(y)
    model.fit(X_arr, y_arr)
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            z = model.predict(np.array([[x, y]]))
            arr[x,y]=z
            cv2.circle(color_frame, (coordinates_calc[i][1], coordinates_calc[i][0]), 4, (0, 0, 255), thickness=2)
            cv2.imshow("depth_frame", depth_frame)
            cv2.imshow("color_frame", color_frame)
            key = cv2.waitKey(1)
            if key == 110:
                break

    df = pd.DataFrame(arr, columns)
    df.to_csv('mydata.csv', index=False, float_format='%.0f')
    global var
    var=True
    cv2.destroyWindow('color_frame')
    cv2.destroyWindow('depth_frame')




