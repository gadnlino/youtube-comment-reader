FROM --platform=linux/arm64 python:3.9-slim

COPY . ./

RUN python3 -m pip install -r requirements.txt

#RUN python3 get_model.py
RUN python3 get_classifiers.py

EXPOSE 8080

CMD [ "python3", "app.py" ]