import re
import sys
from bs4 import BeautifulSoup


class AutoLinker:
    NUMBER_PATTERN = r'\b(?:(Section)\s+)?(\d+(?:\.\d+)*)\b'
    NO_GO_PATTERN = r'(?i)\b(?:Tables?|Chapters?)\s*$'

    def __init__(self, document):
        self.content = BeautifulSoup(document, 'html.parser')
        self.section_ids = set()

    def render(self):
        self._find_section_ids()
        self._linkify_text_nodes()
        return self.content

    def _find_section_ids(self):
        for element in self.content.find_all(id=True):
            section_id = element.get('id')
            if section_id and re.match(self.NUMBER_PATTERN, section_id):
                self.section_ids.add(section_id)

    def _linkify_text_nodes(self):
        for text_node in self.content.find_all(string=True):

            if self._should_skip_node(text_node):
                continue

            text_to_replace = str(text_node)
            new_text = text_to_replace

            sections_to_linkify = self._collect_valid_sections(text_to_replace)

            for section in reversed(sections_to_linkify):
                linked = self._linkify(
                    section['full_match'], section['section_num'])
                new_text = new_text[:section['start']] + \
                    linked + new_text[section['end']:]

            if new_text != text_to_replace:
                new_node = BeautifulSoup(new_text, 'html.parser')
                text_node.replace_with(new_node)

    def _linkify(self, string, section_id):
        result = f'<a href="#{section_id}" style="font-weight: bold; color: red;">{string}</a>'
        return result

    def _should_skip_node(self, text_node):
        parent = text_node.parent
        parent_classes = parent.get('class')
        return parent_classes and 'section_title' in parent_classes

    def _should_skip_match(self, match, text):
        section_num = match.group(2)
        full_match = match.group(0)

        if '.' not in section_num and 'Section' not in full_match:
            return True

        start_pos = match.start()
        lookback_start = max(0, start_pos - 10)
        preceding_text = text[lookback_start:start_pos]

        return bool(re.search(self.NO_GO_PATTERN, preceding_text))

    def _collect_valid_sections(self, text):
        sections = []
        for match in re.finditer(self.NUMBER_PATTERN, text):
            if self._should_skip_match(match, text):
                continue

            section_num = match.group(2)
            if section_num in self.section_ids:
                sections.append({
                    'start': match.start(),
                    'end': match.end(),
                    'full_match': match.group(0),
                    'section_num': section_num
                })
        return sections


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("enter the name of an input file after the command")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        document = file.read()

    linker = AutoLinker(document)
    print(linker.render())
