import contextlib
import time


import dropbox

def gettoken():
    ACCESS_TOKEN = '';
    with open('token.nogit') as f:
        ACCESS_TOKEN = f.readline();
    return ACCESS_TOKEN.strip();

def main():
    ACCESS_TOKEN = gettoken();

    dbx = dropbox.Dropbox(ACCESS_TOKEN);
    print(ACCESS_TOKEN);

    print(dbx.users_get_current_account());

    names = [];


    for entry in dbx.files_list_folder('/TeamCode', recursive=False).entries:
        print(entry.name);
        names.append(entry.name);

    listing = list_folder(dbx, '/TeamCode');
    for n in names:
        md = listing[n];
        if (isinstance(md, dropbox.files.FileMetadata)):
            print('%s %s %d' %(n, md.client_modified.__str__(), md.size));
        if (isinstance(md, dropbox.files.FolderMetadata)):
            print('Folder: %s' %(n));
#

def listtree():
    ACCESS_TOKEN = gettoken();
    dbx = dropbox.Dropbox(ACCESS_TOKEN);


    with open('dropboxtree.dat', 'w') as f:
        prevpath = '';
        currpath = '';
        listofpaths = [''];
        while ():
            currpath = getlast(listofpaths);
            listing = list_folder(dbx, currpath);
            for l in listing:
                md = listing[l];
                if (isinstance(md, dropbox.files.FolderMetadata)):
                    listofpaths.append(currpath + '/' + md.name);
                

def getlast(listofstr):
    if listofstr:
        return listofstr[-1];
    return None
    

def howmanyfiles():
    ACCESS_TOKEN = gettoken();

    dbx = dropbox.Dropbox(ACCESS_TOKEN);

    with stopwatch('list_folder'):
        listing = list_folder(dbx, '',
                              isrecursive=True);


    num = 0;
    for n in listing:
        md = listing[n];
        if (isinstance(md, dropbox.files.FolderMetadata)):
            num = num+1;
            print(md.name);

    print(num);
    num = 0;
    totalsize = 0;
    with stopwatch('total size'):
        for n in listing:
            md = listing[n];
            if (isinstance(md, dropbox.files.FileMetadata)):
                num = num + 1;
                totalsize = totalsize + md.size;
    print(num);
    print('total size: %f Gbytes?' %(totalsize*1e-9));

def list_folder(dbx, path, isrecursive=False):
    """ list a folder

    Returns a dict maping unicode filenames to 
    FileMetadata|FolderMetadata entries.
    """
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path, recursive=isrecursive);
    except dropbox.exceptions.ApiError as err:
        print ('Folder listing failed for', 
                path, '-- assumped empty:', err);
        return {}
    else:
        rv = {};
        for entry in res.entries:
            rv[entry.name] = entry
        return rv;

@contextlib.contextmanager #decorates for 'with'
def stopwatch(message):
    """ prints show long a block of code took to run """
    t0 = time.time();
    try:
        yield;
    finally:
        t1 = time.time();
        print('Elapsed time for %s: %.3f' % (message, t1 - t0));

if __name__ == '__main__':
    howmanyfiles();
