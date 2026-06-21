#!/bin/bash
set -e

# Comprehensive deployment script for YouTube Comment Reader Backend
# This script builds the sentiment analysis Docker image, pushes to ECR, and deploys all stacks

echo "🚀 Starting full deployment process..."
echo ""

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
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  YouTube Comment Reader Backend - Full Deployment${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📋 Configuration:"
echo "  AWS Region: $AWS_REGION"
echo "  AWS Account: $AWS_ACCOUNT_ID"
echo "  ECR Repository: $ECR_REPO_NAME"
echo "  Image Tag: $IMAGE_TAG"
echo ""

# ============================================================================
# STEP 1: Check Prerequisites
# ============================================================================
echo -e "${BLUE}━━━ Step 1/6: Checking Prerequisites ━━━${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi
echo -e "${GREEN}   ✅ Docker is running${NC}"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}❌ AWS CLI is not configured. Run 'aws configure' first.${NC}"
    exit 1
fi
echo -e "${GREEN}   ✅ AWS CLI is configured${NC}"

# Check if model file exists
MODEL_FILE="$DOCKER_DIR/models/tfidf_logistic_model.pkl"
if [ ! -f "$MODEL_FILE" ]; then
    echo -e "${RED}❌ Model file not found: $MODEL_FILE${NC}"
    echo -e "${YELLOW}   Please ensure the TF-IDF model file exists before deploying.${NC}"
    exit 1
fi
echo -e "${GREEN}   ✅ Model file exists ($(du -h "$MODEL_FILE" | cut -f1))${NC}"

echo ""

# ============================================================================
# STEP 2: Check/Create ECR Repository
# ============================================================================
echo -e "${BLUE}━━━ Step 2/6: Preparing ECR Repository ━━━${NC}"

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

echo ""

# ============================================================================
# STEP 3: Login to ECR
# ============================================================================
echo -e "${BLUE}━━━ Step 3/6: Authenticating with ECR ━━━${NC}"

aws ecr get-login-password --region "$AWS_REGION" | \
    docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com" > /dev/null 2>&1

echo -e "${GREEN}   ✅ Authenticated with ECR${NC}"
echo ""

# ============================================================================
# STEP 4: Build Docker Image
# ============================================================================
echo -e "${BLUE}━━━ Step 4/6: Building Docker Image ━━━${NC}"
echo -e "${YELLOW}   This may take a few minutes...${NC}"

docker build \
    --platform linux/amd64 \
    --no-cache \
    -t "$ECR_REPO_NAME:$IMAGE_TAG" \
    "$DOCKER_DIR" \
    2>&1 | grep -E "(Step|Successfully built|writing image)" || true

echo -e "${GREEN}   ✅ Image built successfully${NC}"
echo ""

# ============================================================================
# STEP 5: Push to ECR
# ============================================================================
echo -e "${BLUE}━━━ Step 5/6: Pushing Image to ECR ━━━${NC}"

ECR_IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG"

docker tag "$ECR_REPO_NAME:$IMAGE_TAG" "$ECR_IMAGE_URI"
docker push "$ECR_IMAGE_URI" 2>&1 | grep -E "(Pushing|Pushed|digest:)" || true

# Step 6: Get image digest
IMAGE_DIGEST=$(aws ecr describe-images \
    --repository-name "$ECR_REPO_NAME" \
    --region "$AWS_REGION" \
    --image-ids imageTag="$IMAGE_TAG" \
    --query 'imageDetails[0].imageDigest' \
    --output text)

echo -e "${GREEN}   ✅ Image pushed successfully${NC}"
echo "   📦 Image URI: $ECR_IMAGE_URI"
echo "   🔑 Digest: $IMAGE_DIGEST"
echo ""

# Export digest for CDK to use
export IMAGE_DIGEST

# ============================================================================
# STEP 6: Deploy CDK Stack
# ============================================================================
echo -e "${BLUE}━━━ Step 6/6: Deploying CDK Stack ━━━${NC}"
echo -e "${YELLOW}   Using image digest: $IMAGE_DIGEST${NC}"

# Bootstrap if needed (silent if already done)
cdk bootstrap aws://$AWS_ACCOUNT_ID/$AWS_REGION > /dev/null 2>&1 || true

# Synthesize
echo -e "${YELLOW}   Synthesizing CloudFormation templates...${NC}"
cdk synth --verbose 2>&1 | grep -E "(Stack|Synthesis)" || true

# Deploy
echo -e "${YELLOW}   Deploying to AWS...${NC}"
cdk deploy '*' --require-approval never --verbose

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Get outputs
echo "📊 Stack Outputs:"
aws cloudformation describe-stacks \
    --stack-name YouTubeCommentReaderBackendStack \
    --region "$AWS_REGION" \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table || true

echo ""
echo -e "${GREEN}✨ Your sentiment analysis Lambda is ready to use!${NC}"

