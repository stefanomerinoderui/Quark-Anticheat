#!/usr/bin/env python3
"""Enforce the vault's append-only standard (05-Meta/Append-Only-Standard.md).

Usage:
    python3 tooling/check_append_only.py            # staged changes vs HEAD (pre-commit)
    python3 tooling/check_append_only.py --worktree # working tree vs HEAD
    python3 tooling/check_append_only.py --base REF # HEAD..worktree-free: REF vs HEAD (CI)

Rules for tracked .md files under the vault (exempt: 04-Kanban/Board.md, Templates/, .obsidian/):
  * no line may be removed or changed, except frontmatter keys status/superseded-by/updated;
  * insertions are allowed only at end of file;
  * deletions and non-100% renames are rejected. New files are always fine.
Exit 0 = ok, 1 = violations. Standard library only.
"""
import argparse, re, subprocess, sys

VAULT = 'docs/obsidian-vault/quark-vault/'
EXEMPT_PREFIX = (VAULT + 'Templates/', VAULT + '.obsidian/')
EXEMPT_FILES = {VAULT + '04-Kanban/Board.md'}
FM_KEYS = ('status:', 'superseded-by:', 'updated:')
HUNK = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')

def git(*a):
    return subprocess.run(['git', *a], capture_output=True, text=True, check=True).stdout

def covered(path):
    return (path.startswith(VAULT) and path.endswith('.md')
            and path not in EXEMPT_FILES and not path.startswith(EXEMPT_PREFIX))

def fm_end(lines):
    """1-based index of the closing '---' of the frontmatter, or 0 if none."""
    if lines and lines[0].strip() == '---':
        for i, l in enumerate(lines[1:], start=2):
            if l.strip() == '---':
                return i
    return 0

def check_file(path, mode_args, errors, old_ref='HEAD'):
    old = git('show', f'{old_ref}:{path}').split('\n')
    if old and old[-1] == '':
        old.pop()
    end = fm_end(old)
    diff = git('diff', *mode_args, '-U0', '--no-color', '--', path).split('\n')
    i = 0
    while i < len(diff):
        m = HUNK.match(diff[i])
        i += 1
        if not m:
            continue
        o_start = int(m.group(1)); o_len = 1 if m.group(2) is None else int(m.group(2))
        removed, added = [], []
        while i < len(diff) and not diff[i].startswith('@@'):
            l = diff[i]
            if l.startswith('-') and not l.startswith('---'):
                removed.append(l[1:])
            elif l.startswith('+') and not l.startswith('+++'):
                added.append(l[1:])
            i += 1
        if o_len == 0:                       # pure insertion after old line o_start
            if o_start >= len(old):
                continue                     # at EOF: ok
            if o_start < end and all(a.startswith(FM_KEYS) for a in added):
                continue                     # new allowed frontmatter key
            errors.append(f'{path}: insertion after line {o_start} (not at end of file)')
        else:
            # appending to a file without trailing newline shows as remove+re-add of last line
            if removed and added and removed[-1] == added[0] and o_start + o_len - 1 == len(old) and len(removed) == 1:
                continue
            first, last = o_start, o_start + o_len - 1
            if last <= end and all(r.startswith(FM_KEYS) for r in removed) and all(a.startswith(FM_KEYS) for a in added):
                continue
            errors.append(f'{path}: lines {first}-{last} modified/removed: ' + ' | '.join(r[:60] for r in removed[:2]))

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--worktree', action='store_true')
    g.add_argument('--base')
    a = ap.parse_args()
    old_ref = 'HEAD'
    if a.base:
        mode_args, ns = [a.base, 'HEAD'], ['diff', '--name-status', '-M', a.base, 'HEAD']
        old_ref = a.base
    elif a.worktree:
        mode_args, ns = [], ['diff', '--name-status', '-M', 'HEAD']
    else:
        mode_args, ns = ['--cached'], ['diff', '--cached', '--name-status', '-M']
    errors = []
    for row in git(*ns, '--', VAULT).splitlines():
        parts = row.split('\t'); st = parts[0]
        if st == 'A':
            continue
        if st == 'D':
            if covered(parts[1]): errors.append(f'{parts[1]}: file deleted')
        elif st.startswith('R'):
            if covered(parts[1]) and st != 'R100': errors.append(f'{parts[1]} -> {parts[2]}: renamed with content change ({st})')
        elif st.startswith('M') and covered(parts[1]):
            check_file(parts[1], mode_args, errors, old_ref)
    if errors:
        print('APPEND-ONLY VIOLATIONS (see 05-Meta/Append-Only-Standard.md):', file=sys.stderr)
        for e in errors: print('  -', e, file=sys.stderr)
        return 1
    print('append-only check: ok')
    return 0

if __name__ == '__main__':
    sys.exit(main())
