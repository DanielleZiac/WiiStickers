from PIL import Image

def layer_images(images, output_path):
    # Open the first image as the base layer
    base_image = Image.open(images[0])

    # Loop through the remaining images and paste them on top of the base image
    for img_path in images[1:]:
        layer = Image.open(img_path)
        base_image.paste(layer, (0, 0), layer)

    # Convert to RGB mode if the image is in RGBA mode
    if base_image.mode == 'RGBA':
        base_image = base_image.convert('RGB')

    # Save the final result
    base_image.save(output_path)

if __name__ == "__main__":
    # Replace these paths with the paths to your input images
    image_paths = ["gui/avatar/boy.png", "gui/avatar/polo.png", "gui/avatar/eyesopened.png", "gui/avatar/mouthopened.png"]

    # Replace this path with the desired output path
    output_path = "outputs/avatar.jpg"

    layer_images(image_paths, output_path)
