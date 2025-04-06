# GitHub Setup Guide

This guide will help you push your SEO Agency project to GitHub as a private repository, ensuring your API keys and sensitive information remain secure.

## Prerequisites

- GitHub account
- Git installed on your machine
- Project files ready for upload

## Step 1: Prepare Your Repository

Before pushing to GitHub, ensure sensitive data is properly protected:

1. Check that `.env` is listed in `.gitignore`
2. Verify `.env.example` is included (without real API keys)
3. Make sure `google/secret.json` is listed in `.gitignore`
4. Confirm no sensitive credentials are committed

## Step 2: Create a Private Repository on GitHub

1. Log in to your GitHub account
2. Click the "+" icon in the top right corner, then select "New repository"
3. Name your repository (e.g., "seo-agency-private")
4. Add a description (optional)
5. Select "Private" to ensure your repository is not publicly accessible
6. Do not initialize with README, .gitignore, or license (we'll push our existing files)
7. Click "Create repository"

## Step 3: Initialize Git and Push Your Project

Run the following commands in your project directory:

```bash
# Initialize a Git repository (if not already done)
git init

# Add all files (respecting .gitignore)
git add .

# Verify what will be committed (check for sensitive files)
git status

# Commit the files
git commit -m "Initial commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/seo-agency-private.git

# Push to GitHub (main branch)
git push -u origin main
```

If you're using the `master` branch instead of `main`:

```bash
git push -u origin master
```

## Step 4: Verify Repository Privacy

1. Go to your GitHub repository page
2. Look for the "Private" label next to the repository name
3. Check that no sensitive files were uploaded:
   - No `.env` file
   - No `google/secret.json` file
   - No API keys visible in any files

## Step 5: Managing Access

To give specific users access to your private repository:

1. Go to your repository on GitHub
2. Click "Settings"
3. Select "Manage access" 
4. Click "Invite a collaborator"
5. Search for the username or email of the person you want to add
6. Select their role (Read, Triage, Write, Maintain, or Admin)
7. Click "Add"

## Security Best Practices

1. **Never commit API keys**: Always use environment variables and .gitignore
2. **Rotate compromised keys**: If you accidentally commit API keys, rotate them immediately
3. **Use SSH keys**: For more secure GitHub authentication
4. **Review before pushing**: Always check `git status` before committing
5. **Consider Git Hooks**: Use pre-commit hooks to prevent accidentally committing sensitive data

## Using Git LFS (Optional)

If your repository contains large files like datasets or models:

1. Install Git LFS: `git lfs install`
2. Track large file types: `git lfs track "*.csv" "*.h5" "*.pkl"`
3. Add .gitattributes: `git add .gitattributes`
4. Commit and push as normal

## Troubleshooting

- **File ignored by .gitignore still being tracked?** It might have been tracked before being added to .gitignore. Use: `git rm --cached <file>` to untrack it.
- **Push error?** Make sure your GitHub account has the correct authentication set up.
- **Large files error?** Consider using Git LFS or exclude the files in .gitignore. 