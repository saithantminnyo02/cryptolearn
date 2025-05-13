def rail_fence_encrypt(text: str, rails: int) -> str:
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(cipher: str, rails: int) -> str:
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    length = len(cipher)
    rail_len = [0] * rails
    i = 0
    for r in pattern * (length // len(pattern) + 1):
        if i >= length:
            break
        rail_len[r] += 1
        i += 1

    rail_text = []
    k = 0
    for r in range(rails):
        rail_text.append(list(cipher[k:k + rail_len[r]]))
        k += rail_len[r]

    result = []
    rail = 0
    direction = 1
    for _ in range(length):
        result.append(rail_text[rail].pop(0))
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    return ''.join(result)