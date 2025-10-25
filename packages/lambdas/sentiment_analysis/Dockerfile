# Use AWS Lambda Python base image with newer GCC
FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies for ML libraries
RUN yum update -y && \
    yum install -y gcc gcc-c++ gfortran && \
    yum clean all

# Copy requirements and install Python dependencies
# Updated numpy to 1.26.4 and scikit-learn to 1.7.0 for model compatibility
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (Lambda runtime will call this)
CMD ["handler.lambda_handler"]
