# importing required modules
import PyPDF3
import os
import pandas as pd

# Dictionary
import docx
from docx.opc.exceptions import PackageNotFoundError
from xlrd import XLRDError

extensions = [".txt", ".png", ".docx", ".pdf", ".doc", "xls", "xlsx"]
bank_data = [["Bank", "28"], ["bank", "28"], ["Euro", "24"], ["euro", "24"], ["Confidentiel", "16"],
             ["confidentiel", "16"], ["dolard", "23"], ["Dolard", "23"], ["Contrat", "12"], ["contrat", "12"]]



def count_interisting_word(words_list):
    # Simple word counter over bank_data
    count = 0
    # Counter process
    for word in words_list:
        for data in bank_data:
            if data[0] == word:
                count = count + 1 * int(data[1])
    return count


def file_collection(path):
    files_return = []
    for (root, dirs, files) in os.walk(path, topdown=True):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    files_return.append(os.path.join(root, file))
    return files_return


def sort_by_priority(tmp_list):
    # Let's put vipers first ! (otherwise pivot problem)
    vip_files = []
    for x in tmp_list:
        if x[1] == -1:  # -1 means encrypted
            vip_files.append(x[0])
            tmp_list.remove(x)
    # If the list is empty we return nothing (for the recursive call)
    if not tmp_list:
        return []

    # Basic quick sort
    else:
        pivot = tmp_list[0]
        t1 = []
        t2 = []
        for x in tmp_list[1:]:
            if x[1] < pivot[1]:
                t1.append(x)
            else:
                t2.append(x)
        return sort_by_priority(t1) + [pivot[0]] + sort_by_priority(t2) + vip_files


def search_interisting_files(files_list):
    tmp_list = []
    # For each file of the list we calculate its score thanks to the function associated to its extension
    for file in files_list:
        if file.endswith('.pdf'):
            tmp_list.append(pdf_parser(file))
        elif file.endswith('.txt'):
            tmp_list.append(txt_parser(file))
        elif file.endswith('.docx'):
            tmp_list.append(docx_parser(file))
        elif file.endswith('.xlsx') or file.endswith('xls'):
            tmp_list.append(excel_parser(file))
    # We apply the sorting algorithm to return an ordered list
    priority_list = sort_by_priority(tmp_list)
    return priority_list


def excel_parser(file):
    try:

        # Opening the file
        workbook = pd.read_excel(file)
        words_list = []
        # Scrub the column headings
        for title in workbook.columns.values:
            words_list.append(title)
        # For each line
        for row in workbook.iterrows():
            for case in row[1]:
                # If the case is not empty
                if case != "NaN":
                    # We put it in the form of a word table
                    words_list.append(case)
        # We check the number of interesting words
        count = count_interisting_word(words_list)
        return [file, count]
    except XLRDError:
        # If the excel is encrypted we flag it -1
        return [file, -1]
    # If the file is unreadable, it becomes less interesting
    except:
        return [file, 0]


def pdf_parser(file):
    count = 0
    try:
        # Opening the file
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF3.PdfFileReader(pdfFileObj)
        # If the pdf is encrypted we flag it -1
        if pdfReader.isEncrypted:
            count = -1
            return [file, count]
        else:
            # For each page
            for i in range(0, pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                # We extract the text
                var = pageObj.extractText()
                # We put it in the form of a word table
                words_list = var.split(" ")
                # We check the number of interesting words
                count += count_interisting_word(words_list)
            pdfFileObj.close()
            return [file, count]
    # If the file is unreadable, it becomes less interesting
    except:
        return [file, 0]


def docx_parser(file):
    count = 0
    try:
        # Opening the file
        doc = docx.Document(file)
        fullText = []
        # for each paragraphs, we extract the text
        for para in doc.paragraphs:
            fullText.append(para.text)
        # For each line of text
        for line in fullText:
            # We put it in the form of a word table
            words_list = line.split(" ")
            # We check the number of interesting words
            count += count_interisting_word(words_list)
        return [file, count]
    # If the pdf is encrypted we flag it -1
    except PackageNotFoundError:
        return [file, -1]
    # If the file is unreadable, it becomes less interesting
    except:
        return [file, 0]


def txt_parser(file):
    try:
        # Opening the file
        file_ = open(file, mode='r', errors='ignore')
        # Extract lines
        lines = file_.readlines()
        # Close file
        file_.close()
        # We transform them into a list of words
        words_list = []
        for line in lines:
            for word in line.split(' '):
                words_list.append(word)
        # We check the number of interesting words
        count = count_interisting_word(words_list)
        return [file, count]
    # If the file is unreadable, it becomes less interesting
    except:
        return [file, 0]


def main():
    location = os.environ["USERPROFILE"] + "\Desktop\\testdir"
    files_list = search_interisting_files(file_collection(location))
    print(files_list)
    return files_list


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
