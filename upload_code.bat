@echo off

REM 设置变量
set COMMIT_MESSAGE= change md file,create directory prompt and upload cjx's files

REM 添加文件到暂存区
echo Adding files to staging area...
git add .

REM 提交到本地仓库
echo Committing changes to local repository...
git commit -m "%COMMIT_MESSAGE%"

REM 添加远程仓库
echo Adding remote repository...
git remote add origin https://gitee.com/stleox/chatops.git

REM 拉取远程代码
echo Pulling changes from GitHub...
git pull origin master

REM 推送到GitHub
echo Pushing changes to GitHub...
git push --set-upstream origin master

echo GitHub Code上传完毕！