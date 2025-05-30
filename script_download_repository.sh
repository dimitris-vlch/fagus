#!/bin/bash

# URL του repository
REPO_URL="https://github.com/dimitris-vlch/fagus"
# Όνομα του κεντρικού φακέλου
BASE_DIR="fagus"

# Δημιουργία του βασικού φακέλου
mkdir -p "$BASE_DIR"
cd "$BASE_DIR" || exit

# Λήψη όλων των branches από το απομακρυσμένο repository
git ls-remote --heads "$REPO_URL" | awk '{print $2}' | sed 's|refs/heads/||' | while read branch; do
    echo "Κατεβάζω το branch: $branch"
    git clone --branch "$branch" --single-branch "$REPO_URL" "$branch"
done
