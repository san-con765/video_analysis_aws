#Save Image
import os
import cv2
import numpy as np

# def SaveImage(image, filename="first_frame.jpg", directory="/"):
#     print("Run Process SaveImage")
#     if image is not None:
#         # Check if directory exists, create if it doesn't
#         if not os.path.exists(directory):
#             os.makedirs(directory)

#         # Save the image
#         save_path = os.path.join(directory, filename)
#         cv2.imwrite(save_path, image)
#         print(f"Image saved at {save_path}")
#     else:
#         print("No analysis available.")



def SaveImage(image, filename, directory="/home/ec2-user/video_analysis_aws/"):
    print("Run Process SaveImage")
    
    # if isinstance(image, np.ndarray):
    try:
        save_path = os.path.join(directory, filename)
        cv2.imwrite(save_path, image[0])
        print(f"Image saved at {save_path}")
    except:
        print("Provided image is not a valid numpy array.")