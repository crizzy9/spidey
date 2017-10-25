import os
from urllib.parse import urlparse

DOCUMENTS_DIR = 'documents'


def create_dir(directory):
    if not os.path.exists(directory):
        print("Creating directory: " + directory)
        os.makedirs(directory)


def create_data_files(dir_name, base_url):
    queue = os.path.join(dir_name, 'queue.txt')
    crawled = os.path.join(dir_name, "crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def add_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


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
            results.append(line.replace('\n', ''))
    return results


def arr_to_file(links, file):
    truncate_file(file)
    for link in links:
        add_to_file(file, link)
    return file


def get_domain_name(url):
    try:
        return "https://" + urlparse(url).netloc
    except:
        return ''


# change to store multiple documents in 1 document
def store_document(name, header, page_url, body_content):
    path = os.path.join(DOCUMENTS_DIR, str(name))
    new_content = "URL: " + page_url + "\n\n" + "HEADER: " + header + "\n\n" + str(body_content)
    try:
        create_dir(DOCUMENTS_DIR)
        if not os.path.isfile(path):
            write_file(path, new_content)
            print("Document stored at:", path)
    except:
        print("Error while storing document...\nNAME: " + header + " URL: " + page_url)