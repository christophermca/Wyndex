import subprocess
import sys
import re

class Wyndex:
    def __init__(self):
        """
        Arguments:
            self
            Optional: list of files
        """
        self.__files = self.get_files_with_changes('HEAD^')


    @classmethod
    def lint_changes(cls):
        """ lint_changes:
        lint files --  stylus,  coffee
        checks for --  dot_only, debuggers
        """
        cls().__lint_coffee()
        cls().__lint_stylus()
        cls().__find_dot_only()
        cls().__find_debuggers()

    def run_tests(self):
        """ Runs Client, Server, Integration tests. """
        self.__run_server_tests()
        self.__run_client_tests()
        # self.__run_integration_tests()


    @classmethod
    def clean_code(cls):
        """ Runs Linter and Checks tests """
        cls().lint_changes()
        cls().run_tests()
        print '\n>> \33[32m' + 'Complete.\n' + '\33[0m'

    @staticmethod
    def get_previous_commit():
        if subprocess.call(['git', 'rev-parse', '--verify HEAD']):
            against = 'HEAD'
        else:
            against = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

        return against

    @staticmethod
    def get_files_with_changes(previous_commit):
        """ @Returns: A list of files with changes """

        get_files = subprocess.check_output([
            'git', 'diff', '--name-only',
            '--diff-filter=ACMRTUXB', previous_commit])
        files = get_files.split()

        files_dict = dict()
        coffee_files = [f for f in files if '.coffee' in f]
        stylus_files = [f for f in files if '.styl' in f]
        test_files = [f for f in files if '.test.' in f]

        files_dict['all'] = files
        files_dict['coffee'] = coffee_files
        files_dict['stylus'] = stylus_files
        files_dict['test'] = test_files

        return files_dict

    def __lint_coffee(self):
        print '> \33[36m' + 'Linting CoffeeScript...' + '\33[0m'

        for coffee_file in self.__files['coffee']:
            subprocess.call([
                'coffeelint',
                '-f', './coffeelint.json',
                coffee_file], cwd='./')

    def __lint_stylus(self):
        print '> \33[36m' + 'Linting Stylus...' + '\33[0m'

        for styl_file in self.__files['stylus']:
            subprocess.call([
                'coffeelint',
                '-f', './coffeelint.json',
                styl_file], cwd='./')

    def __find_dot_only(self):
        print '> \33[36m' + 'Searching for `.only`...' + '\33[0m'

        for test in self.__files['test']:
            with open(test) as test_file:
                for idx, line in enumerate(test_file):
                    if re.match("(it|describe|context)\.only", line) is not None:
                        print('Found `.only`' + '\33[33m #{}:\33[31m {}\33[0m \n'.format(idx, test))

    def __find_debuggers(self):
        print '> \33[36m' + 'Searching for debuggers...' + '\33[0m'

        regex = re.compile('(\.coffee|\.js)$')
        script_files = filter(regex.search, self.__files['all'])

        for script in script_files:
            with open(script):
                for idx, line in enumerate(script):
                    if re.match("debugger", line) is not None:
                        print('Found `debugger`' + '\33[33m #{}:\33[31m {}\33[0m \n'.format(idx, file))

    def __run_integration_tests(self):
        regex = re.compile('/integration/')
        integration_tests = filter(regex.search, self.__files['test'])

        if len(integration_tests) > 0:
            print '> \33[36m' + 'Running Integration Tests...' + '\33[0m'

            for test in integration_tests:
                subprocess.check_output(['mocha', test])

    def __run_server_tests(self):
        regex = re.compile('/server/')
        server_tests = filter(regex.search, self.__files['test'])

        if len(server_tests) > 0:
            print '> \33[36m' + 'Running Server Tests...' + '\33[0m'

            for test in server_tests:
                subprocess.check_output(['mocha', test])

    def __run_client_tests(self):
        regex = re.compile('/client/')
        client_files = filter(regex.search, self.__files['test'])

        if len(client_files) > 0:
            print '> \33[36m' + 'Running Client Tests...' + '\33[0m'
            subprocess.call(['make', 'test-client'])


Wyndex.lint_changes()
