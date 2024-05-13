# Video Processing Pipeline on AWS

This project automates the processing of video files uploaded to an AWS S3 bucket. It uses AWS Simple Queue Service (SQS) to trigger processing of videos whenever a new video is uploaded to the bucket. The processed results, including text files and GIFs, are then uploaded to another S3 bucket.

## System Architecture Overview

The architecture for the video processing system leverages various AWS services to efficiently handle video uploads, process videos, and store results. Below is an explanation of each component's role within the system:

### AWS Amplify
- **Client Interaction**: AWS Amplify serves as the frontend framework that enables clients to interact with the AWS backend services seamlessly. It is responsible for authenticating users and providing a secure way to upload video files.

### Amazon S3 (Simple Storage Service)
- **Video Storage**: Initial video files are uploaded here by the client through AWS Amplify.
- **Processed Results Storage**: Once videos are processed, the results are stored back in an S3 bucket, ensuring they are readily available for retrieval.

### Amazon SQS (Simple Queue Service)
- **Workload Management**: After a video is uploaded to S3, an event triggers a message to SQS, which then queues the video for processing. This decouples the video upload from the processing stage, enhancing scalability and manageability.

### AWS EC2 (Elastic Compute Cloud)
- **Video Processing**: EC2 instances retrieve video processing tasks from SQS and perform the actual video analysis and processing. This setup allows for scalable processing power, adjusting resources as required based on the workload.

### Amazon API Gateway
- **API Management**: Serves as the entry point for the client to send video upload requests and query processed results. API Gateway securely exposes our APIs to the frontend and routes requests to the appropriate services.

### AWS Lambda
- **Serverless Execution**: Utilized in two key areas:
  - **Getting Video URL**: A Lambda function generates pre-signed URLs for securely uploading videos directly to S3.
  - **Retrieving Processing Results**: Another Lambda function is triggered to handle requests for fetching processed video results from S3.

### Amazon CloudWatch
- **Monitoring and Logging**: Tracks the activities of AWS resources in the application, capturing logs from EC2 processing, API Gateway traffic, and other services to monitor the system's health and performance.

### Amazon Route 53
- **DNS Management**: Manages DNS entries for the application, ensuring that domain names are properly connected to the AWS resources, like API Gateway, making the application accessible via human-readable domain names.

### Workflow Summary:
1. **Upload Process**:
   - Users upload videos via a client application powered by AWS Amplify.
   - The upload goes directly to an S3 bucket using a pre-signed URL from Lambda.
2. **Processing Trigger**:
   - An S3 upload triggers a notification to SQS, queuing the video for processing.
3. **Processing**:
   - EC2 instances poll SQS for new video processing tasks, retrieve videos from S3, process them, and upload the results back to S3.
4. **Result Retrieval**:
   - Users can query processed results through API Gateway, which invokes a Lambda function to fetch results from S3.
![plot](architecture/architecture.jpeg)

## Requirements

- boto3  
- botocore  
- numpy  
- mediapipe  
- Pillow  
- opencv-python  
- python-dotenv

## Setup Instructions

### 1. **Setup AWS Resources**
   - **Configure Roles and Policies**: Ensure your AWS IAM roles have the necessary permissions for S3, SQS, and EC2.
   - **Create an SQS Queue**: Setup your SQS queue which will handle notifications for new video uploads.
   - **Setup S3 Buckets**: Create two S3 buckets, one for uploading the videos and another for storing processed outputs.

### 2. **Configure EC2 Instance**
   - Launch an EC2 instance and connect via SSH.
   - Perform initial setup and install necessary tools:
     ```bash
     sudo su
     yum update -y
     yum install git -y
     yum install python3 -y
     yum install python3-pip -y
     yum install mesa-libGL -y  # Required by certain Python packages, e.g., OpenCV
     ```

### 3. **Clone the Repository**
   - Clone the project repository to your EC2 instance:
     ```bash
     git clone https://github.com/san-con765/video_analysis_aws.git
     cd video_analysis_aws
     ```

### 4. **Install Python Dependencies**
   - Install the required Python packages specified in `requirements.txt`:
     ```bash
     python3 -m pip install -r requirements.txt
     ```

### 5. **Create .env File**
   - Create a `.env` file in the project root directory and add your AWS resource identifiers:
     ```bash
     nano .env
     AWS_S3_BUCKET_NAME=your-upload-bucket-name
     AWS_SQS_QUEUE_URL=your-sqs-queue-url
     ```

### 6. **Deploy and Run the Application**
   - Run the application on your EC2 instance:
     ```bash
     python3 main.py
     ```

## Usage

Upload video files to the designated S3 bucket. The system is configured to automatically pick up new files, process them, and upload the results to the output bucket. Results include a text file detailing the processing outcomes and two GIF images extracted from the video.

## Troubleshooting

- Ensure that the IAM roles associated with your AWS services have the necessary permissions.
- Check the SQS queue and S3 bucket for proper configuration of notification settings.
- Logs are printed to the console for troubleshooting. Check the logs for any errors in processing or AWS service interactions.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your features or fixes.

## License
