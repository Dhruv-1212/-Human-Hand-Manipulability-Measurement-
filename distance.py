from Camera_init import *
from camera_inp import dc
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

##code for finding the seting the coordinates of the screen
var=False
def dist_status():
    global var
    return var
def take_dist(coordinates_calc, coordinates_game ):
    #coordinates calc is for training the model it have some intermedaite points
    #coordinates_game is the coordin of the vertieces of the play area
    min_x=min(coordinates_game[0][0], coordinates_game[1][0], coordinates_game[2][0], coordinates_game[3][0])
    max_x = max(coordinates_game[0][0], coordinates_game[1][0], coordinates_game[2][0], coordinates_game[3][0])
    min_y=min(coordinates_game[0][1], coordinates_game[1][1], coordinates_game[2][1], coordinates_game[3][1])
    max_y = max(coordinates_game[0][1], coordinates_game[1][1], coordinates_game[2][1], coordinates_game[3][1])
  
    columns = [str(i) for i in range(1, max_x+1)]
 
    arr = np.zeros((max_x+2, max_y+2))
    model = LinearRegression()
    X=[]
    y=[]
    #
    print(len(coordinates_calc))
    for i in range(len(coordinates_calc)):
        X.append(coordinates_calc[i])
        print(i,"diatance depth")
        ret, depth_frame, depth_img, color_frame = dc.get_frame()
        distance = depth_img[coordinates_calc[i][1], coordinates_calc[i][0]]
        print(distance)
        y.append(distance)
    X_arr=np.array(X)
    y_arr=np.array(y)
    print("data input done")
    model.fit(X_arr, y_arr)
    predict=[]
    print("model firt done")
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
           predict.append([x,y])
    predict_point=np.array(predict)
    predict_z=model.predict(predict_point)
    print("model prediction done")
    df_predicted = pd.DataFrame({'x': predict_point[:, 0], 'y': predict_point[:, 1], 'z': predict_z})
  
    df_predicted.to_csv('mydata.csv', index=False, float_format='%.0f')
    global var
    var=True
    print("file created")
    # cv2.destroyWindow('color_frame')
    # cv2.destroyWindow('depth_frame')




