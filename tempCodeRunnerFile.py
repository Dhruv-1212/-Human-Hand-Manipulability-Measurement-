thread1 = threading.Thread(target=game_start).start()
if(calibration==True):
    thread2 = threading.Thread(target=hand_detector.detect_hand()).start()