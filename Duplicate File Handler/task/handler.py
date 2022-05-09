# write your code here
import os
import sys
import hashlib
from collections import defaultdict

args = sys.argv

if len(args) == 1:
    print('Directory is not specified')
else:
    extension = input('Enter file format:')
    print('''Size sorting options:
                1. Descending
                2. Ascending\n''')
    sort = '0'
    while sort not in '12':
        sort = input('Enter a sorting option:\n')
        if sort in '12':
            break
        else:
            print('Wrong option\n')

    sort = sort == '1'

    file_dic = defaultdict(list)
    hash_dic = defaultdict(list)
    print(extension)
    for root, dirs, files in os.walk(args[1]):
        for name in files:
            if extension in os.path.splitext(name)[1]:
                size = os.path.getsize(os.path.join(root, name))
                filename = os.path.join(root, name)
                file_dic[size].append(filename)
                with open(filename, 'rb') as file:
                    filehash = hashlib.md5(file.read())
                    key = (size, filehash.hexdigest())
                    hash_dic[key].append(filename)
    for key, value in sorted(file_dic.items(), reverse=sort):
        print(key, 'bytes')
        for file in value:
            print(file)

    askhash = '0'
    while askhash not in 'yesno':
        askhash = input('Check for duplicates?')
        if askhash not in 'yesno':
            print('Wrong option')

    # print(hash_dic)
    lastkey = 0
    number = 1
    duplicate_dict = {}
    for key, value in sorted(hash_dic.items(), reverse=sort):
        if len(value) > 1:
            if key[0] != lastkey:
                print()
                print(key[0], 'bytes')
                lastkey = key[0]

            print('Hash:', key[1])

            for i in value:
                print(str(number) + '. ' + i)
                duplicate_dict[number] = i
                number +=1



    deletefiles = '0'
    while deletefiles not in 'yesno':
        deletefiles = input('Delete files?')
        if deletefiles not in 'yesno':
            print('Wrong option')
        elif deletefiles == 'no':
            sys.exit()

    deletefiles_str = 'z'
    bad_string = True
    maxfiles = number
    while bad_string:
        deletefiles_str = input('Enter file numbers to delete:').strip()
        deletefiles_lst = deletefiles_str.split()
        error = 0
        if deletefiles_str == '':
            print('Wrong option')
            error += 1

        else:
            for i in deletefiles_lst:
                if i not in '0123456789'[:maxfiles]:
                    print('Wrong option')
                    error += 1
        if error == 0:
            bad_string = False

    deletefiles_lst = list(map(int, deletefiles_lst))

    freed_space = 0
    print(deletefiles_lst)
    print(duplicate_dict.items())
    for no, link in duplicate_dict.items():
        if no in deletefiles_lst:
            freed_space += os.path.getsize(link)
            print(link)
            os.remove(link)


    print(f'Total freed up space: {freed_space} bytes')