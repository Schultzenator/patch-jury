"""Original, deliberately small regressions. No third-party code."""
from decimal import Decimal, ROUND_HALF_UP

FIXTURES = {
 'pages': {
  'title': 'The page that disappeared',
  'spec': 'pages(total, size): number of pages for nonnegative integer total and positive integer size. Empty input needs zero pages. Integer ceiling division.',
  'function': 'pages',
  'base': 'def pages(total, size):\n    return total // size\n',
  'patch_a': 'def pages(total, size):\n    return total // size + 1\n',
  'patch_b': 'def pages(total, size):\n    return (total + size - 1) // size\n',
  'smoke': [[11,10]], 'examples': [[0,10],[20,10],[21,10]],
  'hidden': [[1,1],[99,3],[100,3],[0,1],[10000,100]],
 },
 'money': {
  'title': 'A cent is not a rounding error',
  'spec': 'cents(amount): convert a nonnegative decimal string with up to 3 fractional digits to integer cents, using decimal ROUND_HALF_UP. Values from 0 to 1000000.',
  'function': 'cents',
  'base': 'def cents(amount):\n    return int(float(amount) * 100)\n',
  'patch_a': 'def cents(amount):\n    return round(float(amount) * 100)\n',
  'patch_b': 'from decimal import Decimal, ROUND_HALF_UP\ndef cents(amount):\n    return int((Decimal(amount) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))\n',
  'smoke': [['1.999']], 'examples': [['1.005'],['0.145'],['2.675']],
  'hidden': [['0.005'],['10.125'],['1.015'],['999.995'],['0.004']],
 },
 'intervals': {
  'title': 'The meeting at the boundary',
  'spec': 'overlap(a,b): whether two nonempty half-open integer intervals [start,end) share any point. Inputs each have two integers with start < end. Touching endpoints are not overlap.',
  'function': 'overlap',
  'base': 'def overlap(a, b):\n    return a[0] < b[0] < a[1]\n',
  'patch_a': 'def overlap(a, b):\n    return max(a[0], b[0]) <= min(a[1], b[1])\n',
  'patch_b': 'def overlap(a, b):\n    return max(a[0], b[0]) < min(a[1], b[1])\n',
  'smoke': [[[1,5],[0,3]]], 'examples': [[[1,3],[3,5]],[[1,5],[1,5]],[[2,3],[0,8]]],
  'hidden': [[[-5,0],[0,5]],[[0,1],[-1,0]],[[1,2],[1,2]],[[0,10],[2,4]],[[1,2],[3,4]]],
 },
}

def expected(fixture, args):
    # Validate *all* values before using them or sending them to a container.
    if fixture == 'pages':
        if len(args)!=2 or any(type(v) is not int for v in args) or not (0<=args[0]<=1000000 and 1<=args[1]<=1000000):
            raise ValueError('Expected [total>=0, size>0], integers <=1000000')
        return (args[0]+args[1]-1)//args[1]
    if fixture == 'money':
        import re
        if len(args)!=1 or not isinstance(args[0],str) or not re.fullmatch(r'\d{1,7}(\.\d{1,3})?',args[0]) or Decimal(args[0])>1000000:
            raise ValueError('Expected a decimal string in range 0..1000000')
        return int((Decimal(args[0])*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    if fixture == 'intervals':
        if len(args)!=2 or any(not isinstance(v,list) or len(v)!=2 or any(type(x) is not int or abs(x)>1000000 for x in v) or v[0]>=v[1] for v in args):
            raise ValueError('Expected two nonempty integer intervals')
        return max(args[0][0],args[1][0])<min(args[0][1],args[1][1])
    raise ValueError('Unknown fixture')

def validate_cases(fixture, cases):
    if not isinstance(cases,list) or not 1<=len(cases)<=12:
        raise ValueError('Expected 1..12 test cases')
    seen=set()
    import json
    for args in cases:
        if not isinstance(args,list): raise ValueError('Each case must be an argument list')
        expected(fixture,args)
        key=json.dumps(args)
        if key in seen: raise ValueError('Duplicate case')
        seen.add(key)
    return cases
