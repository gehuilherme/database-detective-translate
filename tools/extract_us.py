#!/usr/bin/env python3
"""Extract the #US (user strings / literals) heap from a .NET assembly (PE/CLI)."""
import struct, sys, json, re

def read_compressed_uint(b, i):
    b0 = b[i]
    if b0 & 0x80 == 0:
        return b0, i+1
    if b0 & 0xC0 == 0x80:
        return ((b0 & 0x3F) << 8) | b[i+1], i+2
    return ((b0 & 0x1F) << 24) | (b[i+1] << 16) | (b[i+2] << 8) | b[i+3], i+4

def parse(path):
    d = open(path, 'rb').read()
    # DOS header -> PE offset
    pe = struct.unpack_from('<I', d, 0x3C)[0]
    assert d[pe:pe+4] == b'PE\x00\x00', "not PE"
    coff = pe + 4
    num_sections = struct.unpack_from('<H', d, coff+2)[0]
    opt_size = struct.unpack_from('<H', d, coff+16)[0]
    opt = coff + 20
    magic = struct.unpack_from('<H', d, opt)[0]
    is64 = magic == 0x20b
    # data directories start
    dd_off = opt + (112 if is64 else 96)
    # index 14 = CLI header
    cli_rva, cli_size = struct.unpack_from('<II', d, dd_off + 14*8)
    # sections
    sec_off = opt + opt_size
    sections = []
    for s in range(num_sections):
        base = sec_off + s*40
        name = d[base:base+8].rstrip(b'\x00')
        vsize, vaddr, rawsize, rawptr = struct.unpack_from('<IIII', d, base+8)
        sections.append((vaddr, vsize, rawptr, rawsize))
    def rva2off(rva):
        for vaddr, vsize, rawptr, rawsize in sections:
            if vaddr <= rva < vaddr + max(vsize, rawsize):
                return rawptr + (rva - vaddr)
        raise ValueError("rva not found %x" % rva)
    cli_off = rva2off(cli_rva)
    meta_rva, meta_size = struct.unpack_from('<II', d, cli_off + 8)
    m = rva2off(meta_rva)
    assert d[m:m+4] == b'BSJB', "no metadata root"
    ver_len = struct.unpack_from('<I', d, m+12)[0]
    p = m + 16 + ver_len
    p += 2  # flags
    nstreams = struct.unpack_from('<H', d, p)[0]; p += 2
    streams = {}
    for _ in range(nstreams):
        soff, ssize = struct.unpack_from('<II', d, p)[0:2];
        soff = struct.unpack_from('<I', d, p)[0]
        ssize = struct.unpack_from('<I', d, p+4)[0]
        p += 8
        # name: null-terminated, padded to 4
        end = d.index(b'\x00', p)
        name = d[p:end].decode('ascii')
        p = end + 1
        # stream-header name is padded so its total length is a multiple of 4
        if (p - m) % 4 != 0:
            p += 4 - ((p - m) % 4)
        streams[name] = (m + soff, ssize)
    if '#US' not in streams:
        return []
    us_off, us_size = streams['#US']
    b = d[us_off:us_off+us_size]
    i = 1  # first byte is 0 (empty entry)
    out = []
    while i < len(b):
        if b[i] == 0:
            i += 1; continue
        length, i2 = read_compressed_uint(b, i)
        if length == 0:
            i = i2; continue
        data = b[i2:i2+length]
        # last byte is terminal flag
        strbytes = data[:-1] if length > 0 else data
        try:
            s = strbytes.decode('utf-16-le')
        except Exception:
            s = strbytes.decode('utf-16-le', 'replace')
        out.append(s)
        i = i2 + length
    return out

if __name__ == '__main__':
    path = sys.argv[1]
    strs = parse(path)
    # dedupe preserving order
    seen = set(); uniq = []
    for s in strs:
        if s not in seen:
            seen.add(s); uniq.append(s)
    print("TOTAL literals:", len(strs), "UNIQUE:", len(uniq), file=sys.stderr)
    json.dump(uniq, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
