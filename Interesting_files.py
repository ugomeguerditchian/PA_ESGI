# importing required modules
import PyPDF2
import os

# Dictionary
import docx

extensions = [".txt", ".png", ".docx", ".pdf"]
bank_data = ["BIC", "Identité", "Bancaire", "toto", "Exemple", "fichier"]

def count_interisting_word(words_list):
    count = 0
    for word in bank_data:
        for w in words_list:
            if w == word:
                count += 1
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
    priority_list = []
    while len(tmp_list) != 0:
        size = 0
        for item in tmp_list:
            size_tmp = item[1]
            if (size_tmp > size) or (size_tmp == -1):
                size = size_tmp

        for item in tmp_list:
            if item[1] == size:
                priority_list.append(item[0])
                for i in tmp_list:
                    if i[0] == item[0]:
                        tmp_list.remove(i)
    return priority_list


def search_interisting_files(files_list):
    tmp_list = []
    for file in files_list:
        if file.endswith('.pdf'):
            tmp_list.append(pdf_parser(file))
        elif file.endswith('.txt'):
            tmp_list.append(txt_parser(file))
        elif file.endswith('.png'):
            print("TO DO =D")
        elif file.endswith('.docx'):
            tmp_list.append(docx_parser(file))
        else:
            print("balec de ce fichier")
    priority_list = sort_by_priority(tmp_list)
    return priority_list


def pdf_parser(file):
    count = 0
    # Ouverture du pdf
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # Si le pdf est chiffré on le flag -1 (high priority)
    if pdfReader.isEncrypted:
        count = -1
        return [file, count]
    else:
        # Pour chaque page du pdf
        for _ in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(0)
            # On extract le text
            var = pageObj.extractText()
            # On le met sous forme de tableau de mot
            words_list = var.split(" ")
            # On vérifie le nombre de mot intéressant
            count += count_interisting_word(words_list)
        pdfFileObj.close()
        return [file, count]


def docx_parser(file):
    count = 0
    doc = docx.Document(file)
    fullText = []
    # on recup les paragraphe
    for para in doc.paragraphs:
        fullText.append(para.text)
    # on recup les lignes
    for line in fullText:
        words_list = line.split(" ")
        count += count_interisting_word(words_list)
    return [file, count]


def txt_parser(file):
    #On récupère les lignes du fichiers
    file_ = open(file, mode='r')
    lines = file_.readlines()
    file_.close()
    # On les transforme en liste de mots
    words_list = []
    for line in lines:
        for word in line.split(' '):
            words_list.append(word)
    # On compte le nombre de mots intéressant dans le fichier
    count = count_interisting_word(words_list)
    return [file, count]


def main():
    files_list = search_interisting_files(file_collection('testdir'))
    print(files_list)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
