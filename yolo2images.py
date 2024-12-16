import cv2
import numpy as np
import argparse

# Args
# EX: python3 yolo2images-fill.py --txt="./test/coco128.txt"  --img="./test/coco128.jpg"
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--txt')
parser.add_argument('--img')
parser.add_argument('--output', default='savedImage.jpg')
args = parser.parse_args()

ptxt = args.txt
pimg = args.img
pout = args.output

'''
Read txt annotation files and original images
'''

def read_txt_labels(txt_file):
    """
    Read labels from txt annotation file
    :param txt_file: txt annotation file path
    :return: tag list
    """
    with open(txt_file, "r") as f:
        labels = []
        for line in f.readlines():
            label_data = line.strip().split(" ")
            class_id = int(label_data[0])
            # Parsing bounding box coordinates
            coordinates = [float(x) for x in label_data[1:]]
            labels.append([class_id, coordinates])
    return labels

def draw_labels(image, labels):
    """
    Draw segmentation region outlines on the image
    :param image: image
    :param labels: list of labels
    """
    for label in labels:
        class_id, coordinates = label
        # Convert coordinates to integers and reshape into polygons
        points = [(int(x * image.shape[1]), int(y * image.shape[0])) for x, y in zip(coordinates[::2], coordinates[1::2])]
        # Draw outlines using polygons
        cv2.polylines(image, [np.array(points)], True, (0, 255, 0), 2) # Red indicates the segmentation area outline


def main():
    """
    Restore the YOLO semantic segmentation txt annotation file to the original image
    """
    # Reading an Image
    # image = cv2.imread("./test/coco128.jpg")
    image = cv2.imread(pimg)
    height, width, _  = image.shape
    # Read txt annotation file
    # txt_file = "./test/coco128.txt"
    txt_file = ptxt
    labels = read_txt_labels(txt_file)
    # Draw segmentation area
    draw_labels(image, labels)
    # Get the window size
    window_size = (width//2, height//2) # You can resize the window as needed
    # Resize an image
    image = cv2.resize(image, window_size)
    # Create a black image the same size as the window
    background = np.zeros((window_size[1], window_size[0], 3), np.uint8)
    # Place the image in the center of the black background
    image_x = int((window_size[0] - image.shape[1]) / 2)
    image_y = int((window_size[1] - image.shape[0]) / 2)
    background[image_y:image_y + image.shape[0], image_x:image_x + image.shape[1]] = image
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # Filename
    # filename = 'savedImage.jpg'args.output
    filename = args.output

    # Using cv2.imwrite() method
    # Saving the image
    cv2.imwrite(filename, image)
if __name__ == "__main__":
    main()
