from typing import Tuple, List

def compress_(s):

  def f_(x: str) -> Tuple[str, int]: 
    ''' count how many repeats, ignore rest of string'''
    a = x[0]
    r = ''
    for k in range(len(x)): 
      if x[k]!=a: 
        return (a, len(r))
      else: 
        r += x[k]
    
    return (a, len(r))

  def f(x: str) -> List[Tuple[str, int]]: 
    ''' ''' 
    if not x: 
      return []
    else: 
      t = f_(x)
      return [t] + f(x[t[1]:])

  return ''.join([f"{t[1]}{t[0]}" for t in f(s)])

def compress(s: str) -> str:
  """ """
  r = compress_(s)
  if len(r) < len(s): 
    return r
  else: 
    return s
  
a = compress('zzzzzzzkittypurrrr')
print(a)
print(a=="7z1k1i2t1y1p1u4r")

b = compress('yabbadabbadoooooooooooo')
print('yabbadabbadoooooooooooo')
print(b)
