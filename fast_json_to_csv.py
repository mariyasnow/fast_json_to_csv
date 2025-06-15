######################################################################
# @mariyasnow
# Armada Apple coding challenge Spring '18
# Usage: python ArmadaApple.py
"""
root@6f2bacadd356:/home# python ArmadaApple.py
python ArmadaApple.py
.........
----------------------------------------------------------------------
Ran 9 tests in 1.068s

OK
"""
# python --version
# Python 3.6.4
######################################################################

import unittest
import json
import urllib.request 
import subprocess

class TestMain(unittest.TestCase):
    """
    Run through all the problem cases with tests in place of input().strip() or argparse import
    shell scripts are wrapped in subprocess instead of a separate #!/bin/bash file
    to save myself typing
    """

    def test_main(self):
        """ template to save typing """
        actual = main()
        expected = True
        self.assertEqual(actual, expected)
    
    def test_prob_0(self):
        """
        Write a python program to rotate integer array elements by shift  
        (user-input). Do this without using another array or without 
        moving any element of the input array multiple times.
        """
        given_array = [10,11,14,15]
        actual = array_rotate(given_array, 3)
        expected = [11,14,15,10]
        self.assertEqual(actual, expected)

    def test_prob_1(self):
        """ 
        Write a python program to read input json from :   
        http://mysafeinfo.com/api/data?list=englishmonarchs&format=json
        and create list of uniq ‘nm’ by ‘cty' and ‘hse'.
        """
        
        json_dump = sort_by_nm("http://mysafeinfo.com/api/data?list=englishmonarchs&format=json")
        actual = len(json_dump)
        expected = 7270
        self.assertEqual(actual, expected)

    def test_prob_2(self):
        """
        3)  
        i - Write a python program to read input json from 
        http://mysafeinfo.com/api/data?list=englishmonarchs&format=json
        ii - and write the data to local file called  "/tmp/converter_input.json" 
        iii - Then create another file called  “/tmp/converter_input.csv" 
        to dump the data in csv file format.

        Don’t use python CSV modules.
        """
        #i
        d = read_json("http://mysafeinfo.com/api/data?list=englishmonarchs&format=json")
        write_to_file_json("/tmp/converter_input.json", d)
        actual = subprocess.getoutput('ls /tmp/converter_input.json')
        expected = '/tmp/converter_input.json'
        self.assertEqual(actual, expected)

        #ii
        tst = JsonToCSV(d)
        self.assertEqual(actual, expected)
        (headers, body) = tst.json_to_csv()
        write_to_file_csv("/tmp/converter_input.csv", headers, body)
        
        #iii
        actual = subprocess.getoutput('ls /tmp/converter_input.csv')
        expected = '/tmp/converter_input.csv'
        self.assertEqual(actual, expected)

    def test_prob_3(self):
        """ 
        4) Write a shell script to sum the sizes of all files in input dir.
        - Must be shell (no python)
        - Only include regular files (no directly, don’t follow any symlinks)
        - Print the size in bytes as well as human readable format
        """
        #human -h readable
        actual = subprocess.getoutput('du /tmp/* -ach | grep total')
        expected = '12K\ttotal'
        self.assertEqual(actual, expected)

        #non-human default K
        actual = subprocess.getoutput('du /tmp/* -ac | grep total')
        expected = '12\ttotal'
        self.assertEqual(actual, expected)

    """ 

    Secondary DEUBUG tests

    """
    def test_read_json(self):
        d = read_json("http://mysafeinfo.com/api/data?list=englishmonarchs&format=json")
        actual = isinstance(d, list)
        expected = True
        self.assertEqual(actual, expected)
        
    def test_JsonToCSV_flatten(self):
        d = {'one': {'one': [1,2,3], 'two': 'one'}, 'kl': 'vp'}
        prefix = ''
        tst = JsonToCSV(d)
        actual = tst.flatten(d, prefix)
        expected = {'kl': ['vp'], 'one__one': ['', '', [1, 2, 3]], 'one__two': ['', '', 'one']}
        self.assertEqual(actual, expected)
        
    def test_JsonToCSV_json_to_csv(self):
        d = {'one': {'one': [1,2,3], 'two': 'one'}, 'kl': 'vp'}
        tst = JsonToCSV(d)

        actual = tst.json_to_csv()
        expected = (['one__two', 'one__one', 'kl'], [['', '', 'vp']])
        self.assertEqual(sorted(actual[0]), sorted(expected[0]))
        #body
        self.assertEqual(sorted(actual[1]), sorted(expected[1]))
        
    def test_JsonToCSV_merge_d(self):
        ''' to do dummy dict'''
        actual = ''
        expected = ''
        self.assertEqual(actual, expected)
        
        
