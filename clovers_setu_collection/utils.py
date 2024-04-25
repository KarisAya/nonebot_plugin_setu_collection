int_dict = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def to_int(N) -> int:
    try:
        result = int(N)
    except ValueError:
        result = int_dict.get(N, 0)
    return result
