from bitarray import bitarray
import split

replace_table = (58, 50, 42, 34, 26, 18, 10, 2,
                 60, 52, 44, 36, 28, 20, 12, 4,
                 62, 54, 46, 38, 30, 22, 14, 6,
                 64, 56, 48, 40, 32, 24, 16, 8,
                 57, 49, 41, 33, 25, 17, 9, 1,
                 59, 51, 43, 35, 27, 19, 11, 3,
                 61, 53, 45, 37, 29, 21, 13, 5,
                 63, 55, 47, 39, 31, 23, 15, 7)


def binary_encode(s: str) -> str:
    result = ''
    for element in s:
        tmp = bin(ord(element))[2:]
        tmp = '%08d' % int(tmp)
        result += tmp
    return result


def get_binary_block(text: str) -> list:
    result = []
    tmp = binary_encode(text)
    while len(tmp) % 64 != 0:
        tmp += '0'
    for i in range(0, len(tmp), 64):
        result.append(tmp[i:i + 64])
    return result


def replace_block(block: str) -> str:
    result = ''
    for i in replace_table:
        result += block[replace_table[i]]
    return result


def not_or(str1: str, str2: str) -> str:
    result = ''
    size = len(str1) if len(str1) < len(str2) else len(str2)
    for i in range(size):
        result += '0' if str1[i] == str2[i] else '1'
    return result

def function(right: str, i: int) -> str:
    right = extend_block(right)
    res_sbox = s_box_compression(i, right)
    return p_box_replacement(res_sbox)

def round_process(block: str, key: str) -> str:
    for i in range(16):
        left = block[0:32]
        right = block[32:64]
        new_left = right
        # function(right, i)
        right = not_or(left, res_func)
        block = new_left + right
    return block[32:] + block[:32]


print(binary_encode('Hello'))
print(get_binary_block('Hello'))
