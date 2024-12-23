import os, sys
import json
import numpy as np
import cv2
from PIL import Image

def lme2mask(input_folder, output_folder):

    if not os.path.exists(input_folder):
        print("No data source.")
        print("沒有數據來源。")
        print("没有数据来源。")
        sys.exit(0)

    print("All Files" , os.listdir(input_folder))

    if not os.path.exists(output_folder + "masks/"):
        os.makedirs(output_folder + "masks/")
    if not os.path.exists(output_folder + "images/"):
        os.makedirs(output_folder + "images/")
    files = []
    jsons = []
    keys = []

    for filename in os.listdir(input_folder):
        if filename.endswith((".json")):
            jsons.append(filename) 
    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg", ".bmp")):
            files.append(filename) 

    if len(files) == len(jsons) :
        print("The number of JSON files is the same as the number of image files.")
        print("JSON 檔案的數量與圖片檔案的數量相同。")
        print("JSON 档案的数量与图片档案的数量相同。")
        for filename in jsons:
            keys.append(filename.split(".")[0])
    else :
        print("The number of JSON files does not match the number of image files, please check.")
        print("JSON 檔案的數量與圖片檔案的數量不一致，請檢查。")
        print("JSON 档案的数量与图片档案的数量不一致，请检查。")
        sys.exit(0)

    points_save = []
    masks_save = []

    for filename in jsons:
        json_path = os.path.join(input_folder, filename)
        print("INFO. JSON Path :", json_path)
        with open(json_path, "r") as f:
            data = f.read()   
        # convert str to json objs
        data = json.loads(data)
        # get the points 
        points = data["shapes"][0]["points"]
        points = np.array(points, dtype=np.int32)   # tips: points location must be int32
        points_save.append(points)

    for filename in files:
        image_path = os.path.join(input_folder, filename)
        # read image to get shape
        image = cv2.imread(image_path)
        # create a blank image
        mask = np.zeros_like(image, dtype=np.uint8)
        masks_save.append(mask)


    for tem in range(len(keys)):
        cv2.fillPoly(masks_save[tem], [points_save[tem]], (255, 255, 255))
        # save the mask 
        output_path = os.path.join(output_folder + "masks/", keys[tem]+".png")
        print("INFO. Output Path :", output_path)
        cv2.imwrite(output_path, masks_save[tem])

    for filename in files:
        image_path = os.path.join(input_folder, filename)
        open_image = Image.open(image_path)
        output_path = os.path.join(output_folder + "images/", filename.replace('.bmp', '.png'))
        open_image.save(output_path, "PNG")

