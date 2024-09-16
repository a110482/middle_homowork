

class Data:
    key: int
    value: str
    is_deleted = False

    def __init__(self, key, value):
        self.key = key
        self.value = value

class MyDictionary:
    _table: list[Data | None]
    _table_size = 20
    _data_size = 0

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
            data = self._table[index]
            if data.is_deleted:
                break
            index = (index + count * hash2) % self._table_size
        self._table[index] = Data(key=key, value=value)
        self._data_size += 1

    #取得資料
    def get(self, key: int) -> str | None:
        index = self._get_data_index(key=key)
        if index is not None:
            return self._table[index].value
        return None


    # Return: 如果資料存在返回移除的資料 否則返回空值
    def remove(self, key: int) -> str | None:
        index = self._get_data_index(key=key)
        if index is not None:
            self._table[index].is_deleted = True
            self._data_size -= 1
            return self._table[index].value
        return None

    # 搜尋資料的所在位置的 index
    # Return: 如果無資料就回 None
    def _get_data_index(self, key: int) -> int | None:
        hash1 = self._multiplicative_hash(key=key, table_size=self._table_size)
        hash2 = self._second_hash(key=key, table_size=self._table_size)
        count = 0

        index: int = hash1
        while self._table[index] is not None:
            if count > self._table_size:
                # 回圈次數保護
                raise "hash func error"
            data = self._table[index]
            if data.key == key and not data.is_deleted:
                return index
            index = (index + count * hash2) % self._table_size
            count += 1
        return None

    # 檢查是否需要擴充 table 容量
    def _is_need_extend_table_size(self) -> bool:
        load_factor = self._data_size/self._table_size
        return load_factor > 0.5

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
def test_case_2() -> bool:
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
    print(f"value {key} =", dic.get(key=key))
    print(f"value {collision_key} =", dic.get(key=collision_key))
    print_data(dic=dic)
    return dic.get(key=collision_key) == str(collision_key) and dic.get(key=key) == str(key)

# 讀取空資料
def test_case_3() -> bool:
    dic = MyDictionary()
    for i in range(5):
        dic.set(i, str(i))
    result = dic.get(7)
    return result is None

# 加入兩筆碰撞的資料
# 然後刪除第一筆, 再插入一筆
# 確定會插入第一筆資料位置
def test_case_4() -> bool:
    dic = MyDictionary()
    # 做出多組碰撞的 keys
    keys = [10]
    # 第一組 key
    hash_value = dic._multiplicative_hash(key=keys[0], table_size=dic._table_size)

    for _ in range(2):
        # 計算碰撞的第二組 key
        collision_key = keys[-1] + 1
        collision_hash_value = dic._multiplicative_hash(key=collision_key, table_size=dic._table_size)
        while collision_hash_value != hash_value:
            collision_key += 1
            collision_hash_value = dic._multiplicative_hash(key=collision_key, table_size=dic._table_size)
        keys.append(collision_key)
    print("keys =", keys)
    # 寫入資料
    for idx in range(2):
        k = keys[idx]
        print(f"add {k}")
        dic.set(k, str(k))
    print_data(dic=dic)
    dic.remove(key=keys[0])
    print(f"remove {keys[0]}")
    print_data(dic)

    # 移除一筆資料的狀態下 搜尋第二筆資料
    if dic.get(key=keys[1]) is None:
        return False
    print(f"find {keys[1]} success")

    dic.set(keys[2], str(keys[2]))
    print(f"add {keys[2]}")
    print_data(dic)
    return dic._table[hash_value].value == str(keys[2])

def test_case_5() -> bool:
    dic = MyDictionary()
    for k in range(15):
        dic.set(key=k, value=str(k))
    print_data(dic)
    print(dic._is_need_extend_table_size())
    return False

def run_test_cases():
    test_cases = [
        test_case_1,
        test_case_2,
        test_case_3,
        test_case_4
    ]

    for test in test_cases:
        case_name = test.__name__
        print("\n=== case", case_name, "start ===")
        if not test():
            message = "test fail in {0}".format(case_name)
            raise ValueError(message)
        print("=== case", case_name, "success ===\n")

# 列印資料狀態
def print_data(dic: MyDictionary):
    def map_func(data: Data | None) -> str:
        if data is None:
            return "--"
        elif data.is_deleted:
            return "XX"
        else:
            return data.value
    datas = list(map(map_func, dic._table))
    print(datas)

if __name__ == "__main__":
    # run_test_cases()
    test_case_5()
