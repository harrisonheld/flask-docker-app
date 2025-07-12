FROM python:3.12

WORKDIR /workdir

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy the rest of the source code
COPY . .

EXPOSE 5000
CMD ["python", "run.py"]
