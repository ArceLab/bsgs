# -*- coding: utf-8 -*-
"""

@author: iceland
"""
import sys
import gmp_ec as ec
import os
import math

G = ec.G

def create_table(start_value, end_value):
    # create a table:  f(x) => G * x
    P = ec.Scalar_Multiplication(start_value, G)
    baby_steps = []
    for _ in range(start_value, end_value):
        baby_steps.append(P.x)
        P = ec.Point_Addition(P, G)
    baby_steps.append(P.x)              # last element
    return baby_steps


if len(sys.argv) > 3 or len(sys.argv) < 3:
    print('[+] Program Usage.... ')
    print(f'{sys.argv[0]} <bP items> <output filename>\n')
    print(
        f'Example to create a File with 20 million items:\n{sys.argv[0]} 20000000 bPfile.bin'
    )

    sys.exit()


total = int(sys.argv[1])
bs_file = sys.argv[2]
with open(bs_file, 'wb') as out:
    chunk = 1000000
    print('\n[+] Program Running please wait...')

    # =============================================================================
    seq = range(1, total+1)
    parts_list = [seq[i * chunk:(i * chunk) + chunk] for i in range(math.ceil(len(seq) / chunk))]

    print(f'[+] Created {len(parts_list)} Chunks ...')
    for k, piece in enumerate(parts_list, start=1):
        print(f'[+] Working on Chunk {k} ...', end='\r')
        start_value = min(piece)
        end_value = max(piece)
        baby_steps = create_table(start_value, end_value)
        for line in baby_steps:
            out.write(bytes.fromhex(hex(line)[2:].zfill(64)))
        out.flush()
        os.fsync(out.fileno())
print('[+] File created successfully\n')