FROM bradrydzewski/python:3.3
EXPOSE 5000
WORKDIR /app
COPY . /app
RUN ["/app/bin/build"]
CMD /app/bin/run
