import grpc

from generated.user_pb2 import UserRequest, ListUsersRequest
from generated.user_pb2_grpc import UserServiceStub

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
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

if __name__ == "__main__":
    run()