#!/usr/bin/env python

import requests
import json
import sys

sys.path.append('../')
from secrets import git_user, git_repo, git_branch, config_file

def get_github_json(git_user,git_repo,git_branch,config_file):

	raw_config = requests.get('https://raw.githubusercontent.com/' + git_user + '/' + git_repo + '/' + git_branch + '/data/' + config_file)

	json_config = raw_config.text

	return json_config

def validate_json(git_user,git_repo,git_branch,config_file):

	response = requests.get('https://api.github.com/repos/' + git_user + '/' + git_repo + '/contents/data/' + config_file + '?ref=' + git_branch, auth=('kyokeefesally','Cese85!@#'))

	json_data = json.loads(response.text)

	file_name = json_data["name"]
		
	if '.json' in file_name:
		#print('true')
		return 'true'

	else:
		#print('false')
		return 'false'

#validate_json(git_user, git_repo, git_branch, config_file)