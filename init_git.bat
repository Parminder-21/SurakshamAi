@echo off
cd /d d:\Hackathon\SurakshamAI

echo Initializing git repository...
git init

echo Adding remote origin...
git remote add origin https://github.com/Parminder-21/SurakshamAi.git

echo Staging all files...
git add .

echo Creating commit...
git commit -m "chore: initial project structure"

echo Renaming branch to main...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo.
echo ✓ Git repository initialized and pushed successfully!
pause
