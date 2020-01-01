import requests
import json, time, datetime
import math

def github_fetcher():
	url = 'https://api.github.com/users/hellomusa/repos'
	github_token = '068f3c621b92dadec530fa76b3eaa7d0a9811ab2'
	params = {'access_token': github_token}

	response = requests.get(url, params=params)

	repo_names = []
	commits = {}

	if response:
		data = json.loads(response.content)

	# KEEP LOOPING
	while True:
		data = json.loads(response.content)
		for repo in data:
			repo_names.append(repo['full_name'][10:])

		for repo_name in repo_names:
			commit_url = f'https://api.github.com/repos/hellomusa/{repo_name}/commits/master'
			response = requests.get(commit_url, params=params)

			if response:
				data = json.loads(response.content)
				commit_date = data['commit']['author']['date']
				commit_date_dt = datetime.datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
				commits[repo_name] = commit_date_dt

			# STOP LOOP
			else:
				print('Something went wrong.')
				break

		commit_times = [commits[repo] for repo in commits]
		newest_commit_time = max(commit_times)

		newest_commit_repo = ''
		for repo in commits:
			if commits[repo] == newest_commit_time:
				newest_commit_repo = repo

		current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
		current_time_dt = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

		difference = current_time_dt - newest_commit_time
		minutes = difference.seconds//60
		hours = minutes//60
		minutes -= 60*hours

		return_list = [newest_commit_repo]

		if (60*hours + minutes) < 60:
			return_list.append(f'{minutes} minutes')
		else:
			return_list.append(f'{math.ceil(hours)} hours')

		return return_list

	# STOP LOOP
	else:
		print('Something went wrong.')


