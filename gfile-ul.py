import argparse
from gfile import GFile

def upload_folder(folder,output):
    for x in sorted(os.listdir(folder)):
        url = GFile(x, progress=True).upload().get_download_page()
        print(url)

def main():
    parser.add_argument('folder', help='Folder name')
    args = parser.parse_args()

    folder = args.folder

    upload_folder(folder,filename)

if __name__ == '__main__':
    main()
