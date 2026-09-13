import grpc

PORT = 50052  # must match server.py

from generated.user_pb2 import UserRequest, ListUsersRequest, ChatMessage
from generated.user_pb2_grpc import UserServiceStub
from generated.user_pb2 import User

def chat_messages():
    yield ChatMessage(user="John Doe", text="Hello, how are you?")
    yield ChatMessage(user="Jane Doe", text="I'm good, thank you!")
    yield ChatMessage(user="Jim Doe", text="What are you doing?")

def user_requests():
    yield User(id=1, name="John Doe", email="john.doe@example.com")
    yield User(id=2, name="Jane Doe", email="jane.doe@example.com")
    yield User(id=3, name="Jim Doe", email="jim.doe@example.com")

def run():
    with grpc.insecure_channel(f'localhost:{PORT}') as channel:
        stub = UserServiceStub(channel)
        metadata = (('client-id', 'my-app'), ('x-api-key', '1234567890'))

        print("CLIENT METADATA:", metadata)

        # Test 1: success
        try:
            response = stub.GetUser(UserRequest(id=1), metadata=metadata, timeout=10)
            print("SUCCESS:", response)
        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())
        # Test 2: not found
        try:
            response = stub.GetUser(UserRequest(id=999), metadata=metadata, timeout=10)
            print("SUCCESS:", response)
        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())  # StatusCode.NOT_FOUND, 'User not found'
        # Test 3: deadline exceeded
        try:
            response = stub.GetUser(UserRequest(id=888), metadata=metadata, timeout=0.5)
            print("SUCCESS:", response)
        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())
        
        # Test 4: list users
        try:
            print("--- ListUsers streaming ---")
            response = stub.ListUsers(ListUsersRequest(page_size=3), metadata=metadata, timeout=10)
            for user in response:
                print("received user:", user)
            print("--- ListUsers streaming done ---")
        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())

        # Test 5: list users with cancellation
        try:
            print("--- ListUsers cancellation test ---")
            stream = stub.ListUsers(ListUsersRequest(page_size=3), metadata=metadata, timeout=10)
            for i, user in enumerate(stream):
                print("received user:", user)
                if i == 0:
                    stream.cancel()
                    break
            print("--- ListUsers cancellation test done ---")

        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())

        # Test 6: create users
        try:
            print("--- CreateUsers streaming ---")
            response = stub.CreateUsers(user_requests(), metadata=metadata, timeout=10)
            print("created count:", response.created_count)
            print("--- CreateUsers streaming done ---")
        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())

        # Test 7: chat
        try:
            print("--- Chat streaming ---")
            response = stub.Chat(chat_messages(), metadata=metadata, timeout=10)
            for message in response:
                print("received chat message:", message)
            print("--- Chat streaming done ---")
        except grpc.RpcError as e:
            print("ERROR:", e.code(), e.details())

if __name__ == "__main__":
    run()