# from fastapi import FastAPI,WebSocket
# app = FastAPI()


# @app.websocket("/ws")
# async def test(websocket:WebSocket):
#     print("Accepting connection")
#     await websocket.accept()
#     print("Websocket accepted")
#     while True:
#         try:
#             data = await websocket.receive_text()
#             websocket.send("hollow")
#             print(data)
#         except:
#             pass
#             break