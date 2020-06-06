##############################################################################
cd ~/projects
git clone git@github.com:iogf/eacc.git eacc-code
##############################################################################
# Push code
cd ~/projects/eacc-code
git status
git add *
git commit -a
git push 
##############################################################################
# Create the development branch.
cd ~/projects/eacc-code
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# Merge master into development eacc.
cd ~/projects/eacc-code
git checkout development
git merge master
git push
##############################################################################
# Merge development into master eacc.
cd ~/projects/eacc-code
git checkout master
git merge development
git push
git checkout development
##############################################################################
# check diffs, eacc.
cd ~/projects/eacc-code
git diff
##############################################################################
# delete the development branch, eacc.
git branch -d development
git push origin :development
git fetch -p 
##############################################################################
# undo, changes, eacc, github.
cd ~/projects/eacc-code
git checkout *
##############################################################################
# install, eacc.
sudo bash -i
cd /home/tau/projects/eacc-code
python setup.py install
rm -fr build
exit
##############################################################################
# build, eacc, package, disutils.
cd /home/tau/projects/eacc-code
python setup.py sdist 
rm -fr dist
rm MANIFEST
##############################################################################
# Upload to pypi/pip.

cd ~/projects/eacc-code
python setup.py sdist register upload
rm -fr dist
##############################################################################
# check patch-1
cd /home/tau/projects/eacc-code/
git checkout -b cclauss-patch-1 master
git pull https://github.com/cclauss/eacc.git patch-1

# Merge pull request.
git checkout development
git merge --no-ff cclauss-patch-1
git push origin development
##############################################################################
# create development branch for wiki.
cd /home/tau/projects/eacc.wiki-code/
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# push wiki docs.
cd /home/tau/projects/eacc.wiki-code/
git status
git add *
git commit -a 
git push

