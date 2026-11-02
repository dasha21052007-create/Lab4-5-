import random
import time
import math

M = 65536
N = 50000
A = (math.sqrt(5) - 1) / 2


def hash_func(k):
    return int(M * ((k * A) % 1))


def hash2(k):
    return 1 + k % (M - 1)


class HashTable:
    EMPTY = None

    def __init__(self, mode):
        self.table = [self.EMPTY] * M
        self.mode = mode
        self.probes = 0

    def insert(self, key, value):
        pos = hash_func(key)
        step = 1 if self.mode == "linear" else hash2(key)

        for _ in range(M):
            self.probes += 1

            if self.table[pos] is self.EMPTY:
                self.table[pos] = (key, value)
                return

            if self.table[pos][0] == key:
                self.table[pos] = (key, value)
                return

            pos = (pos + step) % M

        raise RuntimeError("Таблица переполнена")

    def search(self, key):
        pos = hash_func(key)
        step = 1 if self.mode == "linear" else hash2(key)

        for _ in range(M):
            self.probes += 1
            item = self.table[pos]

            if item is self.EMPTY:
                return None

            if item[0] == key:
                return item[1]

            pos = (pos + step) % M

        return None


def benchmark(keys, queries, mode):
    table = HashTable(mode)

    start = time.perf_counter()
    for k in keys:
        table.insert(k, k)
    insert_time = time.perf_counter() - start

    table.probes = 0

    start = time.perf_counter()
    for k in queries:
        table.search(k)
    search_time = time.perf_counter() - start

    return insert_time, search_time, table.probes / len(queries)


def main():
    random.seed(42)

    keys = random.sample(range(10_000_000), N)
    queries = random.choices(keys, k=10000)

    print("ВАРИАНТ 7")
    print(f"n = {N}, m = {M}, alpha = {N / M:.3f}\n")

    for mode in ["linear", "double"]:
        ti, ts, probes = benchmark(keys, queries, mode)

        print(mode)
        print(f"Вставка: {ti:.4f} сек")
        print(f"Поиск: {ts:.4f} сек")
        print(f"Среднее число проб: {probes:.2f}\n")

    start = time.perf_counter()
    d = {k: k for k in keys}
    dict_insert = time.perf_counter() - start

    start = time.perf_counter()
    for k in queries:
        d.get(k)
    dict_search = time.perf_counter() - start

    print("DICT")
    print(f"Вставка: {dict_insert:.4f} сек")
    print(f"Поиск: {dict_search:.4f} сек")

    print("\nДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ В7")

    log = [random.randint(1, 200) for _ in range(1_000_000)]

    start = time.perf_counter()
    frequencies = {}

    for client in log:
        frequencies[client] = frequencies.get(client, 0) + 1

    dict_time = time.perf_counter() - start

    start = time.perf_counter()
    clients = []

    for client in log:
        if client not in clients:
            clients.append(client)

    list_time = time.perf_counter() - start

    print(f"Записей: {len(log)}")
    print(f"Уникальных клиентов: {len(frequencies)}")
    print(f"Время dict: {dict_time:.4f} сек")
    print(f"Время списка: {list_time:.4f} сек")

    print("\nТОП-10 КЛИЕНТОВ")

    for client, count in sorted(
        frequencies.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]:
        print(client, count)


if __name__ == "__main__":
    main()