from gitManager import *
import os

import unittest

project_dir = os.getcwd()

class doTests(unittest.TestCase):
	def test_git_pull(self):
		result = git_pull(project_dir)
		self.failUnless(result == 'OK')
	def test_git_checkout(self):
		branch = "pybuilder"
		result = git_checkout(project_dir, branch)
		self.failUnless(result == 'OK')
	def test_git_check_for_updates(self):
		result = git_check_for_updates(project_dir)
		#self.failUnless(result is None)
	def test_git_check_for_uncommitted_changes(self):
		git_check_for_uncommitted_changes(project_dir)