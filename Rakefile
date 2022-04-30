PY="python"
SRC="mathx.py"

task :default => [:run]
task :release => [:release_linux, :release_windows]
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
    rm_rf "mathx\\errors\\__pycache__", verbose: false
    rm_rf "mathx\\c\\__pycache__", verbose: false
    rm_f Dir.glob("*.exe"), verbose: false
    puts "---> Cleaned Directory by deleting files"
end

desc "Runs Mathx Compiler Tests"
task :test do
    puts "---> Testing Compiler"
    sh "#{PY} #{SRC} examples\\sample.mx",  verbose: false
end

desc "Cleans test files"
task :cleantest do
    rm_f Dir.glob("sample.*"), verbose: false
    puts "---> Cleaned test files"
end

desc "Prepare new Release"
task :release_linux do
    cp_r Dir.glob("mathx"), "package\\linux", verbose: false
    cp "mathx.py", "package\\linux\\mathx.py", verbose: false
    mkdir_p "package\\linux\\examples", verbose: false
    cp_r Dir.glob("examples/*.mx"), "package\\linux\\examples", verbose: false

    File.open("package\\linux\\mathxc", "w") { |file|
        file.write("#!/bin/sh\npython3 mathx.py $*")
    }

    puts "---> Prepared Linux Release"
end

desc "Prepare new Release"
task :release_windows do
    cp_r Dir.glob("mathx"), "package\\windows", verbose: false
    cp "mathx.py", "package\\windows\\mathxc", verbose: false
    mkdir_p "package\\windows\\examples", verbose: false
    cp_r Dir.glob("examples/*.mx"), "package\\windows\\examples", verbose: false

    File.open("package\\windows\\mathxc.bat", "w") { |file|
        file.write("@echo off\npy \"%~dpn0\" %*")
    }

    puts "---> Prepared Windows Release"
end