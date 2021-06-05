import argparse
import datetime
import json
import os
import os.path as osp
from pprint import pprint
from urllib.error import URLError
from urllib.parse import quote

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
        "--query", default="", help="Search string for query [default = None]",
    )
    parser.add_argument("--duration", default="any", help="Video duration {any, short, medium, long} [default = any]")
    parser.add_argument(
        "--last_date",
        default=None,
        help="Earliest date before which data should be downloaded in YYYY-MM-DDTHH:MM:SSZ format",
    )
    parser.add_argument("--max_videos", type=int, default=None, help="Maximum number of videos to download")
    parser.add_argument("--dataset_name", default="BBC_News", help="Name of the folder in raw/pytube_data and raw/json")
    parser.add_argument("--update_meta", action="store_true", help="Whether to update json files with meta information")

    args = parser.parse_args()
    args.output_folder = osp.join(system_config.data_dir, "raw", "pytube_data", args.dataset_name)
    args.json_folder = osp.join(system_config.data_dir, "raw", "json", args.dataset_name)

    return args


def download_video_pack(args, video_list, exist_list, n_downloaded=0):

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
                        content = response.json()
                        if args.query:
                            content["query"] = str(args.query)

                        with open(osp.join(args.json_folder, f"{safe_filename(video_name)}.json"), "w") as fout:
                            json.dump(content, fout)
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
                n_downloaded += 1
            except URLError:
                print(
                    f"Video {video_name}, time {published_at}, url "
                    + f"http://youtube.com/watch?v={video_id} was not downloaded due to unknown service error"
                )
                continue

    return published_at, n_downloaded


def download_after(args):

    last_date = args.last_date
    os.makedirs(args.output_folder, exist_ok=True)
    os.makedirs(args.json_folder, exist_ok=True)

    n_downloaded = 0

    while True:

        if last_date is None:
            last_date = datetime.datetime.now().isoformat("T")[:20] + "Z"

        url = (
            f"https://www.googleapis.com/youtube/v3/search?key={download_config.api_key}"
            + f"&part=snippet,id&order=date&maxResults=50&publishedBefore={last_date}"
            + f"&videoDuration={args.duration}&type=video"
        )

        if len(args.channel_id) > 0:
            url += f"&channelId={args.channel_id}"
        if len(args.query) > 0:
            url += f"&q={quote(args.query)}"

        video_list = requests.get(url).json()

        if "items" not in video_list.keys():
            print(last_date)
            pprint(video_list)
            break

        video_list["items"] = list(filter(lambda x: x["id"]["kind"] == "youtube#video", video_list["items"]))

        if len(video_list["items"]) <= 1:
            print(last_date)
            pprint(video_list)
            break

        exist_list = set([osp.splitext(fname)[0] for fname in sorted(os.listdir(args.output_folder))])
        last_date, n_downloaded = download_video_pack(args, video_list, exist_list, n_downloaded)

        if (args.max_videos is not None) and (n_downloaded >= args.max_videos):
            print(last_date)
            print("Max number of videos downloaded")
            break


def main(args):
    download_after(args)


if __name__ == "__main__":
    args = create_parser()
    main(args)
