from PIL import Image, ImageOps
import os

class StegoEmbed():

    images = ["images\\airplane.png", 
              "images\\arctichare.png", 
              "images\\baboon.png", 
              "images\\airplane.png", 
              "images\\watch.png"]
    
    extraction = True
    
    # Iterates over the messages directory. Performs the embed function
    # for each message using one of 5 possible cover objects. The user
    # should provide the FULL messages path
    def embedLoop(self, path):
        imagesIndex = 0
        # For each .txt file in messages dir
        files = os.listdir(path)
        for i in range(len(files)):
            fileName = "messages\\" + "msg" + str(i) + ".txt"
            self.embed(fileName, self.images[imagesIndex], i)
            if imagesIndex == 4:
                imagesIndex = 0
            else:
                imagesIndex += 1
            


    def embed(self, messagePath, image, messagesIndex):
        message = ""
        with open(messagePath, "r") as f:
            message = f.read()

        # Append a null character to the end of the message
        message += '\x00'

        # creating a image1 object
        im1 = Image.open(image)
        
        # applying grayscale method
        im2 = ImageOps.grayscale(im1)

        width, height = im2.size
        data = list(im2.getdata())

        # Convert the message to binary
        binary_message = ''.join(format(ord(i), '08b') for i in message)

        # Check if the message can fit in the image
        if len(binary_message) > width * height:
            raise ValueError('Message is too long to fit in the image')
        
        # Hide the message in the least significant bits of the pixel values
        index = 0
        for i in range(len(data)):
            if index < len(binary_message):
                # Change the least significant bit to the next bit of the message
                data[i] = data[i] & ~1 | int(binary_message[index])
                index += 1

        # Save the modified image
        stego_image = Image.new('L', (width, height))
        stego_image.putdata(data)
        stego_image.save('stego\stego' + str(messagesIndex) + "." + image[-3:])

    def extract_loop(self, path):
        # For each stego image in stego dir
        files = os.listdir(path)
        for i in range(len(files)):
            subString = "stego" + str(i) + "."
            for fileName in os.listdir(path):
                if subString in fileName:
                    subString = subString  + fileName[-3:]
            fileName = "stego\\" + subString
            self.extract_message(fileName, i)

    def extract_message(self, image_path, index):
        extractDirectory = "extracted_messages\\"

        # Open the image and convert it to grayscale
        image = Image.open(image_path).convert('L')
        data = list(image.getdata())

       # Extract the least significant bits of each pixel value
        binary_message = ''
        for i in range(len(data)):
            binary_message += str(data[i] & 1)
            if len(binary_message) % 8 == 0 and binary_message[-8:] == '00000000':
                break

        # Group the bits into bytes
        binary_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]

        # Convert the binary message to a string
        message = ''.join(chr(int(b, 2)) for b in binary_message)

        fileName = extractDirectory + "ex_message" + str(index) + ".txt"
        with open(fileName, 'w', encoding="utf-8") as fout:
            fout.write(message)

        self.extraction = self.compare_files(fileName, "C:\Projects\StegoTest\messages\\" + "msg" + str(index) + ".txt")
        

    
    # Compares two file objects. If the last char is a null char, it
    # ignores it
    def compare_files(self, file1, file2):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            contents1 = f1.read()
            contents2 = f2.read()
            # Ignore the last character if it is a null character
            if contents1 and contents1[-1] == '\x00':
                contents1 = contents1[:-1]
            if contents2 and contents2[-1] == '\x00':
                contents2 = contents2[:-1]
            
            if not contents1 == contents2:
                raise ValueError('my_variable is False')
            else:
                return contents1 == contents2

if __name__== "__main__":
    messagesPath = "C:\Projects\StegoTest\messages"
    stegoPath = "C:\Projects\StegoTest\stego"
    stegoObject = StegoEmbed()
    stegoObject.embedLoop(messagesPath)
    stegoObject.extract_loop(stegoPath)
    