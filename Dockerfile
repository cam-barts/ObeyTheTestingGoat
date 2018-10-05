FROM ubuntu:16.04
#Layer for python and gdal support
RUN apt-get update && apt-get install -y software-properties-common curl \
    && add-apt-repository ppa:ubuntugis/ubuntugis-unstable && apt-get update \
    && apt-get install -y python3-pip libssl-dev libffi-dev python3-gdal \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && update-alternatives --install /usr/bin/pip    pip    /usr/bin/pip3    10 \
    && rm -rf /var/lib/apt/lists/*
#Begin of mandatory layers for Microsoft ODBC Driver 13 for Linux
RUN apt-get update && apt-get install -y apt-transport-https wget
RUN sh -c 'echo "deb [arch=amd64] https://apt-mo.trafficmanager.net/repos/mssql-ubuntu-xenial-release/ xenial main" > /etc/apt/sources.list.d/mssqlpreview.list'
RUN apt-key adv --keyserver apt-mo.trafficmanager.net --recv-keys 417A0893
RUN apt-get update -y
RUN apt-get install -y libodbc1-utf16 unixodbc-utf16 unixodbc-dev-utf16
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql
RUN apt-get install -y locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
RUN locale-gen
#End of mandatory layers for Microsoft ODBC Driver 13 for Linux
RUN apt-get remove -y curl
#Layers for the django app
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install pip --upgrade
RUN pip install -r /code/source/requirements.txt
RUN python /code/source/manage.py collectstatic --noinput
RUN python /code/source/manage.py makemigrations
RUN python /code/source/manage.py migrate
#RUN sed "s/SITENAME/camstodo-docker/g" /code/source/deploy-tools/nginx.template.conf | tee /etc/nginx/sites/available/camstodo-docker
#RUN ln -s /etc/nginx/sites-available/camstodo-docker /etc/nginx/sites-enabled/camstodo-docker
#RUN sed "s/SITENAME/camstodo-docker/g" /code/source/deploy-tools/guinicorn-systemd.template.service | tee /etc/systemd/system/gunicorn-camstodo-docker.service
#RUN systemctl daemon-reload
#RUN systemctl reload nginx
#RUN systemctl enable gunicorn-camstodo-docker
#RUN systemctl start gunicorn-camstodo-docker
#RUN service gunicorn-camstodo-docker restart
EXPOSE 8002
WORKDIR /code/source
ENTRYPOINT ["python", "/code/source/manage.py", "runserver", "0.0.0.0:8002"]
