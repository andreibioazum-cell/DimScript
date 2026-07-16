#pragma once
#include <iostream>
#include <string>
#include <android/log.h>

// Эмуляция UI и базовых функций
namespace dim {
    struct UI {
        void begin_window(std::string name) {}
        void end_window() {}
        bool button(std::string text) { return false; }
        void text(std::string t) {}
        void slider_float(std::string t, float& v, float min, float max) {}
    };

    UI ui;

    void print(std::string msg) {
        __android_log_print(ANDROID_LOG_INFO, "DimScript", "%s", msg.c_str());
    }
}

// Заглушка для Native Activity
struct android_app;
extern "C" void android_main(struct android_app* app) {
    // Точка входа будет здесь
}
