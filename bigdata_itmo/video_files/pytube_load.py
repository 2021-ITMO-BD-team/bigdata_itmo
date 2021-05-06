import argparse
import datetime
import json
import os
import os.path as osp
from pprint import pprint
from urllib.error import URLError

import requests
import tqdm
from pytube import YouTube
from pytube.helpers import safe_filename

from bigdata_itmo.config import download_config, system_config


def create_parser():
    parser = argparse.ArgumentParser("Download frames from stream")

    parser.add_argument(
        "--channel_id",
        default="UC16niRr50-MSBwiO3YDb3RA",
        help="Channel ID from YouTube [default = BBC News channel ID]",
    )
    parser.add_argument(
        "--last_date",
        default=None,
        help="Earliest date before which data should be downloaded in YYYY-MM-DDTHH:MM:SSZ format",
    )
    parser.add_argument(
        "--output_folder",
        default=osp.join(system_config.data_dir, "raw", "pytube_data", "BBC_News"),
        help="Folder to save data",
    )
    parser.add_argument(
        "--json_folder",
        default=osp.join(system_config.data_dir, "raw", "json", "BBC_News"),
        help="Folder to save json files",
    )
    parser.add_argument("--update_meta", action="store_true", help="Whether to update json files with meta information")

    args = parser.parse_args()
    return args


def download_video_pack(args, video_list, exist_list):
    for video_item in tqdm.tqdm(video_list["items"], desc="Download items"):

        item_kind = video_item["id"]["kind"]

        if item_kind == "youtube#video":

            video_id = video_item["id"]["videoId"]

            video_name = video_item["snippet"]["title"]
            published_at = video_item["snippet"]["publishedAt"]

            if args.update_meta:
                response = requests.get(
                    f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cid&id={video_id}&key={download_config.api_key}"
                )
                try:
                    if response.status_code == 200:
                        with open(osp.join(args.json_folder, f"{safe_filename(video_name)}.json"), "w") as fout:
                            json.dump(response.json(), fout)
                    else:
                        print(response.json())
                        print(published_at)
                        break
                except FileNotFoundError:
                    print(f"Meta for video {video_name} was not saved due to unknown service error")

            if video_name in exist_list:
                continue

            yt = YouTube(f"http://youtube.com/watch?v={video_id}")

            try:
                video = yt.streams.filter(file_extension="mp4").first()
                video.download(output_path=args.output_folder)
            except URLError:
                print(
                    f"Video {video_name}, time {published_at}, url "
                    + f"http://youtube.com/watch?v={video_id} was not downloaded due to unknown service error"
                )
                continue

    return published_at


def download_after(args):

    last_date = args.last_date
    os.makedirs(args.output_folder, exist_ok=True)
    os.makedirs(args.json_folder, exist_ok=True)

    while True:

        if last_date is None:
            last_date = datetime.datetime.now().isoformat("T")[:20] + "Z"

        video_list = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?key={download_config.api_key}"
            + f"&channelId={args.channel_id}&publishedBefore={last_date}&part=snippet,id&order=date&maxResults=50"
        ).json()

        if "items" not in video_list.keys():
            print(last_date)
            pprint(video_list)
            break

        video_list["items"] = list(filter(lambda x: x["id"]["kind"] == "youtube#video", video_list["items"]))

        if len(video_list["items"]) == 0:
            print(last_date)
            break

        exist_list = set([osp.splitext(fname)[0] for fname in sorted(os.listdir(args.output_folder))])
        last_date = download_video_pack(args, video_list, exist_list)


def main(args):
    download_after(args)


if __name__ == "__main__":
    args = create_parser()
    main(args)
