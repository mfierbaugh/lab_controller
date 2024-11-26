#! /usr/bin/env python3
#
# lab_controller is a simple python script used to sync the lab playbooks from the gitlab server
# the labs.yml file contains the working directory and the remote repo for each lab
# Author - Marty Fierbaugh (mfierbau@cisco.com)
#
#
# import libraries 
import git
import yaml
from pathlib import Path
from tqdm import tqdm
from time import sleep

config_file = 'labs.yml'

def is_valid_directory(filename):
    p = Path(filename)
    return p.exists() and p.is_dir()

def clone_playbook(pb_dir, repo):
    git.Repo.clone_from(repo, pb_dir)
    for i in tqdm(range(0, 100), total = 100, 
              desc ="Cloning " + pb_dir): 
        sleep(.01)

def pull_playbook(pb_dir, repo):
    git.cmd.Git(working_dir=pb_dir).pull(repo, 'main')
    for i in tqdm(range(0, 100), total = 100, 
              desc ="Updating " + pb_dir): 
        sleep(.01)

for playbook_dir,repo_url in yaml.load(open(config_file), yaml.FullLoader)['labs'].items():
    if is_valid_directory(playbook_dir):
        print ("\nExisting playbook found. Updating from repo..." + playbook_dir)
        pull_playbook(playbook_dir, repo_url)
    else:
        print ("\nFound new playbook in yaml file. Cloning: " + playbook_dir)
        clone_playbook(playbook_dir, repo_url)
