import re
import sys
from bs4 import BeautifulSoup


class AutoLinker:
    SECTION_PATTERN = r'\b(?:(Section)\s+)?(\d+(?:\.\d+)*)\b'
    NO_GO_PATTERN = r'(?i)\b(?:Tables?|Chapters?)\s+\d+(?:\.\d+)*\b'

    def __init__(self, document):
        self.content = BeautifulSoup(document, 'html.parser')
        self.section_ids = []

    # find valid section IDs to check against and link to later
    def find_section_ids(self):
        for element in self.content.find_all(id=True):
            section_id = element.get('id')
            if section_id and re.match(self.SECTION_PATTERN, section_id):
                self.section_ids.append(section_id)

    # wrap valid candidates in href tag
    def linkify(self, string, section_id):
        result = f'<a href="#{section_id}" style="font-weight: bold; color: red;">{string}</a>'
        return result

    # Find Link candidates
    def find_linkable_nodes(self):
        # grabbing any dotted numbers and Section if it exists
        number_pattern = r'\b(?:(Section)\s+)?(\d+(?:\.\d+)*)\b'

        for text_node in self.content.find_all(string=True):
            parent = text_node.parent
            if parent.get('class'):
                parent_classes = parent.get('class')
                if 'section_title' in parent_classes:
                    continue

            text_to_replace = str(text_node)
            new_text = text_to_replace

            # find matches that link to section IDs
            replacements = []
            for match in re.finditer(number_pattern, text_to_replace):
                section_num = match.group(2)
                full_match = match.group(0)

                # skip that 12
                if '.' not in section_num and 'Section' not in full_match:
                    continue

                start_pos = match.start()
                # arbitrary 10
                lookback_start = max(0, start_pos - 10)
                preceding_text = text_to_replace[lookback_start:start_pos]

                # we want to skip table or chapter references since they're not sections
                if re.search(r'(?i)\b(?:Tables?|Chapters?)\s*$', preceding_text):
                    continue

                if section_num in self.section_ids:
                    replacements.append({
                        'start': match.start(),
                        'end': match.end(),
                        'full_match': full_match
                    })

            for rep in reversed(replacements):
                linked = self.linkify(rep['full_match'], section_num)
                new_text = new_text[:rep['start']] + \
                    linked + new_text[rep['end']:]

            if new_text != text_to_replace:
                # print("=====================")
                # print(f"gonna replace this: {text_to_replace}")
                # print(f"with this: {new_text}")
                new_node = BeautifulSoup(new_text, 'html.parser')
                text_node.replace_with(new_node)

    def render(self):
        self.find_section_ids()
        self.find_linkable_nodes()
        return self.content


if __name__ == "__main__":
    # don't forget html file param
    if len(sys.argv) < 2:
        print("enter the name of an input file after the command")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        document = file.read()

    linker = AutoLinker(document)
    print(linker.render())
