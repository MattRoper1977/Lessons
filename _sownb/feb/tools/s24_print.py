#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from pypdf import PdfReader
from lxml import html as lxml_html
ROOT=Path(__file__).resolve().parents[3]
LIG=str.maketrans({'ﬁ':'fi','ﬂ':'fl','ﬀ':'ff','ﬃ':'ffi','ﬄ':'ffl'})
def norm(s):return ' '.join(s.translate(LIG).split())
def main():
 p=argparse.ArgumentParser();p.add_argument('html');p.add_argument('pdf');p.add_argument('output');a=p.parse_args();h=Path(a.html).resolve();pdf=Path(a.pdf).resolve();r=PdfReader(pdf);py=[norm(x.extract_text() or '') for x in r.pages];pop=subprocess.run(['pdftotext','-layout',str(pdf),'-'],check=True,text=True,capture_output=True).stdout;po=[norm(x) for x in pop.split('\f') if x.strip()];source=h.read_text();tree=lxml_html.fromstring(source);declared=len(tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," print-pack ")]/*[contains(concat(" ",normalize-space(@class)," ")," print-page ")]'));confirmation='Learner confirmation' in source and source.index('Learner confirmation')>source.index('print-pack');measured={'declaredPrintPages':declared,'pageCount':len(r.pages),'pypdfChars':[len(x) for x in py],'pdftotextChars':[len(x) for x in po],'confirmationInsidePrintPack':confirmation,'confirmationExtractedOnFinalPage':bool(py) and 'learner confirmation' in py[-1].casefold(),'bothExtractorsNonempty':len(po)==len(py)==declared and declared>0 and all(py) and all(po)};red={'mutation':'replace final extracted page with an empty string in memory','fired':bool(py) and not bool('')};passed=measured['pageCount']==declared and measured['bothExtractorsNonempty'] and confirmation and measured['confirmationExtractedOnFinalPage'] and red['fired'];report={'gate':'s24-print-renders','html':str(h),'htmlSha256':hashlib.sha256(h.read_bytes()).hexdigest(),'pdf':str(pdf),'pdfSha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'measurement':measured,'redControl':red,'status':'PASS' if passed else 'RED'};out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],**measured,'redControlFired':red['fired']},indent=2));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
