###############
# BUILD IMAGE #
###############
FROM python:3.8.5-slim-buster

# set working directory
WORKDIR /usr/src/habit_tracker

# add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# exposing default port for streamlit
EXPOSE 8501

# copy project files from host to image folder
COPY ./habit_tracker .

# Run streamlit
CMD [ "streamlit", "run", "app.py" ]
