# POE-CLI
Command line interface for Poe.

## Installation
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


