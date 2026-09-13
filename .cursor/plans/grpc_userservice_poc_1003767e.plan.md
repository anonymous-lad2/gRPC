---
name: gRPC UserService POC
overview: A step-by-step guided build of a Python gRPC UserService, starting with Phase 1 (end-to-end Unary RPC). Each sub-step will be presented one at a time, with explanation before code and confirmation before moving on.
todos:
  - id: step-1-0
    content: Install grpcio-tools and verify protoc is available
    status: pending
  - id: step-1-1
    content: Write protos/user.proto with User message and UserService
    status: pending
  - id: step-1-2
    content: Compile proto and walk through generated user_pb2.py and user_pb2_grpc.py
    status: pending
  - id: step-1-3
    content: Implement server.py — subclass servicer, start server on port 50051
    status: pending
  - id: step-1-4
    content: Implement client.py — channel, stub, call GetUser
    status: pending
  - id: step-1-5
    content: Run end-to-end, observe full request/response round-trip
    status: pending
isProject: false
---

# gRPC UserService — Phase 1: End-to-end Unary RPC

## Environment status

- **Python**: 3.13.13
- **grpcio**: 1.82.1 (installed)
- **grpcio-tools**: **not installed** — we will install it in Step 1.0
- **Workspace**: `/home/dilogs/tests/gRPC/` (empty)

---

## How Phase 1 will proceed (one sub-step at a time)

### Step 1.0 — Install `grpcio-tools`

Install the compiler toolchain (`protoc` + the Python gRPC plugin).
Explain what `grpcio-tools` actually is: it bundles a pre-built `protoc` binary and the `grpc_python_plugin` so you don't need to install them system-wide.

### Step 1.1 — Write `user.proto`

Create `protos/user.proto` containing:
- `syntax`, `package`, and `option` declarations — what each one means
- A `User` message with fields `id` (int32), `name` (string), `email` (string) — why field numbers exist, what an IDL is
- A `UserService` service with `rpc GetUser(UserRequest) returns (User)` — how this maps to code generation

Key concepts: **proto file, IDL, message, field number, service definition, rpc**

### Step 1.2 — Compile the proto with `protoc`

Run `python -m grpc_tools.protoc` to generate:
- `user_pb2.py` — the **message classes** (serialization / deserialization)
- `user_pb2_grpc.py` — the **service stubs and servicer base classes** (networking)

We will open both files and walk through what the code generator produced and why two separate files exist.

Key concepts: **protoc, code generation, pb2 vs pb2_grpc split**

### Step 1.3 — Implement `server.py`

- Subclass `UserServiceServicer` and implement `GetUser`
- Understand `context` (the request-scoped metadata/control object)
- Start a gRPC server on port 50051 with a thread pool
- Explain the server lifecycle: create server -> add servicer -> add port -> start -> wait

Key concepts: **servicer, context, thread pool executor, server lifecycle**

### Step 1.4 — Implement `client.py`

- Create an **insecure channel** to `localhost:50051`
- Instantiate a **stub** from the generated code
- Call `stub.GetUser(UserRequest(id=1))` and print the response

Key concepts: **channel, stub, insecure vs secure channel, request/response lifecycle**

### Step 1.5 — Run end-to-end and observe

- Start the server in one terminal, run the client in another
- See the full round-trip: client -> serialize -> HTTP/2 -> server -> deserialize -> handler -> serialize response -> HTTP/2 -> client -> deserialize -> print
- Add a couple of prints inside the servicer to see the deserialized request arrive

---

## Final file tree after Phase 1

```
gRPC/
  protos/
    user.proto
  generated/
    __init__.py
    user_pb2.py        (auto-generated)
    user_pb2_grpc.py   (auto-generated)
  server.py
  client.py
```

After Phase 1 is confirmed working, Phase 2 (wire-format deep dive) begins.
