'''
Handle pickle load/dump for python2 and python3
'''
import pickle, gzip, sys

def pkdump(data, pfile, verbose=True):
        '''
        Save *.pickle files
        '''
        with open(pfile,'wb') as f:
                if sys.version_info.major == 2: pickle.dump(data, f)
                if sys.version_info.major == 3: pickle.dump(data, f, protocol=2)
        if verbose: print('Saved:%s'%pfile)

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

def pkdumpgzip(data, pfile, verbose=True):
        '''
        Save *.pzip files
        '''
        with gzip.open(pfile,'wb') as f:
                if sys.version_info.major == 2: pickle.dump(data, f)
                if sys.version_info.major == 3: pickle.dump(data, f, protocol=2)
        if verbose: print('Saved:%s'%pfile)

def pkloadgzip(pfile, verbose=True):
        '''
        Load *.pzip files
        '''
        with gzip.open(pfile,'r') as f:
                if sys.version_info.major == 2: results = pickle.load(f)
                if sys.version_info.major == 3: results = pickle.load(f, encoding='latin1')
        if verbose: print('Loaded:%s'%pfile)
        return results
