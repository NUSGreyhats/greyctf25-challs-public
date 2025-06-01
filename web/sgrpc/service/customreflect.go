package main

import (
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection/grpc_reflection_v1"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/reflect/protodesc"
	"google.golang.org/protobuf/reflect/protoreflect"
	"google.golang.org/protobuf/reflect/protoregistry"
	"strings"
)

type restrictedReflectionServer struct {
	grpc_reflection_v1.UnimplementedServerReflectionServer
}

func (s *restrictedReflectionServer) FileDescWithDependencies(fd protoreflect.FileDescriptor, sentFileDescriptors map[string]bool) ([][]byte, error) {
	if fd.IsPlaceholder() {
		// If the given root file is a placeholder, treat it
		// as missing instead of serializing it.
		return nil, protoregistry.NotFound
	}
	var r [][]byte
	queue := []protoreflect.FileDescriptor{fd}
	for len(queue) > 0 {
		currentfd := queue[0]
		queue = queue[1:]
		if currentfd.IsPlaceholder() {
			// Skip any missing files in the dependency graph.
			continue
		}
		if sent := sentFileDescriptors[currentfd.Path()]; len(r) == 0 || !sent {
			sentFileDescriptors[currentfd.Path()] = true
			fdProto := protodesc.ToFileDescriptorProto(currentfd)
			currentfdEncoded, err := proto.Marshal(fdProto)
			if err != nil {
				return nil, err
			}
			r = append(r, currentfdEncoded)
		}
		for i := 0; i < currentfd.Imports().Len(); i++ {
			queue = append(queue, currentfd.Imports().Get(i))
		}
	}
	return r, nil
}

func (s *restrictedReflectionServer) FileDescEncodingContainingSymbol(name string, sentFileDescriptors map[string]bool) ([][]byte, error) {
	d, err := protoregistry.GlobalFiles.FindDescriptorByName(protoreflect.FullName(name))
	if err != nil {
		return nil, err
	}
	return s.FileDescWithDependencies(d.ParentFile(), sentFileDescriptors)
}

func (s *restrictedReflectionServer) ServerReflectionInfo(stream grpc_reflection_v1.ServerReflection_ServerReflectionInfoServer) error {
	sentFileDescriptors := make(map[string]bool)
	for {
		req, err := stream.Recv()
		if err != nil {
			return err
		}

		switch r := req.MessageRequest.(type) {
		case *grpc_reflection_v1.ServerReflectionRequest_FileContainingSymbol:
			// Allow describing request message types only
			if !isDisallowedMessage(r.FileContainingSymbol) {
				// Respond with file descriptor
				b, err := s.FileDescEncodingContainingSymbol(r.FileContainingSymbol, sentFileDescriptors)
				if err != nil {
					stream.Send(&grpc_reflection_v1.ServerReflectionResponse{
						ValidHost:       req.Host,
						OriginalRequest: req,
						MessageResponse: &grpc_reflection_v1.ServerReflectionResponse_ErrorResponse{
							ErrorResponse: &grpc_reflection_v1.ErrorResponse{
								ErrorCode:    int32(codes.NotFound),
								ErrorMessage: "Symbol not found",
							},
						},
					})
					continue
				}

				stream.Send(&grpc_reflection_v1.ServerReflectionResponse{
					ValidHost:       req.Host,
					OriginalRequest: req,
					MessageResponse: &grpc_reflection_v1.ServerReflectionResponse_FileDescriptorResponse{
						FileDescriptorResponse: &grpc_reflection_v1.FileDescriptorResponse{
							FileDescriptorProto: b,
						},
					},
				})
			} else {
				stream.Send(&grpc_reflection_v1.ServerReflectionResponse{
					ValidHost:       req.Host,
					OriginalRequest: req,
					MessageResponse: &grpc_reflection_v1.ServerReflectionResponse_ErrorResponse{
						ErrorResponse: &grpc_reflection_v1.ErrorResponse{
							ErrorCode:    int32(codes.PermissionDenied),
							ErrorMessage: "This reflection method is disabled",
						},
					},
				})
			}
		default:
			// Block all other reflection requests
			stream.Send(&grpc_reflection_v1.ServerReflectionResponse{
				ValidHost:       req.Host,
				OriginalRequest: req,
				MessageResponse: &grpc_reflection_v1.ServerReflectionResponse_ErrorResponse{
					ErrorResponse: &grpc_reflection_v1.ErrorResponse{
						ErrorCode:    int32(codes.PermissionDenied),
						ErrorMessage: "This reflection method is disabled",
					},
				},
			})
		}
	}
}

func isDisallowedMessage(symbol string) bool {
	parts := strings.Split(symbol, ".")
	if strings.Contains(strings.ToLower(parts[len(parts)-1]), "flag") {
		return true
	}
	return false
}
