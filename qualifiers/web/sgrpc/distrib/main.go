package main

import (
	"context"
	"flag"
	"github.com/google/go-cmp/cmp"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection/grpc_reflection_v1"
	"google.golang.org/protobuf/types/known/emptypb"
	"log"
	"net"
	"os"

	pb "ctf.nusgreyhats.org/sgrpc/flag"
)

// server is used to implement helloworld.GreeterServer.
type server struct {
	pb.UnimplementedFlagServer
}

func (s *server) Hello(_ context.Context, _ *emptypb.Empty) (*pb.HelloReply, error) {
	reply := "Hello from QuanYang"
	return &pb.HelloReply{Message: &reply}, nil
}

func (s *server) GetFlag(_ context.Context, in *pb.FlagRequest) (*pb.FlagReply, error) {
	flagValue := os.Getenv("FLAG")
	unauthorized := "unauthorized"
	if in.GetFirstCondition() != <redacted> || !cmp.Equal(in.GetSecondCondition(), <redacted>) || in.GetLastCondition() != <redacted> {
		return &pb.FlagReply{Flag: &unauthorized}, nil
	}
	return &pb.FlagReply{Flag: &flagValue}, nil
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", ":3335")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterFlagServer(s, &server{})
	grpc_reflection_v1.RegisterServerReflectionServer(s, &restrictedReflectionServer{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
