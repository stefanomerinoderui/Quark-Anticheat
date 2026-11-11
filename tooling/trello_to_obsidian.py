#!/usr/bin/env python3
"""Convert a Trello board JSON export into an Obsidian Kanban board + one note per card.

Usage:
    python3 tooling/trello_to_obsidian.py board.json docs/obsidian-vault/quark-vault/04-Kanban

Writes <out>/Board.md (obsidian-kanban plugin format) and <out>/cards/<title>.md.
Re-running overwrites Board.md and the card notes it generated (back up first or use git).
Archived lists/cards are skipped unless --include-archived is given.
Only the standard library is used.
"""
import argparse, json, re, sys
from collections import defaultdict
from pathlib import Path

def safe(name):
    name = re.sub(r'[\\/:*?"<>|#^\[\]]', '-', name).strip(' .')
    return re.sub(r'\s+', ' ', name)[:80] or 'untitled'

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('export'); ap.add_argument('out')
    ap.add_argument('--include-archived', action='store_true')
    a = ap.parse_args()

    data = json.load(open(a.export, encoding='utf-8'))
    out = Path(a.out); cards_dir = out / 'cards'; cards_dir.mkdir(parents=True, exist_ok=True)

    members = {m['id']: m.get('fullName') or m.get('username', m['id']) for m in data.get('members', [])}
    lists = [l for l in data.get('lists', []) if a.include_archived or not l.get('closed')]
    lists.sort(key=lambda l: l.get('pos', 0))
    checklists = defaultdict(list)
    for cl in data.get('checklists', []):
        checklists[cl['idCard']].append(cl)
    comments = defaultdict(list)
    for act in data.get('actions', []):
        if act.get('type') == 'commentCard':
            cid = act.get('data', {}).get('card', {}).get('id')
            who = act.get('memberCreator', {}).get('fullName', '?')
            comments[cid].append((act.get('date', '')[:10], who, act['data'].get('text', '')))

    cards_by_list = defaultdict(list)
    for c in data.get('cards', []):
        if c.get('closed') and not a.include_archived:
            continue
        cards_by_list[c['idList']].append(c)

    used = set(); board = ['---', '', 'kanban-plugin: board', '', '---', '']
    for l in lists:
        board += [f'## {l["name"]}', '']
        for c in sorted(cards_by_list[l['id']], key=lambda c: c.get('pos', 0)):
            base = safe(c['name']); fname = base; n = 2
            while fname.lower() in used:
                fname = f'{base} ({n})'; n += 1
            used.add(fname.lower())
            labels = [safe(x.get('name') or x.get('color', '')).replace(' ', '-') for x in c.get('labels', []) if x.get('name') or x.get('color')]
            owners = [members.get(m, m) for m in c.get('idMembers', [])]
            due = (c.get('due') or '')[:10]
            done = bool(c.get('dueComplete'))
            line = f'- [{"x" if done else " "}] [[cards/{fname}|{c["name"].replace("|", "/")}]]'
            if due: line += f' @{{{due}}}'
            line += ''.join(f' #{x}' for x in labels)
            board.append(line)

            fm = ['---', f'title: {yaml_str(c["name"])}', f'status: {yaml_str(l["name"])}',
                  f'owner: {yaml_str(", ".join(owners))}', f'due: {due}',
                  'labels: ' + json.dumps(labels, ensure_ascii=False),
                  f'source: {yaml_str("trello:" + c.get("shortUrl", c["id"]))}', 'tags: [card]', '---', '']
            body = [c.get('desc', '').strip(), '']
            for cl in checklists.get(c['id'], []):
                body += [f'## {cl["name"]}']
                for it in sorted(cl.get('checkItems', []), key=lambda i: i.get('pos', 0)):
                    body.append(f'- [{"x" if it.get("state") == "complete" else " "}] {it["name"]}')
                body.append('')
            if comments.get(c['id']):
                body += ['## Comentarios (Trello)']
                body += [f'- {d} — {w}: {t}'.replace('\n', ' ') for d, w, t in sorted(comments[c['id']])]
                body.append('')
            (cards_dir / f'{fname}.md').write_text('\n'.join(fm + body), encoding='utf-8')
        board.append('')
    board += ['%% kanban:settings', '```', json.dumps({'kanban-plugin': 'board'}), '```', '%%', '']
    (out / 'Board.md').write_text('\n'.join(board), encoding='utf-8')
    print(f'{sum(len(cards_by_list[l['id']]) for l in lists)} cards, {len(lists)} lists -> {out}')

if __name__ == '__main__':
    sys.exit(main())
