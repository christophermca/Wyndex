#!usr/bin/ruby

class Wyndex

  def lint_changes
    get_files_with_changes if not @files

    lint_coffee
    lint_stylus
  end

  def find_dot_only
    print "> \e[36mChecking for `.only` in test files... \e[0m"
    get_files_with_changes if not @files

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
  end

  def find_debuggers
    print "> \e[36mChecking for `debuggers` in files... \e[0m"
      get_files_with_changes if not @files

    @files.each do |file|
      if file =~ /\.coffee\./i
        test_file = File.read("#{file}")

        test_file.each_line.with_index do |line, line_num|
          if line =~ /(debugger)/i
            line_num += 1
            abort("Found `debugger` \n \e[31m ##{line_num}: \e[0m#{file}")
          end
        end
      end
    end
    puts "OK!"

  end

  def run_client_server_tests
    exit 1 unless system "make test-client test-server"
  end

  def clean_code
    get_files_with_changes
    self.lint_changes
    self.find_dot_only
    self.find_debuggers
    # self.run_client_server_tests
  end

  private
  def get_files_with_changes
    if system "git 'rev-parse', '--verify HEAD >/dev/null 2>&1"
      against="HEAD"
    else
      # diff against empty tree object
      against="4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    end

    @files = `git diff --name-only --diff-filter=ACMRTUXB #{against}`.split
  end

  private
  def lint_coffee
    print "> \e[36mLinting CoffeeScript... \e[0m"

    @files.each do |file|
      if file =~ /\.coffee$/i
        output = `./node_modules/.bin/coffeelint -f ./coffeelint.json #{file}`
        if $?.exitstatus > 0
          abort "#{output}"
        end
      end
    end
    puts "OK!"
  end

  private
  def lint_stylus
    print "> \e[36mLinting Stylus... \e[0m"

    @files.each do |file|
      if file =~ /\.styl$/i
        puts " > " + file
         exit 1 unless system "stylint #{file} -c ./.stylintrc"
      end
    end
    puts "OK!"
  end
end
