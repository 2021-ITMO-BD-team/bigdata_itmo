import os
import os.path as osp

CURRENT_PATH = osp.dirname(osp.realpath(__file__))


class DownloadConfig:

    api_key = os.getenv("GOOGLE_API_KEY")


class SystemConfig:

    root_dir = osp.realpath(osp.join(CURRENT_PATH, ".."))
    data_dir = osp.join(root_dir, "data")


download_config = DownloadConfig()
system_config = SystemConfig()
