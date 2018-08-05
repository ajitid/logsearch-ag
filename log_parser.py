import pendulum


def get_pair_close(c):
    mapping = {
        '[': ']',
        '{': '}',
        '(': ')',
    }
    return mapping[c]


def get_logging_level_index(tokens):
    possible_matches = ('SEVERE', 'DEBUG', 'ERROR', 'FATAL',
                        'INFO', 'WARN', 'WARNING', 'TRACE', 'NOTIFICATION')
    for i, token in enumerate(tokens):
        if token.upper() in possible_matches:
            return i
    return None


def get_timestamp_index(tokens):
    for i, token in enumerate(tokens):
        try:
            pendulum.parse(token)
            return i
        except pendulum.parsing.ParserError:
            pass
    return None


def generate_key_value_pairs(tokens, skip_indices=tuple()):
    kv = {}
    for i, token in enumerate(tokens):
        if i in skip_indices:
            continue
        for split_char in ('=', ':'):
            arr = token.split(split_char, 1)
            if len(arr) == 2:
                kv[arr[0].strip()] = arr[1].strip()
                continue
    return kv


if __name__ == '__main__':
    f = open('log1.log', 'r')
    l1 = f.readline().strip()
    # l2 = f.readline().strip()
    pair_open = l1[0]  # error
    pair_close = get_pair_close(pair_open)
    tokens = []
    i = 0
    while i < len(l1):
        if l1[i] == pair_open:
            j = i + 1
            new_token = ''
            inner_pair_open_count = 0
            while (l1[j] is not pair_close) or (inner_pair_open_count != 0):
                if l1[j] is pair_open:
                    inner_pair_open_count += 1
                if l1[j] is pair_close:
                    inner_pair_open_count -= 1
                new_token += l1[j]
                j += 1
            tokens.append(new_token)
            i = j + 1
        else:
            i += 1
    print(get_logging_level_index(tokens))
    print(get_timestamp_index(tokens))
    print(generate_key_value_pairs(
        tokens, skip_indices=(get_timestamp_index(tokens),)))
