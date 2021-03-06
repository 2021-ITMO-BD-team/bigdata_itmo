import argparse
import glob
import json
import os
import os.path as osp
import re

import pandas as pd
import tqdm
from pytube.helpers import safe_filename

from bigdata_itmo.config import system_config


def create_parser():
    parser = argparse.ArgumentParser(("Gather meta information from raw json files"))
    parser.add_argument("--dataset", default="BBC_News", help="Name of the dataset")

    args = parser.parse_args()
    args.json_dir = osp.join(system_config.data_dir, "raw", "json", args.dataset)
    args.video_dir = osp.join(system_config.data_dir, "raw", "pytube_data", args.dataset)
    args.audio_dir = osp.join(system_config.data_dir, "raw", "mp3_data", args.dataset)
    args.out_dir = osp.join(system_config.data_dir, "processed", args.dataset)

    return args


def read_one_json(json_path):
    with open(json_path) as fin:
        raw_dict = json.load(fin)

    video_item = raw_dict["items"][0]
    out_dict = {
        "id": video_item["id"],
        "publishedAt": video_item["snippet"]["publishedAt"],
        "categoryId": video_item["snippet"]["categoryId"],
        "title": video_item["snippet"]["title"],
        "description": video_item["snippet"]["description"],
        "channelId": video_item["snippet"]["channelId"],
        "channelTitle": video_item["snippet"]["channelTitle"],
        "tags": video_item["snippet"].get("tags", []),
        "query": raw_dict.get("query"),
    }

    return out_dict


def clean_description(
    in_str, pat=re.compile("((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)")
):  # noqa W605
    # Regex from https://macxima.medium.com/python-extracting-urls-from-strings-21dc82e2142b

    lines = list(in_str.split("\n"))

    # Delete strings containing link
    lines = list(filter(lambda x: not ((re.search(pat, x) is not None) and (len(x) < 100)), lines))
    lines = list(filter(lambda x: "youtube" not in x, lines))

    return "\n".join(lines).strip()


def update_one_json(prep_json, video_dir, audio_dir):
    prep_json["title_clean"] = safe_filename(prep_json["title"])
    prep_json["description_clean"] = clean_description(prep_json["description"])

    video_path = osp.join(video_dir, f"{safe_filename(prep_json['title'])}.mp4")
    audio_path = osp.join(audio_dir, f"{safe_filename(prep_json['title'])}.mp3")
    try:
        prep_json["theme"] = CHANNEL_TITLE_2_THEME[prep_json["channelTitle"]]
    except KeyError:
        try:
            prep_json["theme"] = QUERY_2_THEME[prep_json["query"]]
        except KeyError:
            print(
                f"Theme cannot be extracted from channel title {prep_json['channelTitle']} "
                f"or query {prep_json.get('query')}"
            )

    for fpath, fpath_name in zip([video_path, audio_path], ["video_path", "audio_path"]):
        prep_json[fpath_name] = "/".join(list(fpath.split("/"))[-3:])
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


CHANNEL_TITLE_2_THEME = {
    "Bloomberg Politics": "politics",
    "Bloomberg Technology": "technology",
    "NBC Sports": "sports",
    "Crime News": "violence",
    "Met Office - Weather": "weather",
}
QUERY_2_THEME = {"tv commercials english": "commercials", "tv advertisement": "commercials"}


if __name__ == "__main__":
    args = create_parser()
    markup = gather_meta(args)

    os.makedirs(args.out_dir, exist_ok=True)
    markup.to_csv(osp.join(args.out_dir, "all_df.csv"), index=False)
