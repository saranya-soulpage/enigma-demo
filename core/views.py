from django.shortcuts import render, HttpResponse

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
import requests
import json
import pprint

from rest_framework import views


@method_decorator(login_required(login_url="/api/login/"), name="dispatch")
class ReposRequest(views.APIView):
    def get(self, request):
        user_data = SocialAccount.objects.get(user=request.user).extra_data
        repo_request = requests.get(
            "https://api.github.com/users/{}/repos?page=0&per_page=200".format(
                str(user_data["login"])
            )
        )
        repo_request_json = json.loads(repo_request.content)
        repos = []
        for i in repo_request_json:
            repos.append(i["name"])
        print(repos)
        context = repos
        return render(request, "index.html", {"context": context})


@login_required
def repo_info_view(request, repo_name):
    user_data = SocialAccount.objects.get(user=request.user).extra_data

    """
    Commit Names and Message Fetch from User.
    """
    # /repos/:owner/:repo/collaborators
    repo_info_commits = requests.get(
        "https://api.github.com/repos/{}/{}/commits?page=0&per_page=200".format(
            str(user_data["login"]), repo_name
        )
    )
    repo_info_commits_json = json.loads(repo_info_commits.content)
    commits = []
    for i in repo_info_commits_json:
        commits.append([i["commit"]["author"], i["commit"]["message"]])

    """
    Commiters and Collab Info
    """
    # /repos/:owner/:repo/commits
    repo_commits = requests.get(
        "https://api.github.com/repos/{}/{}/commits?page=0&per_page=200".format(
            str(user_data["login"]), repo_name
        )
    )
    repo_commits_json = json.loads(repo_commits.content)
    collab = []
    sha = []
    print(repo_commits_json)
    for i in repo_commits_json:
        collab.append(i["commit"]["committer"]["name"])
        sha.append(i["sha"])

    collab = set(collab)
    print(sha)
    # Commit Additions and Deletions
    # GET /repos/:owner/:repo/commits/:sha
    stats = []
    print(len(sha))

    for i in range(0, len(sha)):
        print(i)
        print("#########")
        print(sha[i])
        commit_add_del = requests.get(
            "https://api.github.com/repos/{}/{}/commits/{}".format(
                str(user_data["login"]), repo_name, sha[i]
            )
        )
        commit_add_del_json = json.loads(commit_add_del.content)
        stats.append(commit_add_del_json["stats"])
    print(stats)

    """
    Languages Used for Repos
    """
    # /repos/:owner/:repo/languages
    repo_info_languages = requests.get(
        "https://api.github.com/repos/{}/{}/languages".format(
            str(user_data["login"]), repo_name
        )
    )
    repo_info_languages = json.loads(repo_info_languages.content)

    # /repos/:owner/:repo/commits/:sha
    # repo_diff = requests.get('https://api.github.com/repos/{}/{}/{}'.format(str(user_data['login']),repo_name))

    context = {
        "repo_name": repo_name,
        "repo_info_languages": repo_info_languages,
        "repo_info_commits_json": repo_info_commits_json,
        "commits": commits,
        "repo_commits_json": repo_commits_json,
        "collab": collab,
    }
    return render(request, "repo_info.html", context)


@login_required
def commits(request):
    user_data = SocialAccount.objects.get(user=request.user).extra_data
    pass
