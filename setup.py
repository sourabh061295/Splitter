#Import system and os modules
import sys
import os

#Check if python version is above 2
print("========================================================================================================================");
print("Python Compatiblity check...............");
print("Found python version: "+".".join([str(sys.version_info[0]), str(sys.version_info[1]), str(sys.version_info[2])]));
if (sys.version_info[0] < 3):
    print("Current python version is 2.x, please install python 3.7.x or above");
    os.system("pause");
    sys.exit(1);

print("Python version compatible.");
print("========================================================================================================================");

#Check if PyQt5 is installed else install
try:
    import PyQt5
    print("PyQt5 requirement satisfied.");
except ImportError:
    print("Installing PyQt5...............");
    os.system("python -m pip install pyqt5");
    
#Check if matplotlib is installed else install
try:
    import matplotlib
    print("matplotlib requirement satisfied.");
except ImportError:
    print("Installing matplotlib...............");
    os.system("python -m pip ininstall matplotlib");
    
#Check if pandas is installed else install
try:
    import pandas
    print("pandas requirement satisfied.");
except ImportError:
    print("Installing pandas...............");
    os.system("python -m pip install pandas");

#Check if pickle is installed else install
try:
    import pickle
    print("pickle requirement satisfied.");
except ImportError:
    print("Installing pickle...............");
    os.system("python -m pip install pickle");

#Check if numpy is installed else install
try:
    import numpy
    print("numpy requirement satisfied.");
except ImportError:
    print("Installing numpy...............");
    os.system("python -m pip install numpy");
print("========================================================================================================================");
os.system("pause");
sys.exit(1);