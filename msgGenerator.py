import os
import random
import shutil
import string

#messagesDirectory = "messages\\"""
messagesDirectory = "C:\Projects\StegoTest\messages"

if os.listdir(messagesDirectory):
    for filename in os.listdir(messagesDirectory):
        file_path = os.path.join(messagesDirectory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

#10KB, 15KB, 20KB, 25KB
sizes = [10240, 15360, 20480, 25600]

ascii_chars = string.ascii_letters

for i in range(50):
    randomSize = random.randint(0,3)
    random_string = ''.join(random.choice(ascii_chars) for _ in range(sizes[randomSize]))

    fileName = messagesDirectory + "\\""msg" + str(i) + ".txt"

    with open(fileName, 'w', encoding="utf-8") as fout:
        fout.write(random_string)