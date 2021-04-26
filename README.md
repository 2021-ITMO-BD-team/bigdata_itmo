# Course project on ITMO Big Data course

Please work in branches, then make pull-request into master, or the master will become a huge mess.

# Sorta development guide

## 1. Install dependencies
```bash
pip install -r requirements/torch.txt
pip install -r requirements/prod.txt
```

If you need development requirements - install them
```
pip install -r requirements/dev.txt
```

## 2. Install package from current folder in editable mode
```bash
pip install -e .
```

## 3. If you want to have autostyle - install [pre-commit](https://pre-commit.com/) and run
```bash
pre-commit install
```

Now hooks will apply to your code within folder `bigdata_itmo` each time you make `git commit`.
