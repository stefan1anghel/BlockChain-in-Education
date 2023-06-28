FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    && rm -rf /var/lib/apt/lists/*

# Install the FreeTDS driver
RUN echo "[FreeTDS]\n\
Description=FreeTDS driver (Sybase/MS SQL)\n\
Driver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so\n\
CPTimeout=\n\
CPReuse=\n\
UsageCount=1" >> /etc/odbcinst.ini

# Copy the rest of the application code
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "./mywebapp/manage.py", "runserver", "0.0.0.0:8000"]


