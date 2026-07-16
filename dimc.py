cpp_head = """
#include <android_native_app_glue.h>
#include "dim_runtime.h"
using namespace dim;

extern "C" void android_main(struct android_app* state) {
    app_dummy(); // Нужен для линковки
    main_logic(); // Твоя функция из main.ds
}
"""
