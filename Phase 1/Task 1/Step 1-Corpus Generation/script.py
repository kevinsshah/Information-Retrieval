import os.path as path
import os
from bs4 import BeautifulSoup


if __name__ == "__main__":
    result = set()
    paths = path.abspath(path.join(os.getcwd(), "../../"))
    paths = os.path.join(paths, "htmldocs")
    i=0
    for file in os.listdir(paths):
        filename = os.path.join(paths,file)
        f = open(filename, 'r', encoding='utf-8')
        html = f.read()
        f.close()

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all("html"):
            print(tag.text)



        i+=1
        if i==1:
            break


    x = " ".join(["123","sdfasdf","vasd"])
    print(type(x))