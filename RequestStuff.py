import requests
import time
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, required=True)
args = parser.parse_args()
print('mode:', args.mode)

# localhost for testing purposes
tls_url = 'https://127.0.0.1:4443/images/'
stego_url = 'https://127.0.0.1:4443/stego/'

start_time = time.time()
while True:
    response = requests.get(tls_url, verify=False)
    # Do something with the response here
    random_integer = random.randint(1, 5)
    time.sleep(random_integer)

    elapsed_time = time.time() - start_time
    if elapsed_time > 120:
        break