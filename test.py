import cv2
import time
import numpy as np

cap = cv2.VideoCapture(1)
frame_count = 0
start_time = time.time()
while cap.isOpened():
    isTrue, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    dimension = (image.shape)
    amount = 6
    height = 100
    y_start = 50
    alpha = 0.6
    currentBox = -1

    overlay = image.copy()
    
    #FPS Anzeige
    fps = 'FPS: {:.2f}'.format(frame_count / (time.time() - start_time))
    position = (5, 25)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0)  # Grün (BGR-Format)
    thickness = 1
    cv2.putText(image, fps, position, font, font_scale, color, thickness)
    frame_count += 1


    #show frame
    cv2.imshow("Video", image)



    # Warten auf eine Taste zum Schließen des Fensters
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()