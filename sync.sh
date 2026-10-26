#!/bin/bash
cd /livescores || exit 1

# Prevent overlapping runs
exec 9>/tmp/livescores-sync.lock
flock -n 9 || exit 0

# Pull first; if conflicts, the server's version wins
git pull --rebase -X theirs --autostash || { git rebase --abort 2>/dev/null; exit 1; }

git add -A
git diff --cached --quiet && exit 0

# Safety net for secrets
if git diff --cached --name-only | grep -qx "secrets.json"; then
    echo "ERROR: secrets.json staged, aborting" >&2
    git reset -q
    exit 1
fi

git commit -q -m "Auto-sync from server $(date -Is)"
git push origin master
