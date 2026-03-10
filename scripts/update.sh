#!/usr/bin/env bash
set -euo pipefail

REPO="Mr-several/skills-ha-mcp-control"
BRANCH="main"
SKILL_DIR_NAME="skills-ha-mcp-control"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="${SKILL_ROOT%/*}/.backup"

log()  { printf '[INFO]  %s\n' "$*"; }
warn() { printf '[WARN]  %s\n' "$*" >&2; }
die()  { printf '[ERROR] %s\n' "$*" >&2; exit 1; }

cleanup() {
    [ -n "${TMP_DIR:-}" ] && [ -d "$TMP_DIR" ] && rm -rf "$TMP_DIR"
}
trap cleanup EXIT

if [ ! -f "$SKILL_ROOT/SKILL.md" ]; then
    die "Cannot locate SKILL.md in $SKILL_ROOT — is this script inside a valid skill?"
fi

TMP_DIR="$(mktemp -d)"
ZIP_URL="https://codeload.github.com/${REPO}/zip/${BRANCH}"
ZIP_FILE="$TMP_DIR/repo.zip"

log "Downloading latest version from $REPO ..."
if ! curl -fSL "$ZIP_URL" -o "$ZIP_FILE" 2>/dev/null; then
    die "Download failed. Check network and repo access: https://github.com/$REPO"
fi

log "Extracting archive ..."
unzip -q "$ZIP_FILE" -d "$TMP_DIR"

EXTRACTED_DIR="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -1)"
if [ -z "$EXTRACTED_DIR" ] || [ ! -f "$EXTRACTED_DIR/SKILL.md" ]; then
    die "Downloaded archive does not contain a valid skill (SKILL.md missing)."
fi

LOCAL_HASH=""
REMOTE_HASH=""
if command -v md5sum >/dev/null 2>&1; then
    LOCAL_HASH="$(find "$SKILL_ROOT" -type f -not -path '*/.git/*' -not -path '*/.backup/*' -exec md5sum {} \; 2>/dev/null | sort -k2 | md5sum | awk '{print $1}')"
    REMOTE_HASH="$(find "$EXTRACTED_DIR" -type f -exec md5sum {} \; 2>/dev/null | sort -k2 | md5sum | awk '{print $1}')"
elif command -v md5 >/dev/null 2>&1; then
    LOCAL_HASH="$(find "$SKILL_ROOT" -type f -not -path '*/.git/*' -not -path '*/.backup/*' -exec md5 -q {} \; 2>/dev/null | sort | md5 -q)"
    REMOTE_HASH="$(find "$EXTRACTED_DIR" -type f -exec md5 -q {} \; 2>/dev/null | sort | md5 -q)"
fi

if [ -n "$LOCAL_HASH" ] && [ -n "$REMOTE_HASH" ] && [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
    log "Already up to date. No changes detected."
    exit 0
fi

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_PATH="$BACKUP_DIR/${SKILL_DIR_NAME}-${TIMESTAMP}"
mkdir -p "$BACKUP_DIR"
log "Backing up current version to $BACKUP_PATH ..."
cp -R "$SKILL_ROOT" "$BACKUP_PATH"

rollback() {
    warn "Update failed — rolling back ..."
    if [ -d "$BACKUP_PATH" ]; then
        rm -rf "$SKILL_ROOT"
        cp -R "$BACKUP_PATH" "$SKILL_ROOT"
        log "Rollback complete. Previous version restored."
    else
        warn "Backup not found; manual recovery may be needed."
    fi
    exit 1
}

log "Replacing with new version ..."

ITEMS_TO_KEEP=(".git" ".backup")
for item in "$SKILL_ROOT"/*  "$SKILL_ROOT"/.[!.]* "$SKILL_ROOT"/..?*; do
    [ -e "$item" ] || continue
    base="$(basename "$item")"
    skip=false
    for keep in "${ITEMS_TO_KEEP[@]}"; do
        [ "$base" = "$keep" ] && skip=true && break
    done
    $skip || rm -rf "$item"
done

if ! cp -R "$EXTRACTED_DIR"/* "$SKILL_ROOT/" 2>/dev/null; then
    rollback
fi

for dotfile in "$EXTRACTED_DIR"/.[!.]* "$EXTRACTED_DIR"/..?*; do
    [ -e "$dotfile" ] || continue
    base="$(basename "$dotfile")"
    [ "$base" = ".git" ] && continue
    cp -R "$dotfile" "$SKILL_ROOT/" 2>/dev/null || true
done

if [ ! -f "$SKILL_ROOT/SKILL.md" ]; then
    rollback
fi

log "Update complete."
log "Backup saved at: $BACKUP_PATH"
log "Please restart your AI coding tool to reload the skill."
