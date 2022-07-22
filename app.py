from rembg import remove
import gradio as gr
from PIL import Image
from zipfile import ZipFile
import os

def crop_and_resize(img, size, proportion):
    frac = proportion

    left = img.size[0]*((1-frac)/2)
    upper = img.size[1]*((1-frac)/2)
    right = img.size[0]-((1-frac)/2)*img.size[0]
    bottom = img.size[1]-((1-frac)/2)*img.size[1]

    cropped_img = img.crop((left, upper, right, bottom))

    newsize = (size, size)
    cropped_img = cropped_img.resize(newsize)
    return cropped_img


def remove_bg(folder, size, proportion):

    if os.path.exists("images_no_bg.zip"):
        os.remove("images_no_bg.zip")
    else:
        print("The file does not exist")

    with ZipFile("images_no_bg.zip", "w") as zipObj:

        for i, file in enumerate(folder):

            image = Image.open(file)
            image = remove(image)

            image = crop_and_resize(image, size, proportion)

            image_name = f"image_{i}.png"
            image.save(image_name)
            zipObj.write(image_name, image_name)
            os.remove(image_name)

    return "images_no_bg.zip"


interface = gr.Interface(
    title = "Batch Image Background Remover",
    description = "Select a folder with images. Then, select the size of output image (square), and the cropping proportion.",
    allow_flagging="never",
    fn = remove_bg, 
    inputs = [
        gr.File(file_count="directory"),
        gr.Slider(400, 800, step = 100, value=600, label = "Size (Square)"),
        gr.Slider(0, 1, value=.7, step = .1, label = "Croping Proportion", precision = None),
    ],
    outputs = "file"
)

interface.launch(share = False)