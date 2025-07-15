# C2-Server
Purpose: Create a server in order to await for client's connection. Adding stealth mechanism, in order to hide the packet.
# How does it work:
When running the client in /Linux file, it will use socket module, to connect back to the C2 server IP Adress and Port. 
# How to run it?
# For C2-Server
``` bash
git clone https://github.com/phuc223/C2-Server/
cd C2-Server
python3 server.py -h
```
# For Client
``` bash
git clone https://github.com/phuc223/C2-Server/
cd C2-Server
cd Linux
./client <ip> <port>
```
# If you want to rebuild you can just use "$ make clean" and "$ make"
# The C2 Server currently cannot use the --secure module properly, I will add more to the client later.
