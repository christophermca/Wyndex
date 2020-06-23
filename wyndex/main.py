import subprocess
import re

class Wyndx(object):
    def __init__(self, *args, **kwargs):
        """
        Arguments:
            *args:
                file(s)    # One or multiple files

            **kwargs:
               --exitcode    # Use exitcode
               --tdd         # Run tests for script changes
               --skip-tests  # Skip tests
        """

        if kwargs['SHA']:
            files = self.get_files_with_changes(kwargs['SHA'])
            self.__files = self.__sort_files(files)
        else:
            self.__files = self.__sort_files(args)


    @classmethod
    def lint_changes(cls):
        """ lint_changes:
        lint files -- stylus, coffee, javascript
        checks for -- dot_only, debuggers
        """
        cls().__lint_coffee()
        cls().__lint_js()
        cls().__lint_stylus()
        cls().__find_dot_only()
        cls().__find_debuggers()

    @classmethod
    def run_tests(cls):
        """ Runs Client, Server, Integration tests. """
        cls().__run_server_tests()
        cls().__run_client_tests()
        # cls().__run_integration_tests()

    @classmethod
    def clean_code(cls):
        """ Runs Linter and Checks tests """
        cls().lint_changes()
        cls().run_tests()
        print('\n>> \33[32m' + 'Complete.\n' + '\33[0m')

    @staticmethod
    def get_files_with_changes(SHA):
        """ @Returns: A list of files with changes """

        get_files = subprocess.check_output([
            'git', 'diff', '--name-only',
            '--diff-filter=ACMRTUXB', SHA])

        return get_files.split()

    @staticmethod
    def __sort_files(files):
        """ Setup configuration file
            contains:
            - filetypes
            - linting command
        """
        files_dict = dict()
        coffee_files = [f for f in files if '.coffee' in f]
        js_files = [f for f in files if bool(re.search('(?<!.test).js$', f))]
        stylus_files = [f for f in files if bool(re.search(r'.styl$', f))]
        test_files = [f for f in files
                      if bool(re.search(r'.test.[coffee|js]', f))]

        files_dict['all'] = files
        files_dict['scripts'] = {
            'coffee': coffee_files,
            'js': js_files
        }
        files_dict['stylus'] = stylus_files
        files_dict['test'] = test_files

        return files_dict

    def __lint_js(self):
        print('> \33[36m' + 'Linting Javascript...' + '\33[0m')

        for js_file in self.__files['scripts']['js']:
            subprocess.call([
                'eslint',
                '--ignore-path',
                '.gitignore',
                js_file], cwd='./')

    def __lint_coffee(self):
        print('> \33[36m' + 'Linting CoffeeScript...' + '\33[0m')

        for coffee_file in self.__files['scripts']['coffee']:
            subprocess.call([
                'coffeelint',
                '-f', './coffeelint.json',
                coffee_file], cwd='./')

    def __lint_stylus(self):
        print('> \33[36m' + 'Linting Stylus...' + '\33[0m')

        for styl_file in self.__files['stylus']:
            subprocess.call([
                'coffeelint',
                '-f', './coffeelint.json',
                styl_file], cwd='./')

    def __find_dot_only(self):
        print('> \33[36m' + 'Searching for `.only`...' + '\33[0m')

        for test in self.__files['test']:
            with open(test) as f:
                for idx, line in enumerate(f):
                    if re.match("\s*(it|describe|context)\.only", line) is not None:
                        print('Found `.only`')
                        print('\33[33m #{}:\33[31m {}\33[0m \n'
                              .format((idx + 1), test))

    def __find_debuggers(self):
        print('> \33[36m' + 'Searching for debuggers...' + '\33[0m')
        print(self.__files)

        for scriptType in self.__files['scripts']:
            scripts = self.__files['scripts'][scriptType]
            for script in scripts:
                with open(script) as f:
                    for idx, line in enumerate(f):
                        if re.search("debugger", line) is not None:
                            print('\33[31mFound Debuggers:\33[0m')
                            print('\33[33m #{}:\33[31m {}\33[0m \n'
                                  .format((idx + 1), f.name))

    def __run_integration_tests(self):
        regex = re.compile('/integration/')
        integration_tests = filter(regex.search, self.__files['test'])

        if len(integration_tests) > 0:
            print('> \33[36m' + 'Running Integration Tests...' + '\33[0m')

            for test in integration_tests:
                subprocess.check_output(['mocha', test])

    def __run_server_tests(self):
        regex = re.compile('/server/')
        server_tests = filter(regex.search, self.__files['test'])

        if len(server_tests) > 0:
            print('> \33[36m' + 'Running Server Tests...' + '\33[0m')

            for test in server_tests:
                subprocess.check_output(['mocha', test])

    def __run_client_tests(self):
        regex = re.compile('/client/')
        client_files = filter(regex.search, self.__files['test'])

        if len(client_files) > 0:
            print('> \33[36m' + 'Running Client Tests...' + '\33[0m')
            subprocess.call(['make', 'test-client'])
