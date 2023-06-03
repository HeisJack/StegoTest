from PIL import Image, ImageOps

class StegoEmbed():
    message = ""
    with open("messages\\""msg.txt", "r") as f:
        message = f.read()
    print(message)
    # creating a image1 object
    im1 = Image.open("images\\""airplane.png")
    
    # applying grayscale method
    im2 = ImageOps.grayscale(im1)
    im2.show()

    width, height = im2.size
    data = list(im2.getdata())

    # Convert the message to binary
    binary_message = ''.join(format(ord(i), '08b') for i in message)

    # Check if the message can fit in the image
    if len(binary_message) > width * height:
        raise ValueError('Message is too long to fit in the image')
    

if __name__== "__main__":
    StegoEmbed()