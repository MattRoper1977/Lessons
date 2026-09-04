#!/usr/bin/env python3
"""Refresh only explicitly listed, digest-bound campaign decks. No week inference."""
import argparse
import hashlib
import json
from pathlib import Path
from lxml import html as lh
from classroom_presentation import apply

ROOT = Path(__file__).resolve().parents[2]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def retained(tree):
    """Independent invariant: preserve source data, teaching, figures and runtime."""
    cfg = tree.xpath('//script[@id="lesson-config"]')[0]
    stages = tree.xpath('//main[contains(@class,"deck")]/section[contains(@class,"slide")]')
    return {
        'config':json.loads(cfg.text),
        'timings':[(s.get('data-min'),s.get('data-minutes')) for s in stages],
        'scripts':[(s.get('id'),s.get('src'),s.text) for s in tree.xpath('//script')],
        'figures':[lh.tostring(n,encoding='unicode') for n in tree.xpath('//svg')],
        'print':[lh.tostring(n,encoding='unicode') for n in tree.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," print-pack ")]')],
        'teaching':[[n.text_content() for n in s.xpath('./p|./ul|./ol|./h3|./div[@data-mbm-guide]')] for s in stages],
    }


def refresh(targets, write=False):
    records=[]
    for row in targets['decks']:
        file=ROOT/row['file']
        if not file.resolve().is_relative_to(ROOT): raise ValueError('Target outside repository')
        raw=file.read_bytes()
        if digest(raw)!=row['sha256']: raise ValueError('Source changed: '+row['file'])
        tree=lh.fromstring(raw.decode('utf-8')); before=retained(tree); cfg=before['config']
        apply(tree,cfg['family'],cfg['title'])
        out=lh.tostring(tree,encoding='unicode',doctype='<!doctype html>').encode('utf-8')
        after=retained(lh.fromstring(out.decode('utf-8')))
        if before!=after: raise ValueError('Teaching/data/runtime changed: '+row['file'])
        again=lh.fromstring(out.decode('utf-8'));apply(again,cfg['family'],cfg['title'])
        if lh.tostring(again,encoding='unicode',doctype='<!doctype html>').encode('utf-8')!=out:
            raise ValueError('Presentation refresh is not idempotent: '+row['file'])
        if write:file.write_bytes(out)
        records.append({'file':row['file'],'beforeSha256':digest(raw),'sha256':digest(out),
                        'preserved':['lesson-config','timings','scripts','figures','print pack','teaching'],
                        'idempotent':True,'family':cfg['family']})
    return {'file':'tools/easter/refresh_classroom_presentation.py','newLessonUnits':0,
            'files':len(records),'applied':write,'rows':records}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--targets',required=True);parser.add_argument('--write',action='store_true')
    parser.add_argument('--output',required=True)
    args=parser.parse_args(); targets=json.loads(Path(args.targets).read_text())
    report=refresh(targets,args.write)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(report,indent=1)+'\n')
    print(f"{report['files']} decks; teaching, data, figures, print and runtime retained; idempotent")


if __name__=='__main__':main()
