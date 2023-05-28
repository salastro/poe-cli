# POE-CLI
Command line interface for Poe.

[![Upload Python Package](https://github.com/salastro/poe-cli/actions/workflows/python-publish.yml/badge.svg)](https://github.com/salastro/poe-cli/actions/workflows/python-publish.yml)

https://github.com/salastro/poe-cli/assets/63563250/d4a2333c-0707-410a-818e-3fb0a644a2c4


## Installation
### From pip
```
pip install poe-cli
```
### From source
```
git clone https://github.com/salastro/poe-cli.git
cd poe-cli
pip install -e .
```

## Usage
Read how to get [Poe token](https://github.com/ading2210/poe-api#finding-your-token).
```bash
poe -h # show help
poe -t TOKEN -l  # list bots
poe -t TOKEN -m "Who are you?" # use default bot (ChatGPT).
poe -t TOKEN -b beaver -m "Who are you?" # use GPT-4
```


