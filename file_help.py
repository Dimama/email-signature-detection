from os import listdir, mkdir, rename
from os.path import isfile, join



def get_all_files_and_clear():
    """delete all #sig# from file lines
    """
    mypath = 'dataset/with/'
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in files:
        with open(mypath + file, "r+") as f:
            lines = [line.replace("#sig#", '') for line in f.readlines()]
            f.seek(0)
            f.truncate()
            f.writelines(lines)
    


def get_all_files_and_rename():
    mypath = 'dataset/without/'
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files.sort()
    try:
        mkdir(mypath + "tmp")
    except Exception as e:
        print('tmp already exist') 
    for i, file in enumerate(files):
        new_name = mypath + "tmp/" + str(i) + "_sender"
        print(new_name)
        rename(mypath + file, new_name)
    print(files)


def main():
    get_all_files_and_clear()

if __name__ == '__main__':
    main()