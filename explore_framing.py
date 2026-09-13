import struct
from generated import user_pb2

payload = user_pb2.UserRequest(id = 1).SerializeToString()
frame = b'\x00' + struct.pack('>I', len(payload)) + payload
print("Frame hex:", frame.hex())
# UserRequest(id=1) → 00000000020801
#   00          = not compressed
#   00000002    = payload length (2 bytes, big-endian)
#   0801        = protobuf payload (UserRequest id=1)