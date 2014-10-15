#!/usr/bin/python

from package.packagefile import get_workspace
from package.finderManager import find_all_git_dirs
from package.gitManager import git_checkout
from package.gitManager import git_check_for_updates
from package.gitManager import git_pull
from package.gitManager import git_check_for_uncommitted_changes
from package.compilingManager import CompilingManager
from package.mavenManager import MavenManager


class Menu():
    def __init__(self):
        loop = True
        while loop:
            print('-----------------------------------------')
            print('What would you like to do?: enter empty to exit')
            print('1: Check which gitrepos needs updating')
            print('2: Update, build and deploy all outdated gitrepos')
            print('3: Check for uncommitted changes')
            user_input = raw_input('')
            if user_input == '1':
                self.check_git_repos()
            elif user_input == '2':
                self.update_git_repos()
            elif user_input == '3':
                self.check_for_uncommitted_changes()
            else:
                loop = False

    def check_git_repos(self):
        for GIT_REPO in find_all_git_dirs(get_workspace()):
            branch = git_check_for_updates(GIT_REPO)
            if branch is not None:
                print "Branch %s in %s is outdated" % (branch, GIT_REPO)

    def update_git_repos(self):
        for GIT_REPO in find_all_git_dirs(get_workspace()):
            branch = git_check_for_updates(GIT_REPO)
            if branch is not None:
                print "Branch %s in %s is outdated" % (branch, GIT_REPO)
                checkout_result = git_checkout(GIT_REPO, branch)
                pull_result = git_pull(GIT_REPO)
                if pull_result == 'OK':
                    dir_to_compile = GIT_REPO.replace('/.git', '')
                    build_file = CompilingManager(dir_to_compile).file_to_compile
                    if 'pom.xml' in build_file:
                        compile_result = MavenManager().mavify_pom_file(build_file)
                        print('Compileresult: %s' % (compile_result,))
                    if 'setup.py' in build_file:
                        print('Compile %s' % (build_file))
                    if 'build.gradle' in build_file:
                        print('Compile %s' % (build_file))
            else:
                print "All Branches in %s is updated" % (GIT_REPO)

    def check_for_uncommitted_changes(self):
        for GIT_REPO in find_all_git_dirs(get_workspace()):
            result = git_check_for_uncommitted_changes(GIT_REPO)
            if result is not None:
                print(result)