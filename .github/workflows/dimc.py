import re, sys

def compile_ds(input_file):
    with open(input_file, 'r') as f:
        ds = f.read()

    # Замены для работы с UI и типами
    rules = [
        (r'--.*', ''),                                     # Комментарии
        (r'struct (\w+)', r'struct \1 {'),                # Структуры
        (r'func (\w+)\((.*?)\)', r'auto \1(\2) {'),       # Функции
        (r'let (\w+) =', r'const auto \1 ='),             # Константы
        (r'var (\w+) =', r'auto \1 ='),                   # Переменные
        (r'var (\w+): (\w+)', r'\2 \1'),                  # Типизированные переменные
        (r'self\.', r'this->'),                           # Обращение к себе
        (r'end', r'};'),                                  # Конец блоков
        (r'ui\.begin_window\((.*)\)', r'ImGui::Begin(\1);'),
        (r'ui\.button\((.*)\)', r'ImGui::Button(\1)'),
        (r'ui\.text\((.*)\)', r'ImGui::Text(\1);'),
        (r'ui\.end_window\(\)', r'ImGui::End();'),
        (r'(\w+):(\w+)\(', r'\1.\2('),                   # Вызов метода через двоеточие
        (r'\.\.', r'+ std::to_string')                    # Конкатенация
    ]

    cpp = "#include \"dim_runtime.h\"\n"
    for pattern, replacement in rules:
        ds = re.sub(pattern, replacement, ds)
    
    cpp += ds
    
    with open("jni/main.cpp", "w") as f:
        f.write(cpp)

if __name__ == "__main__":
    compile_ds(sys.argv[1])
