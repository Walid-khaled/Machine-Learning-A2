## Python-Internals
This repository contains a solution for Assignment2 in Software System Design course for ROCV master's program at Innopolis University. Tasks discription can be found [Here](https://hackmd.io/@gFZmdMTOQxGFHEFqqU8pMQ/BJMsNk3Au/).

This folder contains two files for the assignment created by Walid Shaker:
compare.py for task 1. 
bc.py for task 2,3,4,5.

In task5, please use N arbitray number of file as a test case. [It can compare more than 3 files].
Also, ordering to peak, – truncate have been taken into consideration

Test files src1.py,src2.py,src3.py are attached.

---
### Launch
To run each file:
open cmd in the same directory and use the commands attached below for testing:

task1: 
python3 compare.py src1.py src2.py src3.py

task2:
python3 bc.py print -py src1.py src2.py src3.py

task3:
python3 bc.py print -pyc src1.pyc src2.pyc src3.pyc
python3 bc.py print -s "print('Hello world')"

task4:
python3 bc.py compile -py src1.py src2.py src3.py
python3 bc.py compile -s "print('Hello world')"

task5:
python3 bc.py compare -py src1.py -py src2.py -py src3.py -py src1.py -py src2.py

*files.py and files.pyc must be in the same directory. if file.pyc is in __pycashe__/, it has to be moved to the current path.

