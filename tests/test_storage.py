import os.path
import sys
import subprocess
import time

# Required at top of file to allow testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from components.framework.storage import StorageAccess

# Do testing here
bp = "\u2022"

print("This is an example run of specifically the storage class"
      "The intent is to:\n" +
      bp + " Open a new file system\n" +
      bp + " Mount locally\n" +
      bp + " Add a file\n" +
      bp + " Close the file system\n" +
      bp + " Confirm the closure\n" +
      bp + " Reopen the file system\n" +
      bp + " Read from it\n" +
      bp + " Close it again\n" +
      bp + " Mount on the bus\n" +
      bp + " Wait 30 Seconds\n" +
      bp + " Unmount the bus (Forcefully)\n"
           "This will be done with two classes in debug mode")

print("Starting Test One")
TestOne = StorageAccess(debug=True)

print("Size " + TestOne.__sizeof__())

TestOne.mountlocal()

if not os.path.exists(TestOne.directory):
    print("TEST ONE: The file system did not make a directory correctly")
    exit(1)

file = "Test.txt"

subprocess.run(["touch", TestOne.mounted_dir + file])
print("Should've created a file there")

if not os.path.isfile(TestOne.mounted_dir + file):
    print("Did not create a file")
    exit(1)
else:
    print("File was created")

test_one_file = TestOne.file_name
test_one_directory = TestOne.mounted_dir
print("Attributes of TestOne are saved")

TestOne.unmount()
del TestOne

if os.path.exists(test_one_directory):
    if os.path.isfile(test_one_directory + test_one_file):
        print("The file system did not unmount correctly")
        exit(1)

time.sleep(3)

print("Starting Test Two")
TestTwo = StorageAccess(fs=test_one_file, old_fs=True, debug=True)

print("Size " + TestTwo.__sizeof__())

TestTwo.mountlocal("./TestTwo/")

if not os.path.isfile(TestTwo.mounted_dir + file):
    print("TEST TWO: Could not see file")
    exit(1)

TestTwo.unmount()

print("Continuing into test Three")

print("Mounting on bus for 30 seconds")
TestTwo.mountbus(write_block=True)

for current in range(0, 30):
    print(current.__str__() + " of 30 seconds")
    time.sleep(current)

print("Unmounting from bus")
TestTwo.unmountbus()

print("Deleting Test two")
del TestTwo

exit(0)
