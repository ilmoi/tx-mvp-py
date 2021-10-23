#!/bin/bash
sudo $(command -v solana-sys-tuner) --user $(whoami) > sys-tuner.log 2>&1 &
echo system tuned!