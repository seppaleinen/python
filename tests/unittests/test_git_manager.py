#!/usr/bin/python


import unittest, os, mock, sys
from python_dir.git_manager import ( 
    git_pull, 
    git_checkout, 
    git_check_for_updates, 
    git_check_for_uncommitted_changes, 
    GitCommandError
    )
from StringIO import StringIO

project_dir = os.getcwd()


class doTests(unittest.TestCase):
    @mock.patch('python_dir.git_manager.Repo')
    def test_git_pull(self, mocked):
        mocked.return_value = mocked
        result = git_pull(project_dir)
        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with('pull')
        self.failUnless(result == 'OK')

    @mock.patch('python_dir.git_manager.Repo')
    def test_git_pull_pass_error(self, mocked):
        mocked.return_value = mocked
        mocked.git._call_process.side_effect = GitCommandError('Error', 'Message')
        try:
            git_pull(project_dir)
        except GitCommandError, e:
            self.assertEquals( "Error", e.msg )
        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with("pull")

    @mock.patch('python_dir.git_manager.Repo')
    def test_git_checkout(self, mocked):
        mocked.return_value = mocked
        branch = "master"
        result = git_checkout(project_dir, branch)
        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with('checkout', branch)
        self.failUnless(result == 'OK')

    @mock.patch('python_dir.git_manager.Repo')
    def test_git_checkout_pass_error(self, mocked):
        mocked.return_value = mocked
        mocked.git._call_process.side_effect = GitCommandError('Error', 'Message')
        branch = "master"
        try:
            git_checkout(project_dir, branch)
        except GitCommandError, e:
            self.assertEquals( "Error", e.msg )
        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with('checkout', branch)

    @mock.patch('python_dir.git_manager.Repo')
    def test_git_check_for_updates(self, mocked):
        mocked.return_value = mocked
        mocked.git._call_process.return_value = "git result \n master pushes to master (local out of date)"
        result = git_check_for_updates(project_dir)
        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with('remote', 'show', 'origin')
        self.failIf(result is [])
        self.failUnless('master' in result)

    @mock.patch('python_dir.git_manager.Repo')
    def test_git_check_for_updates_no_result(self, mocked):
        mocked.return_value = mocked
        result = git_check_for_updates(project_dir)
        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with('remote', 'show', 'origin')
        self.assertEqual(result, [])

    @mock.patch('python_dir.git_manager.Repo')
    def test_git_check_for_uncommitted_changes(self, mocked):
        mocked.return_value = mocked
        mocked.git._call_process.return_value = "Changes not staged for commit"
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            result = git_check_for_uncommitted_changes(project_dir)
            output = out.getvalue().strip()
            self.assertTrue('has uncommitted changes' in output)
        finally:
            sys.stdout = saved_stdout

        mocked.assert_called_with(project_dir)
        mocked.git._call_process.assert_called_with('status')    


if __name__ == '__main__':
    unittest.main()