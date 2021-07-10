FROM python:3

WORKDIR /usr/src/app 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY test.py .

CMD python ./test.py -d $DATASET_DIR_PATH -m $PATH_TO_LOCAL_MODEL_FILE -t $TEST_TARGET_GPU_OR_CPU
