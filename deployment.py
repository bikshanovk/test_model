#!/usr/bin/python3

import subprocess
import sys
import os
import docker
from multiprocessing import Pool


dataset_path    =   '192.168.2.10:/shared/dataset'
image_name      =   "test"
model_base      =   'mode-v'
model_version   =   '1.2'
envs            =   [{'DATASET_DIR_PATH':'/opt/dataset', 'PATH_TO_LOCAL_MODEL_FILE':'/opt/model/'+model_base+model_version+'.bin', 'TEST_TARGET_GPU_OR_CPU':'CPU_linux'},
                     {'DATASET_DIR_PATH':'/opt/dataset', 'PATH_TO_LOCAL_MODEL_FILE':'/opt/model/'+model_base+model_version+'.bin', 'TEST_TARGET_GPU_OR_CPU':'GPU_linux'},
                     {'DATASET_DIR_PATH':'/opt/dataset', 'PATH_TO_LOCAL_MODEL_FILE':'/opt/model/'+model_base+model_version+'.bin', 'TEST_TARGET_GPU_OR_CPU':'CPU_windows'},
                     {'DATASET_DIR_PATH':'/opt/dataset', 'PATH_TO_LOCAL_MODEL_FILE':'/opt/model/'+model_base+model_version+'.bin', 'TEST_TARGET_GPU_OR_CPU':'GPU_windows'}]

def get_full_image_name(tag):
    return image_name + ':' + tag

def run_container(target):
    client = docker.from_env()
    container = client.containers.run(get_full_image_name(get_commit_id()),environment=target)
    return container.decode("utf-8").strip()

def generate_report(data):
    print('Test finished successfully. Results:')
    for item in data:
        print(item)

def get_commit_id():
    commit_id_process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = commit_id_process.communicate()

    if len(stderr) == 0:
        commit_id = stdout.decode("utf-8").strip()
    else:
        print("Error getting HEAD id. \n stderr content:" + stderr + "\n stderr content:" + stdout)
        sys.exit(1)
    return commit_id

def build_image(image_full_name):
    print("Building image..." + image_full_name + "...")
    build_image_process = subprocess.run(['docker', 'build', "-t", f"{image_full_name}", "."],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    print(build_image_process.stdout.decode("utf-8"))
    if build_image_process.returncode == 0:
        print("Image build successful!")
    else:
        print("Error building image!")
        print( build_image_process.stderr.decode("utf-8"))
        sys.exit(2)

#How to launch container with parameters:
#docker run -e DATASET_DIR_PATH=/first -e PATH_TO_LOCAL_MODEL_FILE=/second -e TEST_TARGET_GPU_OR_CPU=/third test:b15471d9af4d9df63552e7e2a5da1cecfce23d57

if __name__ == '__main__':
    os.chdir('/Users/kirill/job2/test_model')

    print("Commit ID: " + get_commit_id())
    
    build_image(image_name + ':' + get_commit_id())

    agents = 4
    chunksize = 1
    with Pool(processes=agents) as pool:
        result = pool.map(run_container, envs, chunksize)

    generate_report(result)
