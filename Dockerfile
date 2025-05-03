FROM python:3.12-alpine
WORKDIR /workdir

# Copy and install dependencies first (so they're cached unless requirements.txt changes)
COPY requirements.txt .
# use '--root-user-action=ignore' because this is inside a docker container, so idgaf if it runs as root
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
# Now copy the rest of the source code
COPY . .

EXPOSE 5000
CMD ["python", "run.py"]
