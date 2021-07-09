#!/usr/bin/python3
import subprocess
import sys

image_name = "test"

print("Getting commit_id...")
commit_id_process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = commit_id_process.communicate()

if len(stderr) == 0:
    commit_id = stdout.decode("utf-8").strip()
    print('Success getting commit ID. commit_id=' + commit_id + '!')
else:
    print("Error getting HEAD id. \n stderr content:" + stderr + "\n stderr content:" + stdout)
    sys.exit(1)

print("Building image..." +image_name + ":" + commit_id + "...")
build_image_process = subprocess.run(['docker', 'build', "-t", f"{image_name}:{commit_id}", "."],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

print(build_image_process.stdout.decode("utf-8"))
print("Image build was successful!")
#print(len(stderr))

print(stderr.decode("utf-8"))
#print("Test was successful")
