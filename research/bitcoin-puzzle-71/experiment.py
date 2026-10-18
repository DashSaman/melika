#!/usr/bin/env python3
"""Standard-library, lightweight audit; NO private-key search."""
import hashlib,random,math,json
A='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
TARGET='1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU'
def decode_address(s):
 n=0
 for c in s:n=n*58+A.index(c)
 b=n.to_bytes((n.bit_length()+7)//8,'big')
 b=bytes([0])*(len(s)-len(s.lstrip('1')))+b
 assert len(b)==25
 assert hashlib.sha256(hashlib.sha256(b[:-4]).digest()).digest()[:4]==b[-4:]
 return b[0],b[1:21].hex()
def control(seed=20261018,trials=3000):
 r=random.Random(seed);hits=0
 for _ in range(trials):
  train=[r.randrange(4) for i in range(60)]
  test=[r.randrange(4) for i in range(20)]
  pick=max(range(4),key=lambda x:train.count(x))
  hits+=test.count(pick)
 p=hits/(20*trials); se=math.sqrt(.25*.75/(20*trials))
 return {'synthetic_only':True,'seed':seed,'trials':trials,'accuracy':p,'chance':.25,'z_vs_null':(p-.25)/se}
if __name__=='__main__':
 v,h=decode_address(TARGET)
 rate=250_000_000
 print(json.dumps({'target':TARGET,'version':v,'hash160':h,'range_start':hex(2**70),'range_end':hex(2**71-1),'total_candidates':2**70,'illustrative_keys_per_second':rate,'illustrative_365_day_success_probability':rate*86400*365/(2**70),'synthetic_negative_control':control()},indent=2))
