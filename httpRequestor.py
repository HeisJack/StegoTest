import requests
import time
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, required=True)
args = parser.parse_args()
print('mode:', args.mode)

# localhost for testing purposes
tls_url = 'http://127.0.0.1:80/images/'
stego_url = 'http://127.0.0.1:80/stego/'
messages_url = 'http://127.0.0.1:80/messages/'

start_time = time.time()
while True:
    if(args.mode == "tls"):
        response = requests.get(tls_url)
    elif(args.mode == "stego"):
        response = requests.get(stego_url)
    elif(args.mode == "messages"):
        response = requests.get(messages_url)

    print(response)
    # Do something with the response here
    random_integer = random.randint(1, 5)
    time.sleep(random_integer)

    elapsed_time = time.time() - start_time
    if elapsed_time > 300:
        break