import os
import shutil
# from pydub import AudioSegment
import subprocess
from subprocess import Popen, PIPE
import glob

def src_dst(src):
    print("SOURCE is: {}".format(src))
    if not os.path.isdir(os.path.join(src+"_wav")):
        os.mkdir(src+"_wav")
    else:
        os.system("rm -rf {}".format(src+"_wav"))
        os.mkdir(src+"_wav")

    src_list = [src + "/" + f for f in os.listdir(src)]
    # src_list = ["{}/{}".format(src, f) for f in os.listdir(src)]
    src_list = [src + "/" + f for f in os.listdir(src)]
    #   dst_list = [src + "/" + str(i) + ".wav"  for i in range(len(os.listdir(src)))]
    dst_list = [src+"_wav" + "/{}.wav".format(i) for i, _ in enumerate(os.listdir(src))]
    return src_list, dst_list
  
# subprocess_cmd('echo a; echo b')
def mp3_to_wav_parallel(src_list, dst_list):
  
  # f_list = glob.glob('./*bz2')
  cmds_list = [['ffmpeg', '-i', src,
          dst] for src, dst in zip(src_list, dst_list)]
  
  procs_list = [Popen(cmd, stdout=PIPE, stderr=PIPE) for cmd in cmds_list]
  for proc in procs_list:
    proc.wait()

import sys
def convert(src):
#   src = "src
  if not os.path.isdir(src):
      print("Please provide directory path containing mp3 audio!")
      print("EXITING...")
      sys.exit(0)

  src_list, dst_list = src_dst(src)
  print("total source files: ", len(src_list))
  mp3_to_wav_parallel(src_list, dst_list)
  print("conversion completed: [mp3 to wav]")
#   print("removing: {}".format(src))
#   shutil.rmtree(src)
#   print("Removed successfully")
#   return dst_list