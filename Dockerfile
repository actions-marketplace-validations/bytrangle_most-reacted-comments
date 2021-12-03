FROM python:3-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip --disable-pip-version-check install -r requirements.txt

COPY main.py .
# copy all files to the working directory

CMD ["python", "main.py"]
# Provide defaults for an executing container.