``# group8
**Configuring pylint localy**

Step 1
clone the project repository
command: git clone git@dev.telecomste.fr:printerfaceadmin/2020-21/group8.git

Step 2
move to .git/hooks

Step 3
Add file pre-commit
command: touch pre-commit

Step 4
Add this code to pre-commit file and save 
`
#!/bin/bash

echo "Running pre-commit hook"
#./scripts/run-tests.bash
#git show --no-commit-id --name-only -r
id=$(git rev-parse HEAD)
echo "getting files"
files=$(git diff-tree --no-commit-id --name-only -r $id)
echo $files
python ./test/linter.py $files
# $? stores exit value of the last command
if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi
`

This will launch pylint test before commiting locally and prevent commiting if code format is not conform
