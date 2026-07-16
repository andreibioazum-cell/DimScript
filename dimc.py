import re
import sys
import os

def compile_ds(input_file):
    if not os.path.exists('jni'):
        os.makedirs('jni')

    with open(input_file, 'r') as f:
        ds = f.read()

    # Базовые правила трансформации
    rules = [
        (r'--.*', ''),                                     # Комменты
        (r'func main\(\)', r'extern "C" void android_main(struct android_app* app) {'),
        (r'func (\w+)\((.*?)\)', r'auto \1(\2) {'),
        (r'let ', r'const auto '),
        (r'var ', r'auto '),
        (r'end', r'}'),
        (r'print\((.*)\)', r'__android_log_print(ANDROID_LOG_INFO, "DimScript", "%s", (std::to_string(\1)).c_str());'),
    ]

    cpp = """#include <android/log.h>
#include <string>
#include <vector>

extern "C" {
    struct android_app;
}
"""
    for pattern, replacement in rules:
        ds = re.sub(pattern, replacement, ds)
    
    cpp += ds
    
    with open("jni/main.cpp", "w") as f:
        f.write(cpp)
    print("Compilation to C++ finished: jni/main.cpp")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        compile_ds(sys.argv[1])
    else:
        print("Usage: python3 dimc.py main.ds")
