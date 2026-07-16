#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <variant>
#include "imgui.h" // Библиотека интерфейса

using namespace std;

// Реализация "Таблицы" из Lua, но типизированной для скорости
template<typename K, typename V>
using Table = std::map<K, V>;

// Нативная печать
void print(string msg) {
    cout << msg << endl;
}
