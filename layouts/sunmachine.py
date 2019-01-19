#!/usr/bin/env python

spacing = 0.12  # m
lines = []

for c in range(10):
    rs = [reversed(range(-13,12)), range(-13,12)][c % 2]
    for r in rs:
        # x, y, z
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                     (r*spacing, 0, c*spacing))
print '[\n' + ',\n'.join(lines) + '\n]'
