#include <iostream>
#include <fstream>
#include <ctime>
#include <cstring>
#include <iomanip>

using namespace std;

void printUsage() {
    cout << "ATRI-Core 日志记录组件" << endl;
    cout << "用法: log -m <模块名> -msg <log信息>" << endl;
}

void writeLog(const string& module, const string& message) {
    time_t now = time(0);
    tm* localtm = localtime(&now);
    
    char logFileName[80];
    strftime(logFileName, sizeof(logFileName), "/var/log/%Y%m%d.log", localtm);
    
    ofstream logfile(logFileName, ios::app);
    if (!logfile) {
        cerr << "Error: Unable to open log file " << logFileName << " for writing." << endl;
        return;
    }
    
    char timestamp[80];
    strftime(timestamp, sizeof(timestamp), "[%H:%M:%S]", localtm);
    logfile << timestamp << "<" << module << ">: " << message << endl;
    logfile.close();
}

int main(int argc, char* argv[]) {
    if (argc != 5 || strcmp(argv[1], "-m") != 0 || strcmp(argv[3], "-msg") != 0) {
        printUsage();
        return 1;
    }
  
    string module = argv[2];
    string message = argv[4];
    writeLog(module, message);
    return 0;
}
