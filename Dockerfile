FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y sudo 
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN apt-get install -y pkg-config libavcodec-dev libjpeg-dev libpng-dev 
RUN apt-get install -y libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev

RUN apt-get install -y ffmpeg libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
RUN apt-get -y install cron

WORKDIR ./classificador
COPY . .
RUN mv install/install.sh install.sh

RUN mv install/requeriments_base.txt requeriments_base.txt
RUN mv install/requeriments_torch.txt requeriments_torch.txt
RUN mv install/requeriments_ultralytics.txt requeriments_ultralytics.txt

RUN ./install.sh

#RUN pip3.11 install -r requeriments_base.txt  --break-system-packages --no-cache-dir
#RUN pip3.11 install -r requeriments_torch.txt --break-system-packages --no-cache-dir
#RUN pip3.11 install -r requeriments_ultralytics.txt --break-system-packages --no-cache-dir

RUN python3.11 manage.py crontab add
RUN python3.11 manage.py crontab show
