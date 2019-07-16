import ftplib
import os
import sys

def upload_dir(path_source, session, target_dir=None):
    files = os.listdir(path_source)
    # �ȼ�ס֮ǰ���ĸ�����Ŀ¼��
    last_dir = os.path.abspath('.')
    # Ȼ���л���Ŀ�깤��Ŀ¼
    os.chdir(path_source)

    if target_dir:
        current_dir = session.pwd()
        try:
            session.mkd(target_dir)
        except Exception:
            pass
        finally:
            session.cwd(os.path.join(current_dir, target_dir))

    for file_name in files:
        current_dir = session.pwd()
        if os.path.isfile(path_source + r'/{}'.format(file_name)):
            upload_file(path_source, file_name, session)
        elif os.path.isdir(path_source + r'/{}'.format(file_name)):

            current_dir = session.pwd()
            try:
                session.mkd(file_name)
            except:
                pass
            session.cwd("%s/%s" % (current_dir, file_name))
            upload_dir(path_source + r'/{}'.format(file_name), session)

        # ֮ǰ·�������Ѿ��������Ҫ�ٻظ���֮ǰ��·����
        session.cwd(current_dir)

    os.chdir(last_dir)


def upload_file(path, file_name, session, target_dir=None, callback=None):
    # ��¼��ǰ ftp ·��
    cur_dir = session.pwd()

    if target_dir:
        try:
            session.mkd(target_dir)
        except:
            pass
        finally:
            session.cwd(os.path.join(cur_dir, target_dir))

    print("path:%s \r\n\t   file_name:%s" % (path, file_name))
    file = open(os.path.join(path, file_name), 'rb')  # file to send

    session.storbinary('STOR %s' % file_name, file, callback = callback)  # send the file
    file.close()  # close file
    session.cwd(cur_dir)

upload_dir('D:\��������ѧSSL-2019060101',ftplib.FTP(host='199.200.0.3',user='test',passwd='test'))