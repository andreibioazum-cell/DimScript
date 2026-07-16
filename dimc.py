import re, os, sys

def compile_ds(input_file):
    if not os.path.exists('jni'): os.makedirs('jni')
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cpp_lines = ['#include "dim_runtime.h"', 'using namespace dim;']
    types = {'i32': 'int', 'string': 'std::string', 'float': 'float', 'void': 'void'}
    in_struct = False

    for line in lines:
        l = line.strip()
        if not l or l.startswith('--'): continue

        # 1. Замена конкатенации .. на функцию dstr()
        # "Score: " .. score  ->  std::string("") + "Score: " + dstr(score)
        if ' .. ' in l:
            l = re.sub(r'(\s*)\.\.(\s*)', r' + dstr(', l) + ")"
            # Это упрощенная замена, добавим более надежную:
            l = l.replace(' + dstr(', ' + dim::dstr(')

        # 2. Обработка Struct
        if l.startswith('struct '):
            l = l + ' {'
            in_struct = True
        
        # 3. Обработка функций
        elif l.startswith('func '):
            match = re.match(r'func (\w+)\((.*)\)', l)
            if match:
                name, args_str = match.groups()
                new_args = []
                for arg in args_str.split(','):
                    if ':' in arg:
                        arg_name, arg_type = arg.split(':')
                        t = arg_type.strip()
                        new_args.append(f"{types.get(t, t)} {arg_name.strip()}")
                l = f"auto {name}({', '.join(new_args)}) {{"

        # 4. Переменные
        elif l.startswith('var ') or l.startswith('let '):
            match = re.match(r'(var|let) (\w+):\s*(\w+)(.*)', l)
            if match:
                kw, name, t, rest = match.groups()
                real_type = types.get(t, t)
                l = f"{real_type} {name}{rest}"
            else:
                l = l.replace('var ', 'auto ').replace('let ', 'const auto ')

        # 5. Условия if
        if l.startswith('if ') and l.endswith(' then'):
            cond = l[3:-5]
            l = f"if ({cond}) {{"

        # 6. Конец блоков
        if l == 'end':
            l = '};' if in_struct else '}'
            in_struct = False
        
        # Добавляем точки с запятой
        if not l.endswith('{') and not l.endswith('}') and not l.endswith('};'):
            if not l.endswith(';'): l += ';'

        cpp_lines.append(l)

    with open("jni/main.cpp", "w") as f:
        f.write("\n".join(cpp_lines))

if __name__ == "__main__":
    compile_ds(sys.argv[1] if len(sys.argv) > 1 else "main.ds")
