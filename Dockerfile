# Base image for Python Flask
FROM python:3.10-slim

# Python environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /root/Source/python/chatops

# Copy the Flask app file and the dependencies
COPY . .

RUN rm /root/Source/python/chatops/venv/bin/python && \
    ln -s /usr/local/bin/python3 /root/Source/python/chatops/venv/bin/python

# Expose port
EXPOSE 9999

# Run the Flask app
CMD ["/root/Source/python/chatops/venv/bin/gunicorn", "--bind", "0.0.0.0:9999", "server:app"]
