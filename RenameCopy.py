# -- coding: utf-8 --
import sys, os

src_file = sys.argv[1:][0]
src_file = ll[0]

base = os.path.basename(ll[0]).replace('.mp4', '')

s = tuple(base)
new_base = f'{s[0]}{s[1]}-{s[2]}{s[3]}-{s[5]}.mp4'
#
#
#
#
# trg_name = '\\' + '-'.join(ll[0].split(os.sep)[-4:][:3]).replace('week', 'w').replace('day', 'd')
# print(trg_name)
#
# trg_dir = os.path.dirname(ll[0])



