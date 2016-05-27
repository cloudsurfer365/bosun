#!/usr/bin/env python

import requests
import json

def get_github_json(git_user,git_repo,config_file):

	raw_config = requests.get('https://raw.githubusercontent.com/' + git_user + '/' + git_repo + '/master/data/' + config_file)

	json_config = raw_config.text

	return json_config

def validate_json(git_user,git_repo,config_file):

	response = requests.get('https://api.github.com/repos/' + git_user + '/' + git_repo + '/contents/data/' + config_file, auth=('kyokeefesally','Cese85!@#'))

	json_data = json.loads(response.text)

	file_name = json_data["name"]
		
	if '.json' in file_name:
		return 'true'

	else:
		return 'false'

git_user = 'kyokeefesally'
git_repo = 'bosun'
config_file = 'config.json'

validate_json(git_user, git_repo, config_file)