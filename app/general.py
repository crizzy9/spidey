import os
import pickle
from urllib.parse import urlparse

DOCUMENTS_DIR = 'documents'


def create_dir(directory):
    if not os.path.exists(directory):
        print("Creating directory: " + directory)
        os.makedirs(directory)


def create_data_files(dir_name, base_url):
    queue = os.path.join(dir_name, 'queue.txt')
    bfs_crawled = os.path.join(dir_name, "bfs_crawled.txt")
    # dfs_crawled = os.path.join(dir_name, "dfs_crawled.txt ")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(bfs_crawled):
        write_file(bfs_crawled, '')
    # if not os.path.isfile(dfs_crawled):
    #     write_file(dfs_crawled, '')


def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def add_to_file(path, data):
    with open(path, 'a') as file:
        file.write(str(data) + '\n')


def check_for_duplicate_data(path, data):
    with open(path, 'r') as file:
        if data in file.readlines():
            return True
        else:
            return False


def truncate_file(path):
    with open(path, 'w'):
        pass


def file_to_arr(file_name):
    results = []
    with open(file_name, "rt") as f:
        for line in f:
            results.append(line.strip().replace('\n', ''))
    return results


def arr_to_file(links, file):
    truncate_file(file)
    for link in links:
        add_to_file(file, link)
    return file


def file_to_dict(file_name):
    if os.path.isfile(file_name):
        print("Loading graph file:", file_name)
        if os.path.getsize(file_name) > 0:
            with open(file_name, "rb") as handle:
                dic = pickle.load(handle)
            return dic
    else:
        print("Creating graph file:", file_name)
        f = open(file_name, "wb+")
        f.close()
        return {}


def dict_to_file(graph, file_name):
    # could be stored by converting dict to string
    # but pickle provides better compression
    with open(file_name, "wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_domain_name(url):
    try:
        return "https://" + urlparse(url).netloc
    except:
        return ''


# change to store multiple documents in 1 document
def store_document(name, title, page_url, body_content):
    path = os.path.join(DOCUMENTS_DIR, str(name))
    new_content = "URL: " + page_url + "\n\n" + "TITLE: " + title + "\n\n" + str(body_content)
    try:
        create_dir(DOCUMENTS_DIR)
        if not os.path.isfile(path):
            write_file(path, new_content)
            print("Document stored at:", path)
    except:
        print("Error while storing document...\nNAME: " + title + " URL: " + page_url)
