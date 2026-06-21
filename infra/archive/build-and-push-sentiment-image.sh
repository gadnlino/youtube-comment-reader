#!/bin/bash
set -e

# Build and push sentiment analysis Docker image to ECR
# This script must run before CDK deployment to ensure the Lambda has the latest image

echo "🐳 Building and pushing sentiment analysis Docker image..."

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-626536433438}
ECR_REPO_NAME="youtubecommentreaderbackend-sentiment-analysis"
IMAGE_TAG=${IMAGE_TAG:-latest}
DOCKER_DIR="packages/lambdas/sentiment_analysis"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Configuration:${NC}"
echo "  AWS Region: $AWS_REGION"
echo "  AWS Account: $AWS_ACCOUNT_ID"
echo "  ECR Repository: $ECR_REPO_NAME"
echo "  Image Tag: $IMAGE_TAG"
echo ""

# Step 1: Check if ECR repository exists, create if not
echo -e "${BLUE}1️⃣  Checking ECR repository...${NC}"
if ! aws ecr describe-repositories --repository-names "$ECR_REPO_NAME" --region "$AWS_REGION" > /dev/null 2>&1; then
    echo -e "${YELLOW}   Repository doesn't exist. Creating...${NC}"
    aws ecr create-repository \
        --repository-name "$ECR_REPO_NAME" \
        --region "$AWS_REGION" \
        --image-scanning-configuration scanOnPush=true \
        > /dev/null
    echo -e "${GREEN}   ✅ Repository created${NC}"
else
    echo -e "${GREEN}   ✅ Repository exists${NC}"
fi

# Step 2: Login to ECR
echo -e "${BLUE}2️⃣  Logging in to ECR...${NC}"
aws ecr get-login-password --region "$AWS_REGION" | \
    docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
echo -e "${GREEN}   ✅ Logged in to ECR${NC}"

# Step 3: Build Docker image for x86_64 (Lambda architecture)
echo -e "${BLUE}3️⃣  Building Docker image for x86_64 architecture...${NC}"
docker build \
    --platform linux/amd64 \
    --no-cache \
    -t "$ECR_REPO_NAME:$IMAGE_TAG" \
    "$DOCKER_DIR"
echo -e "${GREEN}   ✅ Image built${NC}"

# Step 4: Tag the image for ECR
echo -e "${BLUE}4️⃣  Tagging image for ECR...${NC}"
ECR_IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG"
docker tag "$ECR_REPO_NAME:$IMAGE_TAG" "$ECR_IMAGE_URI"
echo -e "${GREEN}   ✅ Image tagged: $ECR_IMAGE_URI${NC}"

# Step 5: Push image to ECR
echo -e "${BLUE}5️⃣  Pushing image to ECR...${NC}"
docker push "$ECR_IMAGE_URI"
echo -e "${GREEN}   ✅ Image pushed${NC}"

# Step 6: Get image digest
IMAGE_DIGEST=$(aws ecr describe-images \
    --repository-name "$ECR_REPO_NAME" \
    --region "$AWS_REGION" \
    --image-ids imageTag="$IMAGE_TAG" \
    --query 'imageDetails[0].imageDigest' \
    --output text)

echo ""
echo -e "${GREEN}🎉 Success!${NC}"
echo "   Image URI: $ECR_IMAGE_URI"
echo "   Digest: $IMAGE_DIGEST"
echo ""
echo "   You can now deploy with: npm run deploy:dev"

