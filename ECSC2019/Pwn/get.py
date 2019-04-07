#!/usr/bin/python
from base64 import b64decode as d

v = ['SfBsOxPvNMDyNAhRSgsG',
 'VjYOkGDgkkXgULZUkCeh',
 'OYgUClVWJQAvOtMfBSPg',
 'UgGADoBNyIpiGNyfyuet',
 'RoSgSYiwNwAcSgnPOsMB',
 '4sGvkBZfEqfHEgvkUeUL',
 'ullIdbFSSDZrKCSAJIUz',
 'FPVZxzrNHXShDeRb1GXd',
 'RNpVNeyZRVHTOwZuNdQq',
 'VALsFVveUNPuUoDWlpXu',
 'VyNbOyZjyGBwQUiUxeSe',
 'xO2rYv2pXL3UWoDvBTDQ',
 'qCOaRDOZicRnhDSacIgc',
 'bGUTstlyoElXoIVVghRO',
 'MmNRiDVggENtBjNHvw>g',
 'MC2BCa1DjAyglyzgwQ>v',
 'LeNdcAOGPROrjrOUSiWC',
 'YQEvXfUjbEERJDEjLZcS',
 'baCAeWZGrnROqkJKchEi',
 'oLDKgG6TxDzrQu6amIlZ']

flag = ''
for i in range(96):
    flag += chr(ord(v[i % 20][2 * (i // 10)]) - 1)

print(d(flag).decode())
