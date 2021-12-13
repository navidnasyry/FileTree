import zipfile
import os
from io import StringIO
from io import BytesIO
import pprint
import hashlib

import shutil

#dictionary of directorys
hash_list = [

]
dir_dict = {

}
MAIN_LIST = [

    ]
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def search(my_list, p_value, new_dic):
    #print(p_value)
    #pprint.pprint(my_list)
    if len(p_value) == 0:
        my_list.append(new_dic)
        new_index = len(my_list) - 1
        # create new value
        my_list[new_index]["value"] += str(new_index)+','
        return my_list[new_index]["value"]

    return search(my_list[int(p_value[0])]['children'], p_value.removeprefix(p_value[0]+','), new_dic)




def zipwalk(zfilename, children, parrent_value, password= '', pzip_name= ''):

    tempdir = os.environ.get('TEMP', os.environ.get('TMP', os.environ.get('TMPDIR', '/tmp')))

    try:
        z = zipfile.ZipFile(zfilename, 'r')
        z.setpassword(pwd=bytes(password, 'utf-8'))

        for info in z.infolist():
            fname = info.filename
            data = z.read(fname)
            extn = (os.path.splitext(fname)[1]).lower()

            if extn == '.zip':
                checkz = False
                tmpfpath = os.path.join(tempdir, os.path.basename(fname))
                #print("tmpfpath : " + tmpfpath)
                try:
                    open(tmpfpath, 'w+b').write(data)
                except IOError | OSError as e:
                    pass

                if zipfile.is_zipfile(tmpfpath):
                    checkz = True

                if checkz:
                    try:
                        zip_size = os.path.getsize(tmpfpath)
                        absolute_name = pzip_name + fname + '/'
                        # children.append({
                        #     "label": absolute_name,
                        #     "value": parrent_value,
                        #     "type": 'zip',
                        #     "size": zip_size,
                        #     "children": [
                        #
                        #     ]
                        # })
                        new_index = len(children) - 1
                        # # create new value
                        # children[new_index]["value"] += str(new_index)+','

                        #pprint.pprint(MAIN_LIST)
                        #pprint.pprint(dir_dict)
                        dir_path_1 = absolute_name.removesuffix('/')
                        pdir_path = dir_path_1.removesuffix(dir_path_1.split('/')[-1])
                        p_value = dir_dict[pdir_path]
                        new_dic = {
                            "label": absolute_name,
                            "value": p_value,
                            "type": 'folder',
                            "duplicate": False,
                            "size": zip_size,
                            "children": [

                            ]
                        }
                        dir_val = search(MAIN_LIST, p_value, new_dic);
                        dir_dict[absolute_name] = dir_val

                        for x in zipwalk(tmpfpath, children[new_index]["children"], children[new_index]["value"], "", absolute_name):
                            yield x
                    except Exception as e:
                        raise

                try:
                    os.remove(tmpfpath)
                except:
                    pass

            # ===================== folder ===========================================
            elif fname[-1] == '/':
                if os.path.isdir(fname):
                    folder_size = os.path.getsize(fname)
                else:
                    folder_size = info.file_size

                absolute_name = pzip_name + fname

                dir_path_1 = absolute_name.removesuffix('/')
                pdir_path = dir_path_1.removesuffix(dir_path_1.split('/')[-1])
                p_value = dir_dict[pdir_path]
                new_dic = {
                    "label": absolute_name,
                    "value": p_value,
                    "type": 'folder',
                    "duplicate": False,
                    "size": folder_size,
                    "children": [

                    ]
                }
                dir_val = search(MAIN_LIST, p_value, new_dic);
                dir_dict[absolute_name] = dir_val

                continue


            # ===================== file =============================================
            else:

                absolute_name = pzip_name + info.filename

                # if hash_file in hash_list:
                #     duplicate_bool = True
                # else:
                #     duplicate_bool = False

                p_value = dir_dict[absolute_name.removesuffix(info.filename.split('/')[-1])]
                new_dic = {
                    "label": absolute_name,
                    "value": p_value,
                    "type": 'file',
                    "duplicate": False,
                    "size": info.file_size,
                    "children": [

                    ]
                }

                search(MAIN_LIST, p_value, new_dic);
                yield (info, BytesIO(data))

    except RuntimeError as e:
        print('Runtime Error')



if __name__ == "__main__":
    import sys

    base_name = sys.argv[1]

    file_size = os.path.getsize(sys.argv[1])
    passwd = input("Enter you file Password : ")
    format = base_name.split('.')[-1]
    if format == 'zip':
        type = 'zip'
    else:
        type = 'file'

    hash_file = md5(base_name)
    root_dic = {
        "label": base_name,
        "value": '0,',
        "type": type,
        "size": file_size,
        "duplicate": False,
        "children": [

        ]
    }
    MAIN_LIST.append(root_dic)
    absolute_name = base_name + '/'
    dir_dict[absolute_name] = '0,'
    hash_list.append(hash_file)
    if type == 'zip':
        for i, d in zipwalk(sys.argv[1], MAIN_LIST[0]["children"], MAIN_LIST[0]["value"], password= passwd, pzip_name= absolute_name):
            #print(i.filename)
            # print(i.compress_size)
            # print(i.file_size)
            # print(d)
            pass

    pprint.pprint(MAIN_LIST)

