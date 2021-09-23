#!/bin/sh

PREFIX="${BOOKMARKS_DIR:-$HOME/.bookmarks}"
HOOKS="$PREFIX/.git/hooks"

([ -f "$HOOKS/post-commit" ] || [ -f "$HOOKS/post-checkout" ] || [ -f "$HOOKS/post-merge" ]) && echo "Some hooks already present. Deploy manually." && exit 1

# simple download after commits
ln -s "$(which rofi-bookmark-download)" "$HOOKS/post-commit"

# retry hook after pulls and checkouts
ln -s "$(which rofi-bookmark-download-retry)" "$HOOKS/post-merge"
ln -s "$(which rofi-bookmark-download-retry)" "$HOOKS/post-checkout"
