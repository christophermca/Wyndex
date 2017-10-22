import subprocess
import re

class Wyndex:
    def __init__(self):
        """
        Arguments:
            self
            Optional: list of files
        """
        self.__files = self.get_files_with_changes('HEAD^')

    def lint_changes(self):
        """ lint_changes:
        lint files --  stylus,  coffee
        checks for --  dot_only, debuggers
        """
        self.__lint_coffee()
        self.__lint_stylus()
        self.__find_dot_only()
        #self.__find_debuggers()

    def run_tests(self):
        """ docString. """
        __test_files = 'test files!!!!!'
        # self.__run_client_tests()
        # self.__run_server_tests()
        # self.__run_integration_tests()

    def clean_code(self):
        """ docString. """
        self.lint_changes()
        # self.run_tests()

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
        print '> \33[36m' + 'Checking for `.only`...' + '\33[0m'
        test_files = self.__files['test']
        for test in test_files:
            with open(test) as test_file:
                print test_file
                # TODO
                """
                 read line by line for .only
                  if line =~ /(describe|it|context)\.only/i
                    line_num += 1
                    abort "\n Found `.only` \n \33[31m ##{line_num}: \33[0m#{file}"
                """

        """
            ...
            test_file.each_line.with_index do |line, line_num|
              if line =~ /(describe|it|context)\.only/i
                line_num += 1
                abort "\n Found `.only` \n \33[31m ##{line_num}: \33[0m#{file}"
              end
            end

          end
        end
        puts "OK!"
        """

    def __find_debuggers(self):
        print '> \33[36m' + 'Searching for debuggers...' + '\33[0m'
        return self.__files

    def __get_test_files(self):
        regex = re.compile('/*.test.*')
        x = filter(regex.match, self.__files)

    @staticmethod
    def get_previous_commit():
        if subprocess.call(['git', 'rev-parse', '--verify HEAD']):
            against = 'HEAD'
        else:
            against = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

        return against

    @staticmethod
    def get_files_with_changes(previous_commit):
        """ Returns files with changes since the last commit """

        get_files = subprocess.check_output([
            'git', 'diff', '--name-only',
            '--diff-filter=ACMRTUXB', previous_commit])
        files = get_files.split()

        files_dict = dict()
        coffee_files = [f for f in files if '.coffee' in f]
        stylus_files = [f for f in files if '.styl' in f]
        test_files = [f for f in files if '.test.*' in f]

        files_dict['all'] = files
        files_dict['coffee'] = coffee_files
        files_dict['stylus'] = stylus_files
        files_dict['test'] = test_files

        return files_dict


    @staticmethod
    def __run_client_tests():
        subprocess.call(['make', 'test-client'])

    @staticmethod
    def __run_server_tests():
        subprocess.call(['make', 'test-server'])

    @staticmethod
    def __run_integration_tests():
        subprocess.call(['make', 'test-integration'])


Wyndex().clean_code()
