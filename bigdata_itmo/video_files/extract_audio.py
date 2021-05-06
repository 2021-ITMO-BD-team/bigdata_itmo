import argparse
import glob
import os
import os.path as osp

import moviepy.editor as mp
import tqdm

from bigdata_itmo.config import system_config


def create_parser():
    parser = argparse.ArgumentParser("Convert video to audio")

    parser.add_argument(
        "--input_path",
        default=osp.join(system_config.data_dir, "raw", "pytube_data", "BBC_News"),
        help="File or folder with video files to extract audio",
    )
    parser.add_argument(
        "--output_folder",
        default=osp.join(system_config.data_dir, "raw", "audio_data", "BBC_News"),
        help="Folder to store audio files",
    )
    parser.add_argument("--audio_format", default="wav", help="Format of output audio file")
    parser.add_argument("--rewrite", action="store_true", help="Whether to rewrite existing audio tracks")

    args = parser.parse_args()
    return args


def extract_one_file(fpath, output_folder, format="wav", rewrite=False):
    os.makedirs(output_folder, exist_ok=True)

    out_fpath = osp.join(output_folder, f"{osp.splitext(osp.basename(fpath))[0]}.{format}")
    if not osp.exists(out_fpath) or rewrite:
        my_clip = mp.VideoFileClip(fpath)
        my_clip.audio.write_audiofile(out_fpath)


if __name__ == "__main__":
    args = create_parser()

    if osp.isfile(args.input_path):
        extract_one_file(args.input_path, args.output_folder)

    else:
        file_list = glob.glob(osp.join(args.input_path, "*"))
        for fpath in tqdm.tqdm(file_list, desc="Extracting audios"):
            extract_one_file(fpath, args.output_folder, format=args.audio_format, rewrite=args.rewrite)
