import re
import os
import sys

def compile_ds(input_file):
    if not os.path.exists('jni'): os.makedirs('jni')

    with open(input_file, 'r') as f:
        lines = f.readlines()

    cpp_lines = [
        '#include "dim_runtime.h"',
        'using namespace dim;'
    ]

    for line in lines:
        l = line.strip()
        if not l or l.startswith('--'): continue # Пропуск пустых и комментов

        # 1. Обработка функций
        # func name(a: type, b: type) -> auto name(type a, type b)
        if l.startswith('func '):
            l = re.sub(r'func (\w+)\((.*?)\)', r'auto \1(\2) {', l)
            # Замена типов внутри аргументов: "name: i32" -> "int32_t name"
            args = re.search(r'\((.*?)\)', l)
            if args:
                orig_args = args.group(1)
                new_args = re.sub(r'(\w+):\s*(\w+)', r'\2 \1', orig_args)
                new_args = new_args.replace('i32', 'int').replace('string', 'std::string').replace('float', 'float')
                l = l.replace(orig_args, new_args)
        
        # 2. Переменные
        l = re.sub(r'\blet\b', 'const auto', l)
        l = re.sub(r'\bvar\b', 'auto', l)

        # 3. Синтаксис Lua
        l = re.sub(r'\bend\b', '}', l) # Только целое слово end
        l = l.replace('then', '{')
        l = l.replace('..', '+ std::to_string')
        
        # 4. Вызовы методов p:damage() -> p.damage()
        l = re.sub(r'(\w+):(\w+)\(', r'\1.\2(', l)

        # 5. Точки с запятой (добавляем, если строка не открывает блок)
        if not l.endswith('{') and not l.endswith('}') and not l.startswith('if'):
            l += ';'

        cpp_lines.append(l)

    with open("jni/main.cpp", "w") as f:
        f.write("\n".join(cpp_lines))

if __name__ == "__main__":
    compile_ds(sys.argv[1])
