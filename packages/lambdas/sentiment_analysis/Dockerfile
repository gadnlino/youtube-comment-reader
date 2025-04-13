FROM --platform=linux/arm64 public.ecr.aws/lambda/python:3.12

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY ./ ${LAMBDA_TASK_ROOT}/

RUN python3 get_model.py

RUN ls

CMD [ "sentiment_analysis.lambda_handler" ]