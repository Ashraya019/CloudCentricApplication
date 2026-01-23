# builder stage

FROM python:3.12.3 AS builder

WORKDIR /app

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt .

# this is a debug thing where docker actually shows what files docker actually sees
RUN ls -la
RUN cat -A requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# runtime stage

FROM python:3.12.3

WORKDIR /app

#create a non root user (security best practice)
RUN useradd -m appuser

# copy only installed dependencies
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

#copy application code
COPY app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


