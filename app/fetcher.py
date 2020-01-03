import requests
import json, time, datetime
import math
from app import db
from app.models import Post


def get_post(post_title):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))

	db_titles = [post.title.replace(" ", "-") for post in Post.query.all()]

	if post_title not in db_titles:
		return redirect(url_for('home'))

	post_title = post_title.replace("-", " ")
	post = Post.query.filter_by(title=post_title).first()

	print('GOOD!')
	return post


def github_fetcher():

	# Get token from .txt file
	with open('tokens.txt', 'r') as f:
		token = f.readline().strip()

	url = 'https://api.github.com/users/hellomusa/repos'
	github_token = token
	params = {'access_token': github_token}

	response = requests.get(url, params=params)

	repo_names = []
	commits = {}

	if response:
		data = json.loads(response.content)

		# Get each repository name
		for repo in data:
			repo_names.append(repo['full_name'][10:])

		# Get each commit time for repos in repo list
		for repo_name in repo_names:
			commit_url = f'https://api.github.com/repos/hellomusa/{repo_name}/commits/master'
			response = requests.get(commit_url, params=params)

			if response:
				data = json.loads(response.content)
				commit_date = data['commit']['author']['date']
				commit_date_dt = datetime.datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
				commits[repo_name] = commit_date_dt
			else:
				print('Something went wrong.')

		# Compare current time with latest commit time, return the difference

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

	else:
		print('Something went wrong.')


def blog_fetcher():
	latest_post = Post.query.all()[-1]
	post_title = latest_post.title

	return post_title
