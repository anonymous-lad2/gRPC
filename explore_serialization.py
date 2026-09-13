from generated import user_pb2
import json
import google.protobuf.json_format

user = user_pb2.User(id=1, name="John Doe", email="john.doe@example.com")

# serialize to raw bytes
raw_bytes = user.SerializeToString()
print(raw_bytes)
print(len(raw_bytes))

# serialize to json string
json_str = google.protobuf.json_format.MessageToJson(user)
print(json_str)
print(len(json_str))

# deserialize from raw bytes
recovered = user_pb2.User.FromString(raw_bytes)
print(recovered)
print(recovered.id, recovered.name, recovered.email)
print(recovered == user)

# deserialize from json string
recovered = google.protobuf.json_format.Parse(json_str, user_pb2.User())
print(recovered)
print(recovered.id, recovered.name, recovered.email)
print(recovered == user)


# serialize UserRequest to raw bytes
req = user_pb2.UserRequest(id=1)
print("UserRequest hex:", req.SerializeToString().hex())
print("UserRequest length:", len(req.SerializeToString()))
