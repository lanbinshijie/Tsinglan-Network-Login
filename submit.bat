@echo off
chcp 65001

set /p comment="请输入提交信息: "

git add .
git commit -m "%comment%"

echo Pushing to github-origin...
git push github-origin main

echo Pushing to gitea-origin...
git push gitea-origin main

echo Done!
pause
