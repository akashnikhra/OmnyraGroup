#!/usr/bin/env python3
"""OMNyra Exam Portal - DOCX practice-bank -> portal JSON (stdlib only, Python 3.11+).

Reads: Exam Portal/AIGP Exam/AIGP_Practice_Questions*.docx
Parses word/document.xml with zipfile + xml.etree (no pip deps).
Correct answer = run with green w:color (00B050/00B000/008000/2E7D32/70AD47)
  cross-checked against trailing Q#/Ans table; mismatch = holdout.
Usage:
  python "Exam Portal/tools/docx-to-portal.py" --parse-only
  python "Exam Portal/tools/docx-to-portal.py" --rebalance
"""
import zipfile, xml.etree.ElementTree as ET, os, re, json, random, sys, argparse

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
GREEN = {'00b050', '00b000', '008000', '2e7d32', '22b14f', '70ad47'}
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'AIGP Exam')
FILES = ['AIGP_Practice_Questions.docx', 'AIGP_Practice_Questions_Set2.docx',
         'AIGP_Practice_Questions_Set3.docx', 'AIGP_Practice_Questions_Set4.docx']

def parse_docx(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    # answer key: first table, rows of Q#/Ans pairs
    key = {}
    tables = root.findall('.//w:tbl', NS)
    if tables:
        for row in tables[0].findall('w:tr', NS)[1:]:
            cells = [ ''.join((t.text or '') for t in c.findall('.//w:t', NS)).strip()
                      for c in row.findall('w:tc', NS) ]
            for i in range(0, len(cells) - 1, 2):
                if cells[i].isdigit() and cells[i+1] in ('A', 'B', 'C', 'D'):
                    key[int(cells[i])] = 'ABCD'.index(cells[i+1])
    # green-marked correct option per question block
    paras = []
    for p in root.findall('.//w:p', NS):
        txt = ''.join((t.text or '') for t in p.findall('.//w:t', NS)).strip()
        if not txt:
            continue
        green = None
        runs_green = False
        for r in p.findall('w:r', NS):
            for c in r.findall('w:rPr/w:color', NS):
                v = (c.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') or '').lower()
                if v in GREEN:
                    runs_green = True
                    ttxt = ''.join((t.text or '') for t in r.findall('w:t', NS)).strip()
                    m = re.match(r'^([A-D])\.', ttxt)
                    if m:
                        green = 'ABCD'.index(m.group(1))
        if runs_green and green is None:
            m = re.match(r'^([A-D])\.', txt)
            if m:
                green = 'ABCD'.index(m.group(1))
        paras.append((txt, green))
    # block-split on "Question N"
    recs, cur = [], None
    def flush():
        if cur and len(cur['options']) == 4:
            recs.append(cur)
        elif cur and cur['options']:
            print(f"warn: skipped incomplete block ({len(cur['options'])}/4 options, stem={cur['stem'][:60]!r})", file=sys.stderr)
    for txt, green in paras:
        if re.match(r'^Question\s+\d+', txt):
            flush(); cur = {'domain': '', 'stem': '', 'options': [], 'green': None, 'expl': ''}
        elif cur is not None:
            if txt.startswith('Domain:'):
                cur['domain'] = txt[len('Domain:'):].strip()
            elif re.match(r'^[A-D]\.\s', txt):
                cur['options'].append(re.sub(r'^[A-D]\.\s*', '', txt).strip())
                if green is not None:
                    cur['green'] = green
                if txt.rstrip().endswith('✓ Correct'):
                    cur['options'][-1] = cur['options'][-1].replace('✓ Correct', '').strip()
                    cur['green'] = len(cur['options']) - 1
            elif txt.startswith('Explanation:'):
                cur['expl'] = txt[len('Explanation:'):].strip()
            elif not cur['stem'] and len(txt) > 20:
                cur['stem'] = txt
    flush()
    # attach key by order, flag mismatches
    for i, r in enumerate(recs, 1):
        r['key'] = key.get(i)
        r['mismatch'] = (r['green'] is not None and r['key'] is not None and r['green'] != r['key'])
        r['correct'] = r['green'] if r['green'] is not None else r['key']
    return recs

def to_portal(rec, qid):
    if len(rec['stem']) < 10:
        raise ValueError(f'short stem {qid}: {len(rec["stem"])} chars')
    if len(rec['expl']) < 10:
        raise ValueError(f'short rationale {qid}: {len(rec["expl"])} chars')
    opts = rec['options']
    if len(opts) != 4 or len({o.lower() for o in opts}) != 4:
        raise ValueError(f'bad options {qid}: need 4 distinct')
    if rec['correct'] not in (0, 1, 2, 3):
        raise ValueError(f'no correct {qid}: got {rec["correct"]!r}')
    return {'id': qid, 'question': rec['stem'], 'options': rec['options'],
            'correctIndex': rec['correct'], 'rationale': rec['expl'],
            'topic': rec['domain'] or 'General', 'difficulty': 'medium', 'marks': 1}

def atomic_write_text(path, text):
    # Same payload bytes as before (no trailing-newline change) to keep
    # default-seed outputs byte-identical; tmp+rename only adds atomicity.
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text)
    os.replace(tmp, path)

def rebalance(seed=20261004):
    pools = {}
    for n, fn in enumerate(FILES):
        fp = os.path.join(SRC, fn)
        if not os.path.exists(fp):
            print(f'missing input file: {fp}', file=sys.stderr)
            sys.exit(1)
        recs = parse_docx(fp)
        n_mismatch = sum(1 for r in recs if r['mismatch'])
        n_null = sum(1 for r in recs if r['correct'] is None)
        kept = [r for r in recs if not r['mismatch'] and r['correct'] is not None]
        print(f'{fn}: total={len(recs)} kept={len(kept)} mismatch={n_mismatch} null_correct={n_null}',
              file=sys.stderr)
        pools[n] = kept
    expected_pools = {0: 150, 1: 150, 2: 60, 3: 100}
    for s, exp in expected_pools.items():
        got = len(pools[s])
        if got != exp:
            raise ValueError(f'pool {s} ({FILES[s]}): expected {exp} kept, got {got}')
    print(f'seed={seed} pools=' + ','.join(f'{s}:{len(pools[s])}' for s in sorted(pools)),
          file=sys.stderr)
    print(f'seed={seed} pools=' + ','.join(f'{s}:{len(pools[s])}' for s in sorted(pools)))
    # proportional quota per 100Q mock: 33/33/13/21
    quota = {0: 33, 1: 33, 2: 13, 3: 21}
    rng = random.Random(seed)
    for p in pools.values():
        rng.shuffle(p)
    mocks, spare = [], []
    for m in range(4):
        take = []
        for s, q in quota.items():
            take += pools[s][m*q:(m+1)*q]
        if len(take) != 100:
            raise ValueError(f'mock {m+1}: expected 100, got {len(take)}')
        rng.shuffle(take)
        mocks.append(take)
    for s, p in pools.items():
        spare += p[4*quota[s]:]
    if sum(len(x) for x in mocks) != 400:
        raise ValueError(f'split must be 400, got {sum(len(x) for x in mocks)}')
    if len(spare) != 60:
        raise ValueError(f'spare must be 60, got {len(spare)}')
    general_fallbacks = sum(1 for p in pools.values() for r in p if not r['domain'])
    if general_fallbacks:
        print(f'warn: {general_fallbacks} records fell back to General topic', file=sys.stderr)
    else:
        print('General fallbacks: 0', file=sys.stderr)
    qdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'questions')
    for i, take in enumerate(mocks, 1):
        env = {'examId': f'aigp-practice-{i}', 'title': f'AIGP Practice Mock {i}',
               'description': 'IAPP AIGP-style mock: 100 scenario items. Exam-only timed practice; answers revealed after submit.',
               'version': '2026-10-04', 'durationMinutes': 165, 'passPercent': 70,
               'status': 'published',
               'questions': [to_portal(r, f'aigp-p{i}-{j:03d}') for j, r in enumerate(take, 1)]}
        atomic_write_text(os.path.join(qdir, f'aigp-practice-{i}.v2026-10-04.json'),
                          json.dumps(env, ensure_ascii=False, indent=2))
    atomic_write_text(os.path.join(qdir, 'aigp-spare-pool.v2026-10-04.json'),
                      json.dumps({'examId': 'aigp-spare-pool', 'title': 'AIGP Spare Pool', 'version': '2026-10-04',
                                  'durationMinutes': 60, 'passPercent': 70, 'status': 'draft',
                                  'questions': [to_portal(r, f'aigp-sp-{j:03d}') for j, r in enumerate(spare, 1)]},
                                 ensure_ascii=False, indent=2))
    print('wrote 4x100 + spare 60')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='AIGP docx bank parser + rebalancer.')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--parse-only', action='store_true', help='parse 4 docx and check total == 460')
    mode.add_argument('--rebalance', action='store_true', help='stratified rebalance into 4x100 + 60 spare')
    ap.add_argument('--seed', type=int, default=20261004, help='RNG seed for deterministic shuffle (default 20261004)')
    args = ap.parse_args()
    if args.rebalance:
        rebalance(args.seed)
        sys.exit(0)
    total = 0
    for fn in FILES:
        fp = os.path.join(SRC, fn)
        if not os.path.exists(fp):
            print(f'missing input file: {fp}', file=sys.stderr)
            sys.exit(1)
        recs = parse_docx(fp)
        print(f'{fn}: {len(recs)} records, mismatches={[i+1 for i, r in enumerate(recs) if r["mismatch"]][:10]}')
        total += len(recs)
    print(f'TOTAL {total}')
    if total != 460:
        raise ValueError(f'expected 460, got {total}')
