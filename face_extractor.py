import json

import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("Video")

faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

def Get_last_index_from_json(filename):
    f = open(filename)
    data = json.load(f)
    f.close()
    if len(data) == 0:
        return 0
    else:
        return len(data)


def Add_to_json(filename,imagename):
    f = open(filename)
    data = json.load(f)
    f.close()
    data.append(imagename)
    data = json.dumps(data)
    with open(filename, "w") as file:
        file.write(data)

def extract_images(name):
    img = cv2.imread(name)

    faces = faceCascade.detectMultiScale(img, 1.1, 4)
    i = 1
    for (x, y, w, h) in faces:
        FaceImg = img[y:y + h, x:x + w]
        print(name.split('.')[0])
        # To save an image on disk
        filename = "faces\\"+name.split('/')[1]+"_face_"+str(i) + '.jpg'
        cv2.imwrite(filename, FaceImg)
        i += 1


img_counter = Get_last_index_from_json("images\\images.json")

while True:
    ret, frame = cam.read()

    faces = faceCascade.detectMultiScale(frame, 1.1, 4)
    i = 1
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Video", frame)

    if cv2.waitKey(20) & 0xFF == 27:
        # ESC pressed
        break
    elif cv2.waitKey(20) & 0xFF == 32:
        # SPACE pressed
        cv2.namedWindow("Image")
        cv2.imshow("Image", frame)
        while True:
            if cv2.waitKey(20) & 0xFF == ord('s'):
                img_name = "images/image_{}.jpg".format(img_counter)
                cv2.imwrite(img_name, frame)
                Add_to_json("images\\images.json","image_{}.jpg".format(img_counter))
                print("{} written!".format(img_name))
                img_counter += 1
                extract_images(img_name)
                cv2.destroyWindow('Image')
                break
            elif cv2.waitKey(20) & 0xFF == ord('c'):
                cv2.destroyWindow('Image')
                break


cam.release()

cv2.destroyAllWindows()




