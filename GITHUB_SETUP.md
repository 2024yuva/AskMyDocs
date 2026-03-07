# 🚀 Connect to GitHub Repository

## Quick Setup (3 Steps)

### Step 1: Create a New GitHub Repository

1. Go to https://github.com/new
2. Repository name: `AskMyDocs` (or your preferred name)
3. Description: `Production RAG system with hybrid retrieval, Groq API, and citation enforcement`
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 2: Initialize Git Locally

Open terminal in your project folder (`D:\AskMyDocs`) and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Production RAG system with FREE Groq API"
```

### Step 3: Connect to GitHub

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/johndoe/AskMyDocs.git
git branch -M main
git push -u origin main
```

---

## ✅ What's Protected (Won't be uploaded)

The `.gitignore` file ensures these sensitive items are NOT uploaded:

- ✅ `.env` - Your API keys (SAFE!)
- ✅ `venv/` - Virtual environment (too large)
- ✅ `chroma_db/` - Vector database (regenerate on new machine)
- ✅ `chat_history/` - User conversations (private)
- ✅ `*.pkl` - BM25 index cache (regenerate)
- ✅ `__pycache__/` - Python cache files

---

## 📦 What WILL be uploaded

- ✅ All source code (`app/`, `eval/`, `tests/`)
- ✅ Documentation (`README.md`, guides)
- ✅ Configuration files (`requirements.txt`, `.env.example`)
- ✅ Sample documents (`docs/`)
- ✅ Batch scripts (`*.bat`)
- ✅ CI/CD workflows (`.github/`)

---

## 🔐 Security Checklist

Before pushing, verify:

1. **Check .env is ignored:**
   ```bash
   git status
   ```
   You should NOT see `.env` in the list

2. **Verify .env.example has no real keys:**
   ```bash
   cat .env.example
   ```
   Should show `your_api_key_here`, not real keys

3. **Test ignore rules:**
   ```bash
   git check-ignore -v .env
   git check-ignore -v venv/
   git check-ignore -v chat_history/
   ```
   All should show they're ignored

---

## 📝 Recommended Repository Settings

### Description
```
Production-grade RAG system with hybrid retrieval (BM25 + Vector), cross-encoder reranking, and citation enforcement. Uses FREE Groq API (Llama 3.3) and sentence-transformers.
```

### Topics (Tags)
```
rag, retrieval-augmented-generation, langchain, groq, llama, 
vector-search, bm25, hybrid-retrieval, fastapi, streamlit, 
nlp, ai, machine-learning, python, free-api
```

### README Badges (Optional)
Add these to the top of your README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Groq](https://img.shields.io/badge/LLM-Groq%20(FREE)-orange.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)
```

---

## 🔄 Future Updates

After making changes, push updates:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Add chat history feature"

# Push to GitHub
git push
```

---

## 🌿 Branching Strategy (Optional)

For collaborative development:

```bash
# Create a new feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push branch
git push -u origin feature/new-feature

# Create Pull Request on GitHub
# After merge, switch back to main
git checkout main
git pull
```

---

## 🚨 If You Accidentally Committed .env

If you accidentally committed your `.env` file with API keys:

```bash
# Remove from git but keep locally
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from tracking"

# Push
git push

# IMPORTANT: Rotate your API keys!
# Go to Groq console and create new keys
```

Then:
1. Go to https://console.groq.com/keys
2. Delete the old key
3. Create a new key
4. Update your local `.env` file

---

## 📋 Complete Command Reference

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit: Production RAG system"
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main

# Daily workflow
git status                    # Check changes
git add .                     # Stage all changes
git commit -m "Your message"  # Commit changes
git push                      # Push to GitHub

# Pull latest changes
git pull

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- .
```

---

## 🎯 Quick Start for New Contributors

Add this to your README.md:

```markdown
## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AskMyDocs.git
   cd AskMyDocs
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Configure API keys:
   ```bash
   copy .env.example .env
   # Edit .env and add your Groq API key
   ```

4. Run the project:
   ```bash
   # Double-click RUN_GROQ_PROJECT.bat
   # Or manually:
   uvicorn app.api.main_groq:app --reload
   streamlit run app/ui/app.py
   ```
```

---

## 🆘 Troubleshooting

### "Permission denied (publickey)"
You need to set up SSH keys or use HTTPS with personal access token.

**Solution 1: Use HTTPS with token**
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/REPO.git
```

**Solution 2: Set up SSH keys**
Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### "Repository not found"
Check the URL is correct:
```bash
git remote -v
```

Update if needed:
```bash
git remote set-url origin https://github.com/CORRECT_USERNAME/CORRECT_REPO.git
```

### Large files error
If you get "file too large" error:
```bash
# Check file sizes
git ls-files -z | xargs -0 du -h | sort -h

# Remove large files from git
git rm --cached path/to/large/file
```

---

## ✅ Verification

After pushing, verify on GitHub:

1. Go to your repository URL
2. Check files are there
3. Verify `.env` is NOT visible
4. Check README displays correctly
5. Test clone on another machine

---

## 🎉 You're Done!

Your project is now on GitHub! Share the link:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

Happy coding! 🚀
