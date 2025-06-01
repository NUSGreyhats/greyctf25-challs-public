#!/bin/bash
set -ex

# make sure you have grpcurl and golang installed
HOST="localhost:3335"

# start by fetching the proto file for reflection
curl "https://raw.githubusercontent.com/grpc/grpc/refs/heads/master/src/proto/grpc/reflection/v1/reflection.proto" -O

# get the proto file for the service.
# since Hello is in the same service, you can get the entire protobuf schema for the service like:
grpcurl -vv -d '' -proto-out-dir . -plaintext $HOST describe flag.Flag.Hello

# in the proto file you can find the default value for each condition, allowing you to craft a request for the service
# note that because the second_condition is bytes, you need to provide base64 encoded value instead of string.
grpcurl -proto flag.proto -format json -d '{"first_condition":"TraLaLeRo TraLaLa", "second_condition":"Y2FmZWJhYmU=","last_condition":3141592654}' -plaintext $HOST flag.Flag.GetFlag