'''
Handle pickle load for python2 and python3
'''
import pickle, gzip, sys

def pkload(pfile, verbose=True):
        '''
        Load *.pickle files
        '''
        if sys.version_info.major == 2:
                with open(pfile, 'r') as f: results = pickle.load(f)
        if sys.version_info.major == 3:
                with open(pfile, 'rb') as f: results = pickle.load(f, encoding='latin1')
        if verbose: print('Loaded:%s'%pfile)
        return results

def pkloadgzip(pfile, verbose=True):
        '''
        Load *.pzip files
        '''
        with gzip.open(pfile,'r') as f:
                if sys.version_info.major == 2: results = pickle.load(f)
                if sys.version_info.major == 3: results = pickle.load(f, encoding='latin1')
        if verbose: print('Loaded:%s'%pfile)
        return results
