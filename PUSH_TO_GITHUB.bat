@echo off
echo ========================================
echo   Push AskMyDocs to GitHub
echo ========================================
echo.
echo This script will help you push to GitHub
echo.
echo IMPORTANT: Make sure you've created a repository on GitHub first!
echo Visit: https://github.com/new
echo.
pause
echo.
echo Step 1: Initializing Git...
git init
echo.
echo Step 2: Adding all files...
git add .
echo.
echo Step 3: Creating first commit...
git commit -m "Initial commit: Production RAG system with FREE Groq API"
echo.
echo ========================================
echo   Now enter your GitHub repository URL
echo ========================================
echo.
echo Example: https://github.com/yourusername/AskMyDocs.git
echo.
set /p REPO_URL="Enter your GitHub repository URL: "
echo.
echo Step 4: Adding remote repository...
git remote add origin %REPO_URL%
echo.
echo Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main
echo.
echo ========================================
echo   Done!
echo ========================================
echo.
echo Your project is now on GitHub!
echo Visit: %REPO_URL%
echo.
pause
