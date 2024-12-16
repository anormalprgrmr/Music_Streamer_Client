import websocket
import os

# Define the WebSocket URL and the file paths
websocket_url = "ws://localhost:3000/upload"
file_to_upload = "ss.mp3"  # Path to the file you want to upload

# Function to download a file from the server
def download_file():
    output_file = 'ss.mp3'
    try:
        # Connect to the WebSocket server
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:3000/download")
        print("Connected to the WebSocket server")

        while True:
            try:
                message = ws.recv()  # Receive message from the server
                if isinstance(message,str):
                    print(message)
                if not message:
                    break
                # If the message is 'end', the file transfer is complete
                if message == 'end':
                    print('File transfer finished.')
                    break

                # Save the received file chunk
                with open(output_file, 'ab') as f:
                    f.write(message)
                    print(message)
                    print(f"Received {len(message)} bytes")

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    except Exception as e:
        print(f"Error connecting to WebSocket server: {e}")

    finally:
        ws.close()
        print("WebSocket connection closed.")

# Function to upload a file to the server
def upload_file():
    try:
        # Connect to the WebSocket server for uploading
        ws = websocket.WebSocket()
        ws.connect(websocket_url)
        print("Connected to the WebSocket server for upload")

        # Open the file to be uploaded
        with open(file_to_upload, 'rb') as f:
            # Read the file in chunks and send each chunk
            chunk_size = 1024  # Adjust chunk size as necessary
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break  # Stop when we've read the entire file
                ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)  # Send as binary

                # Optionally, print progress or feedback
                print(f"Sent {len(chunk)} bytes")

        # Send a signal to indicate the upload is complete
        ws.send("end")
        print("File upload completed.")

    except Exception as e:
        print(f"Error uploading file: {e}")
    
    finally:
        ws.close()
        print("WebSocket connection closed after upload.")

# Main function to control the client actions
if __name__ == "__main__":
    # Uncomment the action you want to perform:
    # Download file
    # download_file()

    # Upload file
    upload_file()
    # pass