#!/usr/bin/python3
import subprocess

process = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr

print(type(stdout))
print(stdout.decode("utf-8"))
print("Test was successful")
