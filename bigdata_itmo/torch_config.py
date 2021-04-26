import os

import torch


class TorchConfig:

    device = (
        torch.device("cpu")
        if not torch.cuda.is_available() or os.getenv("FORCE_CPU", "0") == "1"
        else torch.device("cuda")
    )


torch_config = TorchConfig()
