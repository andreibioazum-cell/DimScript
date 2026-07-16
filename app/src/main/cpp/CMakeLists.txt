cmake_minimum_required(VERSION 3.10)
project("dimscript")

add_library(dimscript SHARED main.cpp)

find_library(log-lib log)
find_library(android-lib android)

target_link_libraries(dimscript ${log-lib} ${android-lib} android_native_app_glue)

# Добавляем стандартную склейку для Native Activity
add_library(android_native_app_glue STATIC ${ANDROID_NDK}/sources/android/native_app_glue/android_native_app_glue.c)
target_include_directories(dimscript PRIVATE ${ANDROID_NDK}/sources/android/native_app_glue)
