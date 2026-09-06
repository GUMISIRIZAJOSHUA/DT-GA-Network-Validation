import socket
import json
import time


HOST = "127.0.0.1"
PORT = 5000


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)


server.bind(
    (HOST, PORT)
)


server.listen(5)


print("Server waiting...")


while True:

    conn, addr = server.accept()

    print("Connected:", addr)


    try:

        data = conn.recv(4096)


        if data:

            msg = json.loads(
                data.decode()
            )


            response = {

                "seq": msg["seq"],

                "ack": True,

                "server_time": time.time()

            }


            conn.send(
                json.dumps(response).encode()
            )


    except Exception as e:

        print("Error:", e)


    finally:

        conn.close()
