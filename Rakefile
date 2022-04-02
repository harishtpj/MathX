PY="python"
SRC="mathx.py"

task :default => [:run]
task :neat => [:fresh, :clean]

desc "Runs Mathx Compiler"
task :run do
    puts "---> Running Compiler"
    sh "#{PY} #{SRC} #{ENV['ARGS']}",  verbose: false
end

desc "Cleans Working Directory"
task :clean do
    mv Dir.glob("*.c"), "examples", verbose: false
    puts "---> Cleaned Directory"
end

desc "Cleans Working Directory by deleting files"
task :fresh do
    rm_rf "mathx\\__pycache__", verbose: false
    rm_f Dir.glob("*.exe"), verbose: false
    puts "---> Cleaned Directory by deleting files"
end