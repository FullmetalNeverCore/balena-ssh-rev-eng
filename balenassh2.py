import asyncio
import json
import requests
import websockets
import random 
import string



def random_terminal_id():
    return 'P1'+''.join(random.choice(string.ascii_letters) for _ in range(5))

def get_url_string():
    id = random_terminal_id()
    print(id)
    return f'https://terminal.balena-devices.com/socket.io/?EIO=4&transport=polling&t={id}'

# Function to get initial connection and obtain sid
def get_initial_connection(url):
    url = url
    response = requests.get(url)
    print(f"Initial GET Request Status Code: {response.status_code}")
    print(f"Initial GET Response: {response.text}")
    
    initial_data = response.text
    sid = json.loads(initial_data[1:])["sid"]
    return sid

def sendStrangeRequest(url):
    url = url 
    response = requests.get(url)
    print(f"Strange GET Request Status Code: {response.status_code}")
    print(f"Strange Request Content : {response.text}")

def secondStrangeRequest(url,content):
    url = url
    response = requests.post(url,data=content)
    print(f"Strange POST Request Status Code: {response.status_code}")
    print(f"Sended content {content}")
    print(f"Strange Request Content : {response.text}")



async def connect_to_websocket(uri):
    async with websockets.connect(uri) as websocket:
        cmd = list("ping")
        print(f"Connected to WebSocket server at {uri}")
        
        async def send_message(message):
            await websocket.send(message)
            print(f"> Sent message: {message}")

        async def receive_message():
            message = await websocket.recv()
            print(f"< Received: {message}")
            return message
        
        # while True:
        #     user_input = input()
        #     if user_input.lower() == 'exit':
        #         break

        #string format
        SESSION_ID = 1
        DEVICE_UID = 1

        await send_message(f"5") #vital part
        await send_message(f'42["authentication",{{"token":"{SESSION_ID}","uuid":"{DEVICE_UID}","target":{{"hostos":true}}}}]')
        await receive_message()
        await receive_message()
        await receive_message()
        await send_message(f'42["ssh connect",null]')
        await receive_message()
        await receive_message()
        await receive_message()
        await receive_message()
        await receive_message()
        await receive_message()
        await receive_message()
        await send_message(f'42["data","pwd"]')
        await receive_message()
        await send_message('42["data","\\r"]')
        await receive_message()

        await websocket.close()
        print("WebSocket connection closed")

# Main function to run the process
async def main():
    sid = get_initial_connection(get_url_string()) #vital part1
    websocket_url = f'wss://terminal.balena-devices.com/socket.io/?EIO=4&transport=websocket&sid={sid}' 
    print(sid)
    secondStrangeRequest(f'{get_url_string()}&sid={sid}',"40") #vital part2
    await connect_to_websocket(websocket_url) #websocket connection


if __name__ == "__main__":
    asyncio.run(main())
