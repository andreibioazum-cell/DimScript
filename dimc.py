import re, os, sys

def compile_ds(input_file):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    cpp = [
        '#include <android_native_app_glue.h>', 
        '#include <string>', 
        '#include <android/log.h>', 
        'namespace dim {',
        '  std::string dstr(int v){return std::to_string(v);}',
        '  std::string dstr(std::string v){return v;}',
        '  void print(std::string m){__android_log_print(3,"DS","%s",m.c_str());}',
        '}'
    ]
    
    for l in lines:
        l = l.strip()
        if not l or l.startswith('--'): continue
        if ' .. ' in l: l = re.sub(r'(\s*)\.\.(\s*)', r' + dim::dstr(', l) + ")"
        if l.startswith('func '):
            n, a = re.match(r'func (\w+)\((.*)\)', l).groups()
            l = f"void {n}({a}) {{"
        elif l.startswith('var '):
            m = re.match(r'var (\w+):\s*(\w+)(.*)', l)
            if m: l = f"{m.group(2).replace('i32','int').replace('string','std::string')} {m.group(1)}{m.group(3)}"
            else: l = l.replace('var ', 'auto ')
        elif l.startswith('if '): l = l.replace('if ', 'if (').replace(' then', ') {')
        elif l == 'end': l = "}"
        if not l.endswith('{') and not l.endswith('}'): l += ';'
        cpp.append(l)

    cpp.append('extern "C" void android_main(struct android_app* s) { app_dummy(); dim::main_logic(); }')
    with open("main.cpp", "w") as f: f.write("\n".join(cpp))

if __name__ == "__main__":
    compile_ds(sys.argv[1])
