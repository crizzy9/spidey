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
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(bfs_crawled):
        write_file(bfs_crawled, '')


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
        print("Loading file:", file_name)
        if os.path.getsize(file_name) > 0:
            with open(file_name, "rb") as handle:
                dic = pickle.load(handle)
            return dic
    else:
        print("Creating file:", file_name)
        f = open(file_name, "wb+")
        f.close()
        return {}


def dict_to_file(graph, file_name):
    # could be stored by converting dict to string
    # but pickle provides better compression
    with open(file_name, "wb") as handle:
        pickle.dump(graph, handle, protocol=pickle.HIGHEST_PROTOCOL)


def index_to_str_file(dic, file_name):
    with open(file_name, "w+") as file:
        for key, value in dic.items():
            file.write(key + ":" + str(value) + '\n')


def dict_to_str_file(graph, file_name):
    with open(file_name, "w+") as file:
        for key in graph.keys():
            line = key + ' '
            for elem in graph[key]:
                line += elem + ' '
            file.write(line.strip() + '\n')

# def str_file_to_dict(dic, file_name):
#     with open(file_name, 'r') as file:


def get_domain_name(url):
    try:
        return "https://" + urlparse(url).netloc
    except:
        return ''


def get_url_title(url):
    url_split = url.split('/')
    return url_split[len(url_split) - 1]


def get_titles_for_urls(urls):
    titles = []
    for url in urls:
        titles.append(get_url_title(url))
    return titles


def store_document(page_name, page_url, body_content):
    path = os.path.join(DOCUMENTS_DIR, str(page_name))
    if os.path.isfile(path):
        print("FILE ALREADY EXISTS\nPATH:", path)
    page_title = page_name.lower().translate(str.maketrans({'_': ' ', '(': '', ')': ''}))
    new_content = page_title + "\n " + str(body_content)
    try:
        create_dir(DOCUMENTS_DIR)
        if not os.path.isfile(path):
            write_file(path, new_content)
            print("Document stored at:", path)
    except:
        print("Error while storing document...\nNAME: " + page_name + " URL: " + page_url)
