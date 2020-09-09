from github import Github
#https://pygithub.readthedocs.io/en/latest/examples.html

import urllib3
# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GitHubAPI():
    def __init__(self,git_api, token):
        self.status = True
        self.git_api = git_api
        try:
            self.g = Github(base_url=self.git_api, login_or_token=token, verify=False)
        except Exception as e:
            print(str(e),'git_api = {0}'.format(self.git_api))
            self.status = False
        
    def set_repo(self, repo_url):
        try:
            repo_part = repo_url.split('/')
            self.repo_name = repo_part[-2] + '/' + repo_part[-1].replace(".git","")
            self.repo = self.g.get_repo(self.repo_name)
        except Exception as e:
            print(str(e),'repo_name = {0}'.format(self.repo_name))
            self.status = False
        finally:
            return self.status

    def pull_request(self, title, body, head, base='master'):
        pr = None
        try:
            pr = self.repo.create_pull(
                title=title, body=body, head=head, base=base)
        except Exception as e:
            print(str(e),'repo_name = {0}'.format(self.repo_name))
            self.status = False
        finally:
            return pr, self.status        
    
    def list_branches(self):
        return list(self.repo.get_branches())
    
    def create_story(self,title, body=None, assignee=None, milestone=None, labels=None):
        #title format: jira number --- title
        if title != '' and body != '':
            try:
                issue = self.repo.create_issue(title = title,body = body)
            except Exception as e:
                print(str(e),'repo_name = {0}'.format(self.repo_name))
                self.status = False
            finally:
                return issue, self.status
        else:
            return None, self.status
