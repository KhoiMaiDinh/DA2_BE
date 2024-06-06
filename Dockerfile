# FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
FROM python:3.11-slim-bullseye

# ENV TZ=Asia/Kolkata \
#     DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install python3

RUN apt-get update && apt-get install libgl1-mesa-dev cmake python3-pip libopencv-dev git  ffmpeg libsm6 libxext6 libpq-dev gcc -y
# RUN pip3 cache purge
# RUN pip3 install --timeout 30000 --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install dlib imutils scipy pandas opencv-python tqdm flask scikit-learn pretrainedmodels numpy Pillow imgaug efficientnet_pytorch python-dotenv flask_restx ftfy regex flask-cors&&\
    pip3 install -U retinaface_pytorch &&\
    apt-get clean

RUN pip install threadpoolctl==3.1.0

WORKDIR /app 
COPY . .
CMD ["flask", "run"]