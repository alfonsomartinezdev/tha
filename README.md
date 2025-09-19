# UpCodes Autolinker - Take Home Assignment

Hey folks! Thanks for reviewing my submission. Your job application actually inspired me to take a crack at a [document annotator](https://github.com/alfonsomartinezdev/rpg-annotator-frontend) for tabletop RPG handouts, so I was very excited to try out a different type of implementation of that (section based vs character by character offsets).

Here's my implementation of the autolinker functionality.

## Dependencies

- Python 3.x
- BeautifulSoup4 (`pip install beautifulsoup4`)

## Running the Script

```bash
python autolinker.py input.html > output.html
```

The script takes the HTML file as a command-line argument and prints the modified HTML to stdout.

## Approach

I went with a straightforward approach that prioritizes correctness and readability:

1. *First pass*: Collect all valid section IDs from the document (anything with an `id` attribute matching our section number pattern)
2. *Second pass*: Find and linkify section references in text nodes. **We're determining what a "section reference" is through a mixture of regex and comparing against the section IDs we collected earlier**.

### Key Decisions

- **Only link to existing sections** - I validate against the collected section IDs to avoid broken links
- **Context-aware matching** - The script avoids linking numbers that appear after "Table" or "Chapter".
- **Preserve section titles** - Skip linkification inside elements with class "section_title" to avoid self-referential links
- **Require context for standalone numbers** - A bare "1005" won't be linked, but "Section 1005" or "1005.6" will be (goodbye, random 12)

### Implementation Notes

- Used BeautifulSoup for robust HTML parsing rather than regex-based HTML manipulation. I'm most comfortable with Ruby, and BeautifulSoup is very similar to Nokogiri.
- Process matches in reverse order to maintain string indices during replacement. This is me learning from my mistakes in a [previous personal project](https://github.com/alfonsomartinezdev/rpg-annotator-api/blob/320af4633e36dcd8a0f5a6f03c8ead43982dd778/app/services/document_renderer.rb#L23)
- Changed `section_ids` to a set for O(1) at the last minute lookup performance (noticed this could be improved from my original list implementation)

## Given More Time

A few things I'd explore with more time:
- Add comprehensive test coverage with edge cases
- I'm not sure how often these documents need to be rendered and Autolinked, but I'd probably consider performance optimizations for very large documents (compiled regex, batch DOM updates)
---

Looking forward to chatting more about this! Feel free to reach out if you have any questions about my approach.

Thanks,
Alfonso
