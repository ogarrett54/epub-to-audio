import os
from ebooklib import epub
from bs4 import BeautifulSoup

EPUB_PATH = "book.epub"
OUTPUT_PATH = "book.txt"

def epub_to_string(epub_path):
    """
    Reads an EPUB file and converts its content to a clean, formatted string.
    This function specifically targets and removes citation numbers (in <sup> tags)
    and fixes improper line breaks.
    """
    if not os.path.exists(epub_path):
        print(f"Error: File not found at {epub_path}")
        return ""
    
    try:
        book = epub.read_epub(epub_path)
        full_text = []
        print("Successfully opened EPUB file. Processing contents...")

        for item in book.get_items_of_type(9): # 9 is the type for ITEM_DOCUMENT
            soup = BeautifulSoup(item.get_content(), 'html.parser')

            # Remove citation numbers (superscript tags)
            for sup in soup.find_all('sup'):
                sup.decompose()

            # Process block-level elements to preserve paragraph structure
            blocks = []
            
            # We now only look for specific content tags like paragraphs and headers.
            # By removing 'div', we avoid grabbing container tags that would
            # duplicate the content of the other tags inside them.
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                block_text = tag.get_text(separator=' ', strip=True)
                if block_text:
                    blocks.append(block_text)
            
            if blocks:
                full_text.append('\n\n'.join(blocks))

        if not full_text:
            print("\nWarning: Processed the EPUB but found no text content.")

        return "\n\n".join(full_text)

    except Exception as e:
        print("\n" + "="*20)
        print("AN ERROR OCCURRED. This is likely due to DRM or a formatting issue.")
        print(f"Specific Error: {e}")
        print("="*20 + "\n")
        return ""
    
book_string = epub_to_string(EPUB_PATH)

if book_string:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(book_string)
        print(f"Conversion successful. Full text saved to {OUTPUT_PATH}")
else:
    print("Operation failed. No output file was created.")