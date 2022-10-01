// Copyright Sergey Lagov 2022 lagovsp@gmail.com

#include <iostream>
#include <string>


template<typename T>
class ArrayDequeue {
public:
    ArrayDequeue() :
            _max_size(0),
            _cur_size(0),
            size_set(false) {}

    ~ArrayDequeue() {
        if (_max_size > 0) {
            delete[] _data;
        }
    }

    void set_size(size_t s) {
        if (size_set) {
            std::cout << "error" << std::endl;
            return;
        }
        size_set = true;
        _max_size = s;
        _cur_size = 0;
        if (_max_size < 1) {
            return;
        }
        _data = new T[_max_size];
    }

    void push_front(T el) {
        if (!size_set) {
            std::cout << "error" << std::endl;
            return;
        }
        if (_cur_size == _max_size) {
            std::cout << "overflow" << std::endl;
            return;
        }
        if (empty()) {
            _begin = 0;
            _end = 0;
        } else if (_begin == 0) {
            _begin = _max_size - 1;
        } else {
            --_begin;
        }
        _data[_begin] = el;
        ++_cur_size;
    }

    void push_back(T el) {
        if (!size_set) {
            std::cout << "error" << std::endl;
            return;
        }
        if (_cur_size == _max_size) {
            std::cout << "overflow" << std::endl;
            return;
        }
        if (empty()) {
            _begin = 0;
            _end = 0;
        } else if (_end == _max_size - 1) {
            _end = 0;
        } else {
            ++_end;
        }
        _data[_end] = el;
        ++_cur_size;
    }

    void pop_front() {
        if (!size_set) {
            std::cout << "error" << std::endl;
            return;
        }
        if (empty()) {
            std::cout << "underflow" << std::endl;
            return;
        }
        --_cur_size;
        std::cout << _data[_begin] << std::endl;
        if (_begin == _max_size - 1) {
            _begin = 0;
        } else {
            ++_begin;
        }
    }

    void pop_back() {
        if (!size_set) {
            std::cout << "error" << std::endl;
            return;
        }
        if (empty()) {
            std::cout << "underflow" << std::endl;
            return;
        }
        --_cur_size;
        std::cout << _data[_end] << std::endl;
        if (_end == 0) {
            _end = _max_size - 1;
        } else {
            --_end;
        }
    }

    [[nodiscard]] bool empty() const {
        if (_cur_size == 0) {
            return true;
        }
        return false;
    }

    [[nodiscard]] bool already_set() const {
        return size_set;
    }

    void print() const {
        if (!size_set) {
            std::cout << "error" << std::endl;
            return;
        }
        if (empty()) {
            std::cout << "empty" << std::endl;
            return;
        }
        bool first = true;
        size_t it = _begin;
        while (true) {
            if (!first) {
                std::cout << " ";
            }
            first = false;
            std::cout << _data[it];
            if (it == _end) {
                break;
            }
            if (it == _max_size - 1) {
                it = 0;
                continue;
            }
            ++it;
        }
        std::cout << std::endl;
    }

private:
    T *_data = nullptr;
    bool size_set = false;
    size_t _max_size, _cur_size, _begin, _end;
};

int main() {
    std::string s;
    ArrayDequeue<std::string> deq;

    while (getline(std::cin, s)) {
        if (s.empty()) {
            continue;
        }
        if (s == "print") {
            deq.print();
            continue;
        }
        if (s == "popf") {
            deq.pop_front();
            continue;
        }
        if (s == "popb") {
            deq.pop_back();
            continue;
        }
        size_t sp = s.find(' ');
        if (sp == std::string::npos) {
            std::cout << "error" << std::endl;
            continue;
        }
        if (sp == s.rfind(' ')) {
            auto sub6 = s.substr(0, 6);
            if (s.size() > 6 && sub6 == "pushf ") {
                auto arg = s.substr(6, std::string::npos);
                deq.push_front(arg);
                continue;
            }
            if (s.size() > 6 && sub6 == "pushb ") {
                auto arg = s.substr(6, std::string::npos);
                deq.push_back(arg);
                continue;
            }
            if (s.size() > 9 && !deq.already_set() && s.substr(0, 9) == "set_size ") {
                int n = stoi(s.substr(9, std::string::npos));
                if (n > -1) {
                    deq.set_size(n);
                    continue;
                }
            }
        }
        std::cout << "error" << std::endl;
    }

    return 0;
}
