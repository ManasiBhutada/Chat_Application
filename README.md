# Chat_Application
Implemented a client-server chat application in Python over UDP.
When started, the server should listen on a UDP port specified as an argument to the program (-sp port). When started, a client sends a SIGN-IN message to the server including a USERNAME. The IP address and port of the server should be given as arguments to the client program (-sip server-ip -sp port). 
On receiving the SIGN-IN message from a client, the server will record important information about the client for enabling future communications between multiple clients (e.g., username, IP address, port).
On executing the send command, the client should first retrieve the IP address and port of the destination USERNAME and use this information to directly send the message to the desired destination. 
