def last_digit(idnum):
    '''
    Compute the last (18th) digit of a PRC Resident ID number
    ---------
    Input: idnum (string) the 18-digit ID number or the first 17 digits of an ID number
    Output: last (string) the last digit of the ID number
    '''
    S = 0
    for i in range(17): # the first 17 digits
        S += ((2.**(17 - i))%11) * int(idnum[i])
    last = (12 - (S % 11)) % 11 # what the last digit should be
    last = str(int(last)) if last < 10 else 'X'
    return last

def chek_id(idnum):
    '''
    Check if the last digit of a 18-digit PRC Resident ID number is correct
    ---------
    Input: idnum (string) the 18-digit ID number
    Output: (bool) whether the ID number is reasonable
    '''
    last = last_digit(idnum)
    if idnum[17] == last:
        print('The last digit of the ID number is correct.')
        return True
    else:
        print('The last digit of the ID number is NOT correct. It should be %s.'%last)
        return False

if __name__ == '__main__':
    from builtins import input
    id_tocheck = input('Enter a PRC Resident ID number: ')
    idcorrect = chek_id(id_tocheck)
