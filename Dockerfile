FROM python:3.11
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
EXPOSE 5000
EXPOSE 5432
# RUN python -m venv venv
# RUN . venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]