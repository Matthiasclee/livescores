#!/bin/bash
cd /livescores || exit 1
inotifywait -m -r -q -e modify,create,delete,move \
  --exclude '(\.git/|\.log$|secrets\.json)' /livescores |
while read -r _; do
    # Debounce: wait for changes to settle, then drain queued events
    sleep 5
    while read -t 1 -r _; do :; done
    /livescores/sync.sh >> /tmp/livescores-sync.log 2>&1
done
