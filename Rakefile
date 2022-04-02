PY="python"
SRC="mathx.py"

task :default => [:run]

desc "Runs Mathx Compiler"
task :run do
    puts "---> Running Compiler"
    sh "#{PY} #{SRC} #{ENV['ARGS']}",  verbose: false
end

desc "Cleans Working Directory"
task :clean do
    rm_rf "mathx\\__pycache__", verbose: false
    puts "---> Cleaned Directory"
end