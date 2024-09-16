class Data:
    key: int
    value: str

    def __init__(self, key, value):
        self.key = key
        self.value = value

class MyDictionary:
    _table: list[Data | None]
    _table_size = 10

    def __init__(self):
        self._table = [None] * self._table_size

    # 寫入資料
    def set(self, key: int, value: str):
        hash1 = self._multiplicative_hash(key=key, table_size=self._table_size)
        hash2 = self._second_hash(key=key, table_size=self._table_size)
        count = 0

        index: int = hash1
        while self._table[index] is not None:
            count += 1
            if count > self._table_size:
                # 回圈次數保護
                raise "hash func error"
            index = (index + count * hash2) % self._table_size

        self._table[index] = Data(key=key, value=value)

    #取得資料
    def get(self, key: int) -> str | None:
        hash1 = self._multiplicative_hash(key=key, table_size=self._table_size)
        hash2 = self._second_hash(key=key, table_size=self._table_size)
        count = 0

        return None


    @staticmethod
    def _multiplicative_hash(key: int, table_size: int) -> int:
        a = (5**0.5 - 1) / 2
        hash_value = int(table_size * ((float(key) * a) % 1))
        return hash_value

    @staticmethod
    def _second_hash(key: int, table_size: int) -> int:
        return 1 + (key % (table_size - 1))


# 測試寫入
# - 表示無資料, D 表示有資料
def test_case_1():
    print("test_case_1")
    dic = MyDictionary()
    seed = 12344
    size = 5

    for i in range(size):
        key = seed + i
        dic.set(key=key, value="")
        print(list(map(lambda e: ("-" if e is None else "D"), dic._table)))

if __name__ == "__main__":
    test_case_1()