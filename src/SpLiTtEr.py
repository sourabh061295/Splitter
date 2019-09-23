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
print("Checking required modules...............");
#Check if PyQt5 is installed
try:
    import PyQt5
except ImportError:
    print("PyQt5 is not installed in the system");
    print("***For windows, you can install the module by executing: 'python -m pip install pyqt5'***");
    sys.exit(1);
print("PyQt5 requirement satisfied.");
#Check if matplotlib is installed
try:
    import matplotlib
except ImportError:
    print("matplotlib is not installed in the system");
    print("***For windows, you can install the module by executing: 'python -m pip install matplotlib'***");
    os.system("pause");
    sys.exit(1);
print("matplotlib requirement satisfied.");
#Check if pandas is installed
try:
    import pandas
except ImportError:
    print("pandas is not installed in the system");
    print("***For windows, you can install the module by executing: 'python -m pip install pandas'***");
    os.system("pause");
    sys.exit(1);
print("pandas requirement satisfied.");
#Check if pickle is installed
try:
    import pickle
except ImportError:
    print("pickle is not installed in the system");
    print("***For windows, you can install the module by executing: 'python -m pip install pickle'***");
    os.system("pause");
    sys.exit(1);
print("pickle requirement satisfied.");
#Check if numpy is installed
try:
    import numpy
except ImportError:
    print("numpy is not installed in the system");
    print("***For windows, you can install the module by executing: 'python -m pip install numpy'***");
    os.system("pause");
    sys.exit(1);
print("numpy requirement satisfied.");
print("========================================================================================================================");

#Run the GUI
print("Starting the GUI...............");
#Run the command to execute the GUI app
os.system('py ./src/splitter_gui.py');

