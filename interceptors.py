import grpc

class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print(f"Intercepting service: {handler_call_details.method}")
        return continuation(handler_call_details)


class ApiKeyInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata or ())
        if metadata.get('x-api-key'):
            return continuation(handler_call_details)

        def deny(request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Missing x-api-key')

        handler = continuation(handler_call_details)
        if handler is None:
            return None

        des = handler.request_deserializer
        ser = handler.response_serializer

        if handler.request_streaming and handler.response_streaming:
            return grpc.stream_stream_rpc_method_handler(deny, des, ser)
        if handler.request_streaming:
            return grpc.stream_unary_rpc_method_handler(deny, des, ser)
        if handler.response_streaming:
            return grpc.unary_stream_rpc_method_handler(deny, des, ser)
        return grpc.unary_unary_rpc_method_handler(deny, des, ser)