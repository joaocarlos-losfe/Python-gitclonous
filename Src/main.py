from gitclonous import *

if __name__=="__main__":
    repos = get_all_repositories("joaocarlos-losfe")
    
    for repo in repos:
        download_repository(repo, auto_extract=True)
