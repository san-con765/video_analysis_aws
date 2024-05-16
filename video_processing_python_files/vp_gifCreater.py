from PIL import Image
import cv2
import os
import io
 
 
######################################################
# Local Writing
# def create_gif(image_paths, output_path, duration = 500):
#     images = []
#     for path in image_paths:
#         # Ensure the image exists
#         if os.path.exists(path):
#             # Open the image and append to the list
#             images.append(Image.open(path))
#         else:
#             print(f"Image {path} not found.")
#             return
 
#     # Save the images as a GIF
#     images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
#     print(f"GIF saved successfully at {output_path}")
 
 
######################################################
# Create gif based on image paths
def create_gif(inputImagesPath, duration = 500):
    print("Run Process create_gif")
    

    # for i in range(0, len(inputImagesPath)):
    #     print(inputImagesPath[i])
        
    images = []
    print("Gif failure point 1")
    
    for path in inputImagesPath:
        try:
            img = Image.open(path).convert('RGB')
            images.append(img)
            print(f"Loaded {path}")
        except Exception as e:
            print(f"Failed to open {path}: {e}")
    
    
    # for path in inputImagesPath:
    #     images.append(Image.open(path))
    #             # Confirm correct syntax to return
    print("Gif failure point 2")
    # print(f"GIF saved successfully at {output_path}")
    output_path = "/home/ec2-user/video_analysis_aws/output.gif"
    print("Gif failure point 3")
    images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
    print("Gif Created")
    return "/home/ec2-user/video_analysis_aws/output.gif"
    # print(f"Image {path} not found.")
 