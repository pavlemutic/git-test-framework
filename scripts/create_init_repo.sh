rm -rf scenario_artefacts/init_repo
mkdir scenario_artefacts/init_repo
cd scenario_artefacts/init_repo || { echo "'scenario_artefacts' dir might not exist"; exit 1; }
mkdir repo.git
mkdir local

git init repo.git --bare
git --git-dir=repo.git symbolic-ref HEAD refs/heads/main
git clone repo.git local

cd local || { echo "'local' dir might not exist"; exit 1; }
git config user.name "Pavle Mutic"
git config user.email "mail@pavlemutic.com"

printf "# Test Git Repo\n" >> README.md
git add README.md
git commit -m "Initial commit"
git push -u ../repo.git main

mv .git .git-nogit
