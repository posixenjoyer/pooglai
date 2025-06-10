from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file


def main():
    '''
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "../"))
    print(get_files_info("calculator", "/bin/cat"))
    print(get_file_contents("calculator", "main.py"), end="")
    print(get_file_contents("calculator", "pkg/calculator.py"), end="")
    print(get_file_contents("calculator", "/bin/cat"), end="")
    '''

    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()
