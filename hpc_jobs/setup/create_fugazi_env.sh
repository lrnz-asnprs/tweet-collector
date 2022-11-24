#!/bin/bash


# Run this file simply running ./create_fugazi_env.sh


# Fetch conda from the HPC to your local user
module load Anaconda3/2021.05

# init conda in the bash
conda init bash

# Go to the tweet_collector directory where files environment.yml and requirement.txt are located

# Create the fugazi environment
conda create -n fugazi environment.yml

