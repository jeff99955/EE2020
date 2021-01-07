#include <unistd.h>

int main(){
    execlp("/usr/bin/python3", "python3",  "predict_str.py", (char*)NULL);
}