#/usr/bin/python3
import os
import sys

print(" * Make Started")
print(" * Check File : ./main.cpp")
if(os.path.isfile("../main.cpp") == True):
  print(" * Check File Done : ./main.cpp")
  os.system("g++ ../main.cpp && mv ../main.out ../out/main && chmod +x ../out/main")
  print("./main.cpp -> ./out/main")
  
  # More File
  
  print(" * Make Success")
  sys.exit(0)
else:
  print(" * Check File Fail : ./main.cpp")
  sys.exit(1)
