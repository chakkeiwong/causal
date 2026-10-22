#!/usr/bin/env python3
"""Inert stdlib HTML/PDF extraction; originals remain authoritative."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess

BASE=Path(__file__).resolve().parents[1]/'docs/program/execution/2026-10-22/observations-commercial-v1'
class Text(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,attrs):
        if t in ('script','style','nav','header','footer'):self.skip+=1
        if not self.skip and t in ('p','div','h1','h2','h3','h4','li','tr','td','pre','br'):self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('script','style','nav','header','footer'):self.skip=max(0,self.skip-1)
        if not self.skip and t in ('p','div','h1','h2','h3','h4','li','tr','td','pre'):self.parts.append('\n')
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)

def main():
    out=BASE/'extracted';out.mkdir(exist_ok=True)
    for f in sorted((BASE/'acquisition').glob('network*/*.html')):
        h=Text();h.feed(f.read_text());body='\n'.join(s.strip() for s in ''.join(h.parts).split('\n') if s.strip())+'\n'
        target=out/(f.stem+'.txt')
        if target.exists():assert target.read_text()==body
        else:target.write_text(body)
    for f in sorted((BASE/'acquisition').glob('network*/*.pdf')):
        target=out/(f.stem+'.txt')
        if not target.exists():
            subprocess.run(['pdftotext','-layout',str(f),str(target)],check=True,timeout=30)
            (out/(f.stem+'.pdfinfo.txt')).write_bytes(subprocess.check_output(['pdfinfo',str(f)],timeout=15))
    print('Preserved HTML text and PDF extractions; no image inspection or native execution.')

if __name__=='__main__':main()
