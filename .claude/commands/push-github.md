Run the following steps to commit and push all changes to GitHub.

1. Run `git status` to see what has changed. If there is nothing to commit, stop and tell the user.
2. Run `git diff HEAD` to read every changed line.
3. Run `git log --oneline -5` to match the existing commit style.
4. Auto-generate a commit message from the diff:
   - Present tense, under 72 characters
   - Describe WHY the change was made, not which files changed
   - If multiple unrelated changes exist, summarise the most significant one
   - End the message with:
     Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. Stage all changed and new project files:
   - Use specific file paths, never `git add -A` or `git add .`
   - Never stage .env or any file that may contain secrets
6. Create the commit using the auto-generated message.
7. Run `git push origin HEAD` to push to the current branch.
8. Confirm success and print the branch name and latest commit hash.
