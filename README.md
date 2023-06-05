# StegoTest

I'll do my best to cover all the bases:

1. You donn't have to, but i would recommend pre-emptively creating directories titled:
    "messages"
    "extracted_messages"
    "stego"
    "pcaps"
    "excel"
  In the root dir for this project. Depending on where you're checking this out to, the
  processes may or may not have permissions to create those dirs on your behalf
  
2. Create a "certs" directory. Then generate a cert.pem and key.pem via OPENSSL and store them there

3. Make sure all of the dependencies are installed. See requirements.txt. Either install them individually yourself or
   "pip install requirements.txt"
   
4. Now youre ready to begin. First go in msgGenerator.py and change the path at the top of the file. Apparently i was dumb and hard-coded it. Then:
   "python msgGenerator.py"
   This will generate 50 random messages in /messages
5. Then, run:
   "python stego.py"
6. Then start either an http or https python server (make sure to modify IP addresses in server.py, httpserver.py, RequestStuff.py, and httpRequetor.py) I have the
   destination IPs set to localhost by default.
   "python httpServer.py"  or "python server.py"
   If you use httpServer.py use httpRequestor.py in the next step. If you used server.py, use "RequestStuff.py" in the next step
7. For example say you used httpServer.py in your last step, for this step run:
   "python httpRequestor.py --mode stego"
   See file for args requirements
   
8. Be sure to capture PCAPs with Wireshark while running httpRequestor.py

9. ONce you have PCAPs, you can use them to run the analyze.py script
   See args requirements in analyze.py
