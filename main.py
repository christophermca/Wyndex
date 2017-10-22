import subprocess
import re

class Wyndex:
    def __init__(self):
        """
        Arguments:
            self
            Optional: list of files
        """
        previous_commit = self.get_previous_commit()
        self.__files = self.get_files_with_changes(previous_commit)

    def lint_changes(self):
        """ lint_changes:
        lint files --  stylus,  coffee
        checks for --  dot_only, debuggers
        """
        self.__lint_coffee()
        self.__lint_stylus()

        # self.__find_dot_only()
        # self.__find_debuggers()

    def run_tests(self):
        """ docString. """
        __test_files = 'test files!!!!!'
        print __test_files
        # self.__run_client_tests()
        # self.__run_server_tests()
        # self.__run_integration_tests()

    def clean_code(self):
        """ docString. """
        self.lint_changes()
        # self.run_tests()



    def __lint_coffee(self):
        # lint coffee
        print '> \33[36m' + 'Linting CoffeeScript...' + '\33[0m'
        coffee = re.compile('/*.coffee*')
        coffee_files = filter(coffee.match, self.__files)
        print 'here', coffee_files
        # subprocess.call(['./node_modules/.bin/coffeelint', '-f ./coffeelint.json,', coffee_files])

    def __lint_stylus(self):
        # lint coffee
        print '> \33[36m' + 'Linting Stylus...' + '\33[0m'
        return self.__files

    def __find_dot_only(self):
        print '> \33[36m' + 'Checking for `.only`...' + '\33[0m'
        return self.__files
        '''

        @files.each do |file|
          if file =~ /test\./i
            test_file = File.read("#{file}")

            test_file.each_line.with_index do |line, line_num|
              if line =~ /(describe|it|context)\.only/i
                line_num += 1
                abort "\n Found `.only` \n \e[31m ##{line_num}: \e[0m#{file}"
              end
            end

          end
        end
        puts "OK!"
        '''

    def __find_debuggers(self):
        print '> \33[36m' +  'Searching for debuggers...' + '\33[0m'
        return self.__files

    def __get_test_files(self):
        print 'files:', self.__files
        regex = re.compile('/*.test.*')
        x =  filter(regex.match, self.__files)

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

        return get_files.split()

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
