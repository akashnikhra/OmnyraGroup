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
    root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
    # answer key: first table, rows of Q#/Ans pairs
    key = {}
    tables = root.findall('.//w:tbl', NS)
    if tables:
        for row in tables[0].findall('w:tr', NS)[1:]:
            cells = [ ''.join((t.text or '') for t in c.findall('.//w:t', NS)).strip()
                      for c in row.findall('w:tc', NS) ]
            for i in range(0, len(cells) - 1, 2):
                if cells[i].isdigit() and cells[i+1] in 'ABCD':
                    key[int(cells[i])] = 'ABCD'.index(cells[i+1])
    # green-marked correct option per question block
    paras = []
    for p in root.findall('.//w:p', NS):
        txt = ''.join((t.text or '') for t in p.findall('.//w:t', NS)).strip()
        if not txt:
            continue
        green = None
        for r in p.findall('w:r', NS):
            for c in r.findall('w:rPr/w:color', NS):
                v = (c.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') or '').lower()
                if v in GREEN:
                    ttxt = ''.join((t.text or '') for t in r.findall('w:t', NS)).strip()
                    m = re.match(r'^([A-D])\.', ttxt)
                    if m:
                        green = 'ABCD'.index(m.group(1))
        paras.append((txt, green))
    # block-split on "Question N"
    recs, cur = [], None
    def flush():
        if cur and len(cur['options']) == 4:
            recs.append(cur)
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

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='AIGP docx bank parser (Task 1: parse-only).')
    ap.add_argument('--parse-only', action='store_true', help='parse 4 docx and assert total == 460')
    ap.add_argument('--rebalance', action='store_true', help='Task 2 entry point (not implemented yet)')
    args = ap.parse_args()
    if args.rebalance:
        print('rebalance lands in Task 2 (not implemented)')
        sys.exit(2)
    total = 0
    for fn in FILES:
        recs = parse_docx(os.path.join(SRC, fn))
        print(f'{fn}: {len(recs)} records, mismatches={[i+1 for i, r in enumerate(recs) if r["mismatch"]][:10]}')
        total += len(recs)
    print(f'TOTAL {total}')
    assert total == 460, f'expected 460, got {total}'
