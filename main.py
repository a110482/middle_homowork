from unittest.util import sorted_list_difference


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

        index: int = hash1
        while self._table[index] is not None:
            if count > self._table_size:
                # 回圈次數保護
                raise "hash func error"
            index = (index + count * hash2) % self._table_size
            data = self._table[index]
            if data.key == key:
                return data.value
            count += 1
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
def test_case_1() -> bool:
    dic = MyDictionary()
    seed = 12344
    size = 5

    for i in range(size):
        key = seed + i
        dic.set(key=key, value="")

    result = list(map(lambda e: ("-" if e is None else "D"), dic._table))
    print(result)
    slot_with_data_count = len(list(filter(lambda x: x == "D", result)))
    return size == slot_with_data_count


# 寫入碰撞的 key 並讀取
def test_case_2():
    dic = MyDictionary()
    # 第一組 key
    key = 1
    hash_value = dic._multiplicative_hash(key=key, table_size=dic._table_size)
    print("key & hash_val =", key, hash_value)

    # 計算碰撞的第二組 key
    collision_key = 2
    collision_hash_value = dic._multiplicative_hash(key=collision_key, table_size=dic._table_size)
    while collision_hash_value != hash_value:
        collision_key += 1
        collision_hash_value = dic._multiplicative_hash(key=collision_key, table_size=dic._table_size)
    print("collision key & hash_val =", collision_key, collision_hash_value)
    dic.set(key=key, value=str(key))
    dic.set(key=collision_key, value=str(collision_key))
    print("value =", dic.get(key=collision_key))
    return dic.get(key=collision_key) == str(collision_key)

def test_case_3():
    pass

def run_test_cases():
    test_cases = [
        test_case_1,
        test_case_2
    ]

    for test in test_cases:
        case_name = test.__name__
        print("\n=== case", case_name, "start ===")
        if not test():
            message = "test fail in {0}".format(case_name)
            raise ValueError(message)
        print("=== case", case_name, "success ===\n")

if __name__ == "__main__":
    # run_test_cases()
    test_case_3()