# Create your views here.
import json

def readFile(self):
        f = open('Sample.txt')
        lines = f.readlines()
        f.close()
        print lines