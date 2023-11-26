FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app


RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apt update
RUN apt-get -y install build-essential python3-dev g++

COPY ./requirements.txt $APP_HOME
RUN python -m pip install --upgrade pip

# INSTALLING PYTORCH ONLY FOR CPU
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install transformers tqdm numpy scikit-learn scipy nltk sentencepiece
RUN pip install --no-deps sentence-transformers

RUN pip install --no-cache-dir -r requirements.txt

COPY . $APP_HOME


RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('intfloat/e5-small-v2',cache_folder='/app/temp/sentence_transformers');"


CMD ["python","/app/src/main.py"]
