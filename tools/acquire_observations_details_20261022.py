#!/usr/bin/env python3
"""Follow two recovered official links; fixed public technical originals only."""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import acquire_transport_commercial_v2_20261021 as transport

BASE=transport.ROOT/'docs/program/execution/2026-10-22/observations-commercial-v1'
REQUESTS=(
 ('aws_er_manual','https://docs.aws.amazon.com/pdfs/entityresolution/latest/userguide/user-guide.pdf','pdf'),
 ('ibm_matching','https://www.ibm.com/docs/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.qs.ug.doc/topics/matchingcontainer.html','html'),
)

def main():
 p=argparse.ArgumentParser();p.add_argument('--retry-network',action='store_true');a=p.parse_args()
 transport.BASE=BASE;attempt='network-details' if a.retry_network else 'sandbox-details'
 if a.retry_network:
  for name,_,_ in REQUESTS:
   old=json.loads((BASE/'acquisition/sandbox-details'/(name+'.receipt.json')).read_text())
   assert old['returncode'] in (5,6,7)
 with ThreadPoolExecutor(max_workers=2) as pool:
  for r in pool.map(lambda x:transport.acquire(x,attempt),REQUESTS):print(json.dumps(r),flush=True)

if __name__=='__main__':main()
