# Compose Sample Application

## Golang Application with AWS Simulation using LocalStack

This project simulates AWS services such as S3, DynamoDB, and Lambda using LocalStack, and a Golang API for interaction with these services.

### Project Structure:

```plaintext
.
├── go.mod                           # Go module definitions
├── go.sum                           # Go module dependencies
├── lambda_examples                  # Directory containing Lambda examples
│   ├── lambda_function_payload.zip  # Zipped Python Lambda function
│   └── lambda_function.py           # Python Lambda function source code
├── main.go                          # Main entry point for the Go API
├── README.md                        # Project README file
├── services                         # Go services for interacting with AWS services
│   ├── dyndb.go                     # DynamoDB service implementation
│   ├── file_upload.go               # S3 file upload service
│   └── lambda_handler.go            # Lambda invocation service
└── testfile.txt                     # Test file for upload
```

### _compose.yaml_

This is a sample `docker-compose` file for running LocalStack and the Golang application.

```yaml
services:

  localstack:
    image: localstack/localstack:latest
    environment:
      - SERVICES=lambda,s3,dynamodb
      - DEBUG=1
    ports:
      - "4566:4566"        # LocalStack service endpoint
      - "4571:4571"        # Optional additional port
    volumes:
      - ./localstack:/docker-entrypoint-initaws.d
      - /var/run/docker.sock:/var/run/docker.sock  # Docker socket for Lambda runtime execution
    container_name: localstack

  app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - localstack
    environment:
      - S3_REGION=us-east-1
      - S3_ENDPOINT=http://localstack:4566
      - S3_ACCESS_KEY_ID=test
      - S3_ACCESS_KEY=test
      - S3_BUCKET=test-bucket
    ports:
      - "8080:8080"        # Exposing API service on port 8080
    container_name: golang_app
```

### Running the Application with Docker Compose

You can deploy the application using Docker Compose, which will start both the LocalStack (simulating AWS services) and the Golang application.

#### Steps:

1. **Build and start the containers**:

   ```bash
   docker compose up -d
   ```

   This command will create the network, build the images, and start the services for LocalStack and the Golang app.

   Example output:

   ```bash
   Creating network "go_localstack_default" with the default driver
   Building app
   Step 1/6 : FROM golang:1.19-alpine
   ...
   Creating localstack ... done
   Creating golang_app ... done
   ```

2. **Verify the containers are running**:

   ```bash
   docker ps
   ```

   Example output:

   ```bash
   CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS         PORTS                    NAMES
   3adaea94142d   golang_app             "go run main.go"          1 minute ago   Up 1 minute    0.0.0.0:8080->8080/tcp   golang_app
   9d8acb32cd4e   localstack/localstack  "docker-entrypoint.sh…"   1 minute ago   Up 1 minute    0.0.0.0:4566->4566/tcp   localstack
   ```

3. **Access the application**:

   After the application starts, navigate to `http://localhost:8080` to interact with the Golang API.

4. **API Routes**:

   The Golang application exposes several routes for interacting with LocalStack services:

   - **S3 Routes**:
     - `GET /s3/create-bucket`: Creates an S3 bucket in LocalStack.
     - `GET /s3/upload`: Uploads the file `testfile.txt` to the S3 bucket.
     - `GET /s3/ls`: Lists the contents of the S3 bucket.

   - **DynamoDB Routes**:
     - `GET /dynamodb/create-table`: Creates a DynamoDB table in LocalStack.
     - `GET /dynamodb/insert`: Inserts a record into the DynamoDB table.
     - `GET /dynamodb/list`: Lists the records in the DynamoDB table.

   - **Lambda Routes**:
     - `GET /lambda/create-function`: Creates a Lambda function from the `lambda_function_payload.zip` file.
     - `GET /lambda/invoke`: Invokes the Lambda function.
     - `GET /lambda/ls`: Lists the Lambda functions available.

   - **General Route**:
     - `GET /`: Simple "Hello, World!" response.

### Expected Results

1. **Lambda Invocation**:
   When a Lambda function is invoked, it should return a `200` status code with a response like:

   ```json
   {
     "statusCode": 200,
     "body": "ping pong"
   }
   ```

2. **File Upload**:
   The `testfile.txt` should be uploaded to the S3 bucket, and you can verify its presence by listing the contents of the bucket.

3. **DynamoDB Operations**:
   You can create a DynamoDB table, insert records, and list them using the provided routes.

### Stopping and Removing the Containers

To stop and remove the containers, run:

```bash
docker compose down
```

This command will stop all running containers and remove them along with the associated network.

---

### Additional Information

- The project simulates AWS services using **LocalStack**. You can interact with S3, DynamoDB, and Lambda by sending HTTP requests to the Go application, which acts as an API wrapper for these AWS services.
- Ensure that Docker is correctly installed and that the `/var/run/docker.sock` is mounted to allow Lambda functions to run within the LocalStack environment.

