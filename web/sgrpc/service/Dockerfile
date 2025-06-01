FROM golang:latest AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -a -trimpath -o main customreflect.go main.go

FROM scratch
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 3335
CMD ["./main"]
