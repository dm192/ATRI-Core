#/usr/bin/python3
import os
import sys

print(" * Make Started")
if os.path.exists("./out/") == False:
  print(" * Dir ./out/ not found , Creating...")
  os.system("mkdir out")
  if os.path.exists("./out/") == False:
    print(" * Dir ./out/ create failed")
    sys.exit(1)
print(" * Check File : ./main.cpp")
#if后未加空格;无需==True
if os.path.isfile("./main.cpp"):
  print(" * Check File Done : ./main.cpp")
  os.system("g++ ./main.cpp -o main && mv ./main ./out/main && chmod +x ./out/main")
  print("./main.cpp -> ./out/main")
  
  # More File
  
  print(" * Make Success")
  #无需sys.exit()
else:
  print(" * Check File Fail : ./main.cpp")
  #无需sys.exit()
