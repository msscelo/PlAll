import os
import git
import json

class PlAll:
    repoDirs = []
    messageNoPendingChanges = '''nothing to commit, working tree clean'''
    messageAlreadyUpToDate = 'Already up to date'
    gc = False

    def __init__(self, pathToConfig):
        with open(os.path.join(pathToConfig, 'configs.json'), 'r') as f:
            configData = json.load(f)
            for currentRepoDir in configData:
                self.repoDirs.append(currentRepoDir)

    def pullall(self, param):
        print('-- PlAll started --\n')
        if (param == 'gc'):
            print('-- Garbage collection on --\n')
            self.gc = True

        for dir in self.repoDirs:
            self.pullDir(dir)

        print('\n-- PlAll ended--')

    def isThisAGitRepo(self, dir):
        if not os.path.exists(os.path.join(dir, '.git')):
            return False
        return True

    def pullDir(self, baseDir):
        print("\n" + baseDir)
        if not os.path.exists(baseDir):
            print(" - This directory does not exist, it will be skipped.")
            return
        print(" - Processing.")

        gitDirectories = os.listdir(baseDir)

        if (self.isThisAGitRepo(baseDir)):
            gitDirectories = [""]

        for reposit in gitDirectories:
            currentGitDir = os.path.join(baseDir, reposit)
            if (not self.isThisAGitRepo(currentGitDir)):
                print(' -- ' + currentGitDir + ' this is not a git repo')
                continue

            gitCommand = git.cmd.Git(currentGitDir)

            if (self.gc):
                try:
                    gcResult = gitCommand.gc()
                    # TODO print gc result?
                except git.GitCommandError:
                    print('  -- ' + currentGitDir + ' gc failure')

            try:
                pullResult = gitCommand.pull()
            except git.GitCommandError:
                print('  -- ' + currentGitDir + ' failed to update')
                continue

            if (pullResult != self.messageAlreadyUpToDate):
                print('  -- ' + reposit + ' updated:')
                print(pullResult)

            gitStatus = gitCommand.status()
            if (self.messageNoPendingChanges in gitStatus):
                if (pullResult == self.messageAlreadyUpToDate):
                    print('  -- ' + reposit + ' OK')
                else:
                    print('  -- ' + reposit + ' clean')
            else:
                print('  -- ' + reposit + ' dirty:')
                print(gitStatus)
