import re
import sys
from bs4 import BeautifulSoup

class AutoLinker:
  def __init__(self,document):
    self.soup = BeautifulSoup(document, 'html.parser')
    self.section_ids = []
  
  # find valid section IDs to check against and link to later
  def find_section_ids(self):
    for element in self.soup.find_all(id=True):
      section_id = element.get('id')
      if section_id and re.match(r'\d+(?:\.\d+)*', section_id):
        self.section_ids.append(section_id)

  # wrap valid candidates in href tag
  def linkify(self,string):
    return f"<link>{string}<link>"


  # Find Link candidates
  def find_linkable_nodes:
    for text_node in self.soup.find_all(string=True):

    text_to_replace = str(text_node)
    text_with_link = self.linkify(text_to_replace)
    

  def render(self):
    self.find_section_ids()
    return self.section_ids
  


if __name__ == "__main__":
    # don't forget html file param
    if len(sys.argv) < 2:
      print("enter the name of an input file after the command")
      sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
      document = file.read()
    
    linker = AutoLinker(document)
    print(linker.render())
    



# compare link candidates to valid section ids
# wrap valid candidates in href tag