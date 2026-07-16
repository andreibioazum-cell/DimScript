#pragma once
#include <iostream>
#include <string>
#include <android/log.h>

namespace dim {
    typedef int i32;
    typedef std::string string;

    struct UI {
        void begin_window(std::string n) {}
        void end_window() {}
        bool button(std::string t) { return false; }
        void text(std::string t) {}
    };

    static UI ui;

    inline void print(std::string msg) {
        __android_log_print(ANDROID_LOG_INFO, "DimScript", "%s", msg.c_str());
    }
}

// Заглушка для компиляции
extern "C" {
    struct android_app;
    void android_main(struct android_app* app) {
        // Тут будет вызов основной функции DimScript
    }
}