def array_rotate(arr, byn):
    ''' Write a python program to rotate integer array elements by shift  (user-input). 
    Do this without using another array or without moving any element of the input array 
    multiple times.'''
    
    n = len(arr)%byn
    if n == 0 or n==len(arr):
        return arr
    return arr[n:]+arr[:n]

def read_json(url):
    ''' Write a python program to read input json from :   
    http://mysafeinfo.com/api/data?list=englishmonarchs&format=json 
    '''
    with urllib.request.urlopen(url) as f:
        return json.loads(f.read().decode(f.info().get_param('charset') or 'utf-8'))

def sort_by_nm(url):
    ''' and create list of uniq ‘nm’ by ‘cty' and ‘hse' '''
    d = read_json(url)
    cdict = JsonToCSV(d)
    
    headers, body = cdict.json_to_csv()
    nm = headers.index('nm')
    cty = headers.index('cty')
    hse = headers.index('hse')

    unique_nm = ()
    list_of_uniq = []
    for ln in body:
        if ln[nm] not in unique_nm:
            list_of_uniq.extend([{ln[cty]:{ln[hse]: [ln[nm]]}}])
    return json.dumps(list_of_uniq, indent=4)

""" WR helper stuff ...boring but reusable"""
def write_to_file_csv(filename, headers, body):
    with open(filename, 'w') as f:
        #headers
        f.write(', '.join(list(headers)))
        f.write('\r\n')
        #body
        for ln in body:
            f.write(', '.join(ln))
            f.write('\r\n')

def write_to_file_json(filename, d):
    ''' write json to filename '''
    with open(filename, 'w') as f:
        json.dump(d, f,indent=4)
        
def read_json_file(filename):
    ''' Simple small csv for tests'''
    with open("test.csv", "r") as f:
        d = json.loads(f.read())
    k = JsonToCSV(d)
    headers, body = k.json_to_csv()
    return headers, body
    
        
class JsonToCSV():

    """ 
    Group JsonToCSV  specific methods
    unlike stdlib.csv doesn't require headers and works on generic json inputs
    also unlike stdlib needs more error handling, extra type handling, and less lazy one-liners 
    """
    
    def __init__(self, json_d):
        self.d = json_d

    def json_to_csv(self):
        ''' and write the data to local file called  "/tmp/converter_input.json" 
        Then create another file called  “/tmp/converter_input.csv" to dump 
        the data in csv file format.
        Don’t use python CSV modules.'''

        flatD = self.flatten(self.d, '')

        headers = list(flatD.keys())
        body_t = flatD.values()

        #transpose the mtrx
        body = [list(x) for x in zip(*body_t) if len(''.join(x))!=0]
        return headers, body

    @staticmethod
    def flatten(d, prefix):
        ''' flatten json to a dict with {header: [list, of, values]} modified tree walk-ish'''

        if len(d) == 0:
            return {}
        
        else:
            res = {}
            delim = '__' if prefix else ''

            #TODO other type checks
            if isinstance(d, list):
                for v in d:
                    res = JsonToCSV.merge_d(res, JsonToCSV.flatten(v, prefix))

            else:
                for k,v in d.items():
                    #new header key
                    nk = '{}{}{}'.format(prefix,delim,k)

                    if not isinstance(v, dict):
                        #easy case reach node end
                        if nk in res.keys():
                            res[nk] = res[nk].append(v)
                        else:
                            res[nk] = [v]
                    else:
                        #got more nested json
                        res = JsonToCSV.merge_d(res, JsonToCSV.flatten(v, nk))
            return res

    @staticmethod
    def merge_d(a,b):
        ''' custom merge to extend dict values as lists vs set(**a, **b) shallow merge'''
        #TODO check for dict
        merged_d = {}
        merged_keys = set(list(b.keys()) + list(a.keys()))

        for k in merged_keys:
            extended_list = merged_d.get(k, ['']) + a.get(k, ['']) + b.get(k, [''])
            #non-empty check 
            if len( ''.join(map(str, extended_list)))!= 0:
                merged_d[k] = extended_list

        return merged_d

def main():
    return True

if __name__ == '__main__':
    unittest.main()
