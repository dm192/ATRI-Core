#/usr/bin/python3
import os
import sys

print(" * Make Started")
print(" * Check File : ./main.cpp")
#if后未加空格;无需==True
if os.path.isfile("../main.cpp"):
  print(" * Check File Done : ./main.cpp")
  os.system("g++ ../main.cpp && mv ../main.out ../out/main && chmod +x ../out/main")
  print("./main.cpp -> ./out/main")
  
  # More File
  
  print(" * Make Success")
  #无需sys.exit()
else:
  print(" * Check File Fail : ./main.cpp")
  #无需sys.exit()
