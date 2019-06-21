# -- coding: utf-8 --
import sys, os

ll = sys.argv[1:]

trg_dir = os.path.dirname(ll[0])

trg_name = '\\' + '-'.join(ll[0].split(os.sep)[-4:][:3]).replace('week', 'w').replace('day', 'd')
print(trg_name)

cmd = 'ffmpeg -i ' + ' -i '.join(ll) + ' -c:a copy -c:v copy ' + trg_dir + trg_name + '.mp4 ' 
os.system(cmd)

# trg_name = '\\out'

# print(trg_dir)

# print(ll)

# path_list = your_path.split(os.sep)
# print (ll[0].split(os.sep)[-4:][:3])


# cmd = 'ffmpeg -loglevel panic -i ' + ' -i '.join(ll) + ' -c:a copy -c:v copy ' + trg_dir + trg_name + '.mp4 > ' + trg_dir + trg_name + '.log '




input('Press ENTER key ... ')

# self.global_log.write(f'\n cmd is '+cmd)
# self.global_log.flush()
