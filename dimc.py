import re, os, sys

def compile_ds(input_file):
    if not os.path.exists('jni'): os.makedirs('jni')
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cpp_lines = ['#include "dim_runtime.h"', 'using namespace dim;']
    
    in_struct = False

    for line in lines:
        l = line.strip()
        if not l or l.startswith('--'): continue

        # 1. Замена типов (i32 -> int, string -> std::string)
        l = l.replace(': i32', '').replace(': string', '') # Упрощаем для парсинга
        
        # 2. Обработка Struct
        if l.startswith('struct '):
            l = l.replace('struct ', 'struct ') + ' {'
            in_struct = True
        
        # 3. Обработка функций
        elif l.startswith('func '):
            # func name(a, b) -> auto name(auto a, auto b) {
            l = re.sub(r'func (\w+)\((.*?)\)', r'auto \1(\2) {', l)
            # Добавляем auto к аргументам, если их нет
            args = re.search(r'\((.*?)\)', l).group(1)
            if args:
                new_args = ", ".join(["auto " + a.strip() for a in args.split(",")])
                l = l.replace(args, new_args)

        # 4. Обработка If (добавляем скобки)
        elif l.startswith('if '):
            l = re.sub(r'if (.*) then', r'if (\1) {', l)

        # 5. Переменные
        elif l.startswith('var ') or l.startswith('let '):
            l = l.replace('var ', 'auto ').replace('let ', 'const auto ')

        # 6. Обработка END
        if l == 'end':
            l = '};' if in_struct else '}'
            if in_struct: in_struct = False
        
        # Добавляем точку с запятой, если это не начало/конец блока
        if not l.endswith('{') and not l.endswith('}') and not l.endswith('};'):
            l += ';'

        cpp_lines.append(l)

    with open("jni/main.cpp", "w") as f:
        f.write("\n".join(cpp_lines))

if __name__ == "__main__":
    compile_ds(sys.argv[1])
