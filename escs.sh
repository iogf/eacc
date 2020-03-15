##############################################################################
self.area.get_line('%s.0' % line), # Clone yacc.
cd ~/projects
git clone git@github.com:iogf/yacc.git yacc-code
##############################################################################
# Push code
cd ~/projects/yacc-code
git status
git add *
git commit -a
git push 
##############################################################################
# Create the development branch.
cd ~/projects/yacc-code
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# Merge master into development yacc.
cd ~/projects/yacc-code
git checkout development
git merge master
git push
##############################################################################
# Merge development into master yacc.
cd ~/projects/yacc-code
git checkout master
git merge development
git push
git checkout development
##############################################################################
# check diffs, yacc.
cd ~/projects/yacc-code
git diff
##############################################################################
# delete the development branch, yacc.
git branch -d development
git push origin :development
git fetch -p 
##############################################################################
# undo, changes, yacc, github.
cd ~/projects/yacc-code
git checkout *
##############################################################################
# install, yacc.
sudo bash -i
cd /home/tau/projects/yacc-code
python setup.py install
rm -fr build
exit
##############################################################################
# build, yacc, package, disutils.
cd /home/tau/projects/yacc-code
python setup.py sdist 
rm -fr dist
rm MANIFEST
##############################################################################
# Upload to pypi/pip.

cd ~/projects/yacc-code
python setup.py sdist register upload
rm -fr dist
##############################################################################
# check patch-1
cd /home/tau/projects/yacc-code/
git checkout -b cclauss-patch-1 master
git pull https://github.com/cclauss/yacc.git patch-1

# Merge pull request.
git checkout development
git merge --no-ff cclauss-patch-1
git push origin development
##############################################################################
# create development branch for wiki.
cd /home/tau/projects/yacc.wiki-code/
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# push wiki docs.
cd /home/tau/projects/yacc.wiki-code/
git status
git add *
git commit -a 
git push




