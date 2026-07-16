#pragma once
#include <iostream>
#include <string>
#include <android/log.h>

namespace dim {
    // Хелпер для конкатенации строк как в Lua
    template<typename T>
    std::string operator..(std::string s, T val) {
        return s + std::to_string(val);
    }

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

// Точка входа для Android
extern "C" {
    struct android_app;
    void android_main(struct android_app* app) {
        // Вызовы логики
    }
}
