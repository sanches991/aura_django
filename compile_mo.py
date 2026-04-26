import struct


def unescape(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            c = s[i + 1]
            if c == 'n':
                result.append('\n')
            elif c == 't':
                result.append('\t')
            elif c == 'r':
                result.append('\r')
            elif c == '\\':
                result.append('\\')
            else:
                result.append(s[i])
                result.append(c)
            i += 2
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)


def compile_po(po_path, mo_path):
    catalog = {}
    msgid = None
    msgstr = None
    in_msgid = False
    in_msgstr = False

    with open(po_path, encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.rstrip('\n').rstrip('\r')
            if line.startswith('msgid '):
                if msgid is not None and msgstr is not None:
                    catalog[msgid] = msgstr
                rest = line[6:].strip()
                msgid = unescape(rest[1:-1]) if rest.startswith('"') else ''
                in_msgid = True
                in_msgstr = False
            elif line.startswith('msgstr '):
                rest = line[7:].strip()
                msgstr = unescape(rest[1:-1]) if rest.startswith('"') else ''
                in_msgid = False
                in_msgstr = True
            elif line.startswith('"'):
                inner = unescape(line[1:-1])
                if in_msgid and msgid is not None:
                    msgid += inner
                elif in_msgstr and msgstr is not None:
                    msgstr += inner

    if msgid is not None and msgstr is not None:
        catalog[msgid] = msgstr

    if '' not in catalog:
        catalog[''] = 'Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n'

    # empty string (header) must sort first
    ids = sorted(catalog.keys(), key=lambda k: (k != '', k))

    offsets = []
    ids_data = b''
    strs_data = b''
    for mid in ids:
        mstr = catalog[mid]
        mid_b = mid.encode('utf-8')
        mstr_b = mstr.encode('utf-8')
        offsets.append((len(mid_b), len(ids_data), len(mstr_b), len(strs_data)))
        ids_data += mid_b + b'\x00'
        strs_data += mstr_b + b'\x00'

    n = len(ids)
    keystart = 7 * 4 + 16 * n
    valuestart = keystart + len(ids_data)
    koffsets = []
    voffsets = []
    for l1, o1, l2, o2 in offsets:
        koffsets += [l1, keystart + o1]
        voffsets += [l2, valuestart + o2]

    with open(mo_path, 'wb') as f:
        f.write(struct.pack('<I', 0x950412de))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', n))
        f.write(struct.pack('<I', 7 * 4))
        f.write(struct.pack('<I', 7 * 4 + 8 * n))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 0))
        for o in koffsets:
            f.write(struct.pack('<I', o))
        for o in voffsets:
            f.write(struct.pack('<I', o))
        f.write(ids_data)
        f.write(strs_data)


compile_po('locale/en/LC_MESSAGES/django.po', 'locale/en/LC_MESSAGES/django.mo')
compile_po('locale/ky/LC_MESSAGES/django.po', 'locale/ky/LC_MESSAGES/django.mo')
print('OK: en and ky .mo files compiled')
