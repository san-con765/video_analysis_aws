# ~/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/CapstoneProject/GIT/Video Analysis/video_analysis_aws/.conda
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
def create_gif(inputImagesPath, output_path, durationGif = 500):
    print("Run Process create_gif")
    print("Items provided are")
    for i in range(0, len(inputImagesPath)):
        print(inputImagesPath[i])
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
    # output_path = 
    print("Gif failure point 3")
    try:
        # images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
        images[0].save(output_path, save_all=True, append_images=images[1:], duration=durationGif, loop=0)
        print("Gif Created")
    except Exception as e:
            print(f"Failed to Save gif {output_path}: {e}")
            
    
    return "/home/ec2-user/video_analysis_aws/output.gif"
    # print(f"Image {path} not found.")

######################################################
# # Create gif based on images parsed
# NOT WORKING
# def create_gif(analysis_array, duration=500):
#     print("Run Process create_gif")
#     pil_images = []

#     # Assuming that analysis_array contains up to three elements, each with an image at index 0
#     for data in analysis_array[:3]:  # Only take the first three images
#         image = data[0]  # Assuming the image is the first item in each sub-array
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
#         pil_image = Image.fromarray(image_rgb)
#         pil_images.append(pil_image)

#     # Create the GIF in memory
#     with io.BytesIO() as byte_stream:
#         if pil_images:
#             pil_images[0].save(byte_stream, format='GIF', save_all=True, append_images=pil_images[1:], optimize=False, duration=duration, loop=0)
#             gif_data = byte_stream.getvalue()  # Get GIF byte data
#             return gif_data
#         else:
#             print("No images were processed. GIF not created.")
#             return None

# # Example usage within your existing code:
# # Assuming `AnalysisArray` is the result from `AnalysePose()`
# # images_gif_bytes = create_gif_from_analysis(AnalysisArray)
# # You can now handle `images_gif_bytes` as needed, such as sending over a network, displaying in a GUI, etc.



######################################################
# #Testing
# # List of image paths
# path = "/Users/seanryan/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/Local ActiveAging/VideoAnalysis/Example_output/"
# image1_path = path+'1 max_frame.jpg'
# image2_path = path+'1 min_frame.jpg'
# image3_path = path+'2 max_frame.jpg'

# image_paths = [image1_path, image2_path, image3_path]

# # Output path for the GIF
# output_gif_path = path+'output.gif'

# # Duration of each frame in the GIF (in milliseconds)
# frame_duration = 500

# create_gif(image_paths, output_gif_path, frame_duration)


# def create_gif(inputImagesPath, duration = 500):
#     print("Run Process create_gif")
#     print("Items provided are")
#     for i in range(0, len(inputImagesPath)):
#         print(inputImagesPath[i])
#     images = []
#     print("Gif failure point 1")
    
#     for path in inputImagesPath:
#         try:
#             img = Image.open(path).convert('RGB')
#             images.append(img)
#             print(f"Loaded {path}")

#         except Exception as e:
#             print(f"Failed to open {path}: {e}")
    
#     # for path in inputImagesPath:
#     #     images.append(Image.open(path))
#     #             # Confirm correct syntax to return
#     print("Gif failure point 2")
#     # print(f"GIF saved successfully at {output_path}")
#     output_path = "/Users/seanryan/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/Local ActiveAging/VideoAnalysis/output_frames/output.gif"
#     print("Gif failure point 3")
#     images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
#     print("Gif Created")
#     return "/home/ec2-user/video_analysis_aws/output.gif"
#     # print(f"Image {path} not found.")

# image_1 = "/Users/seanryan/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/Local ActiveAging/VideoAnalysis/output_frames/0 max_frame.jpg"
# image_2 = "/Users/seanryan/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/Local ActiveAging/VideoAnalysis/output_frames/1 max_frame.jpg"
# image_3 = "/Users/seanryan/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/Local ActiveAging/VideoAnalysis/output_frames/1 min_frame.jpg"

# imageInput = [image_1, image_2, image_3]

# create_gif(imageInput)