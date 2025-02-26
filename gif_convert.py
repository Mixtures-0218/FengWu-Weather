from PIL import Image
import os


def gif(image_path):
    image_folder = image_path  # Path to the folder containing the images
    images = []

    # Load the images into a list
    for filename in sorted(os.listdir(image_folder)):  # Sorting to keep order
        if filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            images.append(Image.open(image_path))

    # Create GIF
    output_gif = "output_animation.gif"
    images[0].save(output_gif, save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)


gif(os.path.join(os.path.join(os.getcwd(), "t2m_output"),)) # Please change the file name for different output