import argparse
import glob
import json
import os
import os.path as osp

import pandas as pd
import tqdm
from pytube.helpers import safe_filename

from bigdata_itmo.config import system_config


def create_parser():
    parser = argparse.ArgumentParser(("Gather meta information from raw json files"))
    parser.add_argument(
        "--json_dir",
        default=osp.join(system_config.data_dir, "raw", "json", "BBC_News"),
        help="Path to folder with json files",
    )
    parser.add_argument(
        "--video_dir",
        default=osp.join(system_config.data_dir, "raw", "pytube_data", "BBC_News"),
        help="Path to folder with videos",
    )
    parser.add_argument(
        "--audio_dir",
        default=osp.join(system_config.data_dir, "raw", "audio_data", "BBC_News"),
        help="Path to folder with audios",
    )
    parser.add_argument(
        "--out_dir",
        default=osp.join(system_config.data_dir, "processed", "BBC_News"),
        help="Path to folder to save meta data",
    )
    args = parser.parse_args()
    return args


def read_one_json(json_path):
    with open(json_path) as fin:
        raw_dict = json.load(fin)

    video_item = raw_dict["items"][0]
    out_dict = {
        "id": video_item["id"],
        "title": video_item["snippet"]["title"],
        "description": video_item["snippet"]["description"],
        "publishedAt": video_item["snippet"]["publishedAt"],
        "channelId": video_item["snippet"]["channelId"],
        "channelTitle": video_item["snippet"]["channelTitle"],
        "tags": video_item["snippet"].get("tags", []),
        "categoryId": video_item["snippet"]["categoryId"],
    }

    return out_dict


def update_one_json(prep_json, video_dir, audio_dir):
    video_path = osp.join(video_dir, f"{safe_filename(prep_json['title'])}.mp4")
    audio_path = osp.join(audio_dir, f"{safe_filename(prep_json['title'])}.wav")

    for fpath, fpath_name in zip([video_path, audio_path], ["video_path", "audio_path"]):
        prep_json[fpath_name] = fpath[len(system_config.data_dir) + 1 :]
        prep_json[f"{fpath_name}_exists"] = osp.exists(fpath)
        if not osp.exists(fpath):
            print(f"Path {fpath} doesn't exist")

    return prep_json


def gather_meta(args):

    json_flist = sorted(glob.glob(osp.join(args.json_dir, "*.json")))
    data = []
    for json_fpath in tqdm.tqdm(json_flist, desc="Gathering markup"):
        prep_json = read_one_json(json_fpath)
        prep_json = update_one_json(prep_json, args.video_dir, args.audio_dir)
        data.append(prep_json)

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    args = create_parser()
    markup = gather_meta(args)

    os.makedirs(args.out_dir, exist_ok=True)
    markup.to_csv(osp.join(args.out_dir, "all_df.csv"), index=False)
