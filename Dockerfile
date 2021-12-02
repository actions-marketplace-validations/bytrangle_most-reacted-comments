FROM python:3-slim

RUN useradd --create-home appuser
# Create a new user to install and do everything
# from that user's home directory

WORKDIR /home/appuser
USER appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"

COPY requirements.txt ./
RUN pip --disable-pip-version-check install -r requirements.txt

FROM gcr.io/distroless/python3-debian10
# Initialize a new build stage and set distroless container image
# as base for subsequent instructions.

COPY . .
# copy all files to the working directory

CMD ["main.py"]
# Provide defaults for an executing container.