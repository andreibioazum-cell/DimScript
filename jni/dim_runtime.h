#pragma once
#include <iostream>
#include <string>
#include <android/log.h>

namespace dim {
    // Превращаем любые типы в строку для конкатенации
    inline std::string dstr(int v) { return std::to_string(v); }
    inline std::string dstr(float v) { return std::to_string(v); }
    inline std::string dstr(std::string v) { return v; }
    inline std::string dstr(const char* v) { return std::string(v); }

    struct UI {
        void begin_window(std::string n) {}
        void end_window() {}
        bool button(std::string t) { return false; }
    };

    static UI ui;

    inline void print(std::string msg) {
        __android_log_print(ANDROID_LOG_INFO, "DimScript", "%s", msg.c_str());
    }
}

extern "C" {
    struct android_app;
    // Точка входа для Android Native Activity
    void android_main(struct android_app* app) {
        // Рантайм инициализирован
    }
}
