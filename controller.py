import requests
import websocket
import os

# Define the WebSocket URL and the file paths
websocket_url = "ws://localhost:3000/upload"
# file_to_upload = "ss.mp3"  # Path to the file you want to upload

# Function to download a file from the server
def download_file(id):
    output_file = 'ss.mp3'
    try:
        # Connect to the WebSocket server
        ws = websocket.WebSocket()
        ws.connect(f"ws://localhost:3000/download/{id}")
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
def upload_file(file_to_upload):
    try:
        # Connect to the WebSocket server for uploading
        ws = websocket.WebSocket()
        ws.connect(websocket_url)
        print("Connected to the WebSocket server for upload")
        file_name = os.path.basename(file_to_upload)
        ws.send('file')

        ws.send(file_name)
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

def get_songs():

    # Sending the GET request
    response = requests.get('http://localhost:3000/getSongs')

    if response.status_code == 200:
        print('Response JSON:', response.json())  # Parse JSON response
    else:
        print('Error:', response.status_code, response.text)

def login(username,password):
    url = 'http://localhost:3000/login'

    # JSON data to be sent in the body of the POST request
    json_data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, json=json_data)

    # Checking the response
    if response.status_code == 200:
        print('Success!')
        result = response.json()
        print('Response JSON:', response.json())
        if(result['status'] == 'success'):
            return True
    else:
        print('Failed to send POST request')
        print('Status Code:', response.status_code)
        print('Response Text:', response.text)
    return False

def signup(username,password):
    url = 'http://localhost:3000/signup'

    # JSON data to be sent in the body of the POST request
    json_data = {
        'username': username,
        'password': password
    }
    print('json data ', json_data)
    response = requests.post(url,json=json_data)

    # Checking the response
    if response.status_code == 200:
        print('Success!')
        result = response.json()
        print('Response JSON:', response.json())
        if(result['status'] == 'success'):
            return True
    else:
        print('Failed to send POST request')
        print('Status Code:', response.status_code)
        print('Response Text:', response.text)
    return False

# Main function to control the client actions
if __name__ == "__main__":
    
    # Uncomment the action you want to perform:
    # Download file
    # download_file("Koorosh-Vanish-128.mp3")
    # result = signup('ab','12')
    # print(result)
    # Upload file
    # upload_file()
    # get_songs()
    # pass
    result = login('qwesss','12')
    print('resul t ',result)
