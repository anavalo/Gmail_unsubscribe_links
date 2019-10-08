import re
import pprint


def get_unsub_links(txt_file):
    text = open(txt_file).read()
    pp = pprint.PrettyPrinter(indent=4)
    urls = re.findall(r'(https?://\S+)',text)
    duplicates = {}
    print('Got ' + str(len(urls)) + ' URLs.')
    for url in urls:
        duplicates[url] = True
    print('Got ' + str(len(duplicates)) + ' Unsubscribe URLs. (duplicates included)')
    for k, v in duplicates.items():
        if any(re.findall(r'(U|u)nsub', k)):
            print(k)


def main():
    file = 'mail.txt'
    get_unsub_links(file)


if __name__ == '__main__':
    main()
