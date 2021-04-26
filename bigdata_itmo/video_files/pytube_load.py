import argparse
import os
import os.path as osp

import requests
import tqdm
from pytube import YouTube

from bigdata_itmo.config import download_config, system_config


def create_parser():
    parser = argparse.ArgumentParser("Download frames from stream")

    parser.add_argument(
        "--channel_id",
        default="UC16niRr50-MSBwiO3YDb3RA",
        help="Channel ID from YouTube [default = BBC News channel ID]",
    )
    parser.add_argument(
        "--output_folder",
        default=osp.join(system_config.data_dir, "raw", "pytube_data"),
        help="Filename to write stream",
    )

    args = parser.parse_args()
    return args


def main(args):

    video_list = requests.get(
        f"https://www.googleapis.com/youtube/v3/search?key={download_config.api_key}"
        + f"&channelId={args.channel_id}&part=snippet,id&order=date&maxResults=20"
    ).json()

    os.makedirs(osp.dirname(args.output_folder), exist_ok=True)

    for video_item in tqdm.tqdm(video_list["items"], desc="Download items"):

        item_kind = video_item["id"]["kind"]

        if item_kind == "youtube#video":

            video_id = video_item["id"]["videoId"]
            # TODO: save this information along with video content

            # video_name = video_item["snippet"]["title"]
            # published_at = video_item["snippet"]["publishedAt"]
            # tumbnail_url = video_item["snippet"]["thumbnails"]["high"]

            yt = YouTube(f"'http://youtube.com/watch?v={video_id}'")
            video = yt.streams.filter(file_extension="mp4").first()
            video.download(output_path=args.output_folder)


if __name__ == "__main__":
    args = create_parser()
    main(args)
