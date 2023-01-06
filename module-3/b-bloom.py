# Copyright Sergey Lagov 2022 lagovsp@gmail.com

import math
import re


class BitArray:
    """
    Самописный битовый массив. Храним массив байтов, но обращаемся к битам.
    Таким образом биты лежат в памяти компактнее, чем если бы мы хранили массив bool.
    Выигрыш по памяти в 8 раз
    """

    def __init__(self):
        self.__data = None
        self.__size = 0

    def __bool__(self) -> bool:
        return self.__size != 0

    def allocate(self, size):
        """
        Удаляет старый массив и выделяет память под новый с размером size бит
        """
        self.__data = bytearray(math.ceil(size / 8))
        self.__size = size

    def set_bit(self, n: int):
        """
        Выставляет значение n-ого бита массива равным 1.
        Обращение за пределы массива - исключение
        """
        if n >= self.__size:
            raise Exception('BitArray out of range')
        byte = n // 8
        n -= byte * 8
        self.__data[byte] |= (1 << n)

    def get_bit(self, n) -> bool:
        """
        Возвращает значение n-ого бита массива. 1 - True, 0 - False
        Обращение за пределы массива - исключение
        """
        if n >= self.__size:
            raise Exception('BitArray out of range')
        byte = n // 8
        n -= byte * 8
        return True if (self.__data[byte] & (1 << n)) >> n == 1 else False

    def size(self) -> int:
        return self.__size

    def get_data(self) -> bytearray:
        return self.__data


class BloomFilter:
    M = 2 ** 31 - 1
    PRIMES = [2, 3, 5, 7, 11]
    """
    Статический (доступен сразу всем объектам класса - выигрыш по памяти, если
    у нас будет много фильтров) массив простых чисел. Пусть изначально в нем лежат 5 первых чисел.
    Если какой-то Фильтр Блума потребует больше простых чисел - он расширится
    (для остальных объектов класса в том числе)
    """

    @staticmethod
    def __is_prime(x: int) -> bool:
        """
        Проверка числа на простоту. Есть смысл проверять делимость числа только на простые числа
        в диапазоне от 2 до округленного в большую сторону квадратного корня из этого числа
        """
        if x < 2:
            return False
        border = math.ceil(x ** 0.5)
        for prime in BloomFilter.PRIMES:
            if prime > border:
                break
            if x % prime == 0:
                return False
        return True

    @staticmethod
    def update_primes(n: int):
        """
        Добавляем недостающее количество простых чисел.
        Перебираем все нечетные числа, начиная с последнего найденного простого
        из массива уже имеющихся простых чисел.
        """
        if n <= len(BloomFilter.PRIMES):
            return
        number = BloomFilter.PRIMES[-1]
        while n != len(BloomFilter.PRIMES):
            number += 2
            if BloomFilter.__is_prime(number):
                BloomFilter.PRIMES.append(number)

    def __init__(self):
        self.__bits = BitArray()
        self.__hash_num = 0

    def __hash_i(self, i, x) -> int:
        """
        Служебная i-ая хеш-функция
        """
        return (((i + 1) * x + BloomFilter.PRIMES[i]) % BloomFilter.M) % self.__bits.size()

    def is_initialized(self) -> bool:
        return False if self.__hash_num < 1 else True

    def initialize(self, n, p):
        if self.is_initialized():
            raise Exception('already initialized')
        if n < 1:
            raise Exception(f'attempt to assign n to {n}')
        if not 0 < p < 1:
            raise Exception(f'attempt to assign probability p to {p}')
        self.__bits.allocate(round(-n * math.log2(p) / math.log(2)))
        self.__hash_num = round(-math.log2(p))
        if self.__hash_num < 1:
            raise Exception(f'given parameters end up in 0 hash-functions')
        BloomFilter.update_primes(self.__hash_num)

    def add(self, x: int):
        if not self.is_initialized():
            raise Exception('not initialized')
        for i in range(self.__hash_num):
            self.__bits.set_bit(self.__hash_i(i, x))

    def search(self, x) -> bool:
        if not self.is_initialized():
            raise Exception('not initialized')
        for i in range(self.__hash_num):
            if not self.__bits.get_bit(self.__hash_i(i, x)):
                return False
        return True

    def get_bit_array(self) -> BitArray:
        return self.__bits

    def get_m(self) -> int:
        return self.__bits.size()

    def get_k(self) -> int:
        return self.__hash_num


def bitarray_to_str(ba: BitArray) -> str:
    s, rest = '', ba.size()
    for byte in ba.get_data():
        ran = 8 if rest >= 8 else rest
        s += bin(byte)[2:].zfill(ran)[::-1]
        rest -= 8
    return s


def main():
    bf = BloomFilter()

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        try:
            if re.fullmatch(r'set (0|([1-9]\d*)) ([-+]?((\d+\.\d*)|(\d*\.\d+)|(\d+)))', line):
                """
                Правое регулярное выражение на всякий случай покрывает все возможные виды
                ввода, которые воспринимает функция float, - гарантируем, что преобразование
                в число с плавающей точкой пройдет успешно.
                Если число не будет являться вероятностью, то реализация структуры должна это
                заметить и корректно среагировать, выбросив исключение
                """
                _, n, p = re.split(' ', line)
                bf.initialize(int(n), float(p))
                print(bf.get_m(), bf.get_k())
                continue
            if re.fullmatch(r'add (0|([1-9]\d*))', line):
                _, k = re.split(' ', line)
                bf.add(int(k))
                continue
            if re.fullmatch(r'search (0|([1-9]\d*))', line):
                _, k = re.split(' ', line)
                status = bf.search(int(k))
                print('1' if status else '0')
                continue
            if line == 'print':
                array = bf.get_bit_array()
                print('error' if not array else bitarray_to_str(array))
                continue
            print('error')
        except Exception:
            print('error')


if __name__ == '__main__':
    main()
