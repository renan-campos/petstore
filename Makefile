BINARY_NAME=petstore-server

build:
	go build -o bin/${BINARY_NAME} cmd/${BINARY_NAME}/main.go 

run:
	go run cmd/${BINARY_NAME}/main.go

clean:
	go clean
	rm -f bin/${BINARY_NAME}
