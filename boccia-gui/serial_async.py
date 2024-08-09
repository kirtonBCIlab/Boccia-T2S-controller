import asyncio
import aioserial
async def read_from_serial(aioserial_instance):
    while True:
        data = await aioserial_instance.read_async()
        print(data.decode(errors='ignore'), end='', flush=True)
async def main():
    #aioserial_instance = aioserial.AioSerial(port='COM3', baudrate=9600)
    await read_from_serial(aioserial_instance)
if __name__ == "__main__":
    asyncio.run(main())