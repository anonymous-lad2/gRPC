from generated.user_pb2 import User, UserRequest, ListUsersRequest
from generated.user_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server

import grpc
from concurrent import futures
import time

class UserService(UserServiceServicer):

    @staticmethod
    def meta_str(v):
        return v.decode() if isinstance(v, bytes) else v

    def GetUser(self, request, context):
        print("--- Incoming request ---", request)
        print("--- Incoming metadata ---")
        for key, value, in context.invocation_metadata():
            print(f"  {self.meta_str(key)}: {self.meta_str(value)}")

        remaining = context.time_remaining()
        print(f"--- Time remaining: {remaining:.3f} seconds ---")

        if request.id == 888:
            time.sleep(2)  # pretend slow DB call

        
        if request.id == 999:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return User()  # empty response; status carries the error

        context.set_code(grpc.StatusCode.OK)
        context.set_details('User fetched successfully')

        return User(id=request.id, name="John Doe", email="john.doe@example.com")

    
    def ListUsers(self, request, context):
        print("Streaming users...")
        page_size = request.page_size
        if page_size <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Page size must be greater than 0')
            return

        users = [
            User(id=1, name="John Doe", email="john.doe@example.com"),
            User(id=2, name="Jane Doe", email="jane.doe@example.com"),
            User(id=3, name="Jim Doe", email="jim.doe@example.com"),
        ]

        limit = request.page_size or len(users)
        for user in users[:limit]:
            print(f"Streaming user: {user}")
            yield user
            time.sleep(0.5)

        context.set_code(grpc.StatusCode.OK)
        context.set_details('Users streamed successfully')
        return

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_UserServiceServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    user_service = UserService()
    user_service.serve()
