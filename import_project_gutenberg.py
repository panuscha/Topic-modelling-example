import os
from bs4 import BeautifulSoup
import re

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def is_non_empty_paragraph(tag):
    return tag.name == 'p' and 'p3' in tag.get('class', []) 


def extract_stories(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    volumes = soup.find_all('h2', text=re.compile(r'VOLUME [IVXLCDM]+', re.IGNORECASE))

    for i, volume in enumerate(volumes):
        volume_folder = f"Volume_{i + 1}"

        if not os.path.exists(volume_folder):
            os.makedirs(volume_folder)

        story_content = ""

        for paragraph in volume.find_all_next(['p', 'h2']):
            if paragraph.name == 'p': 
                # Save the previous story content to a file
                if is_non_empty_paragraph(paragraph):
                    story_content += " ".join(span.get_text() for span in paragraph.find_all('span', class_='s1')) + " "
                
            else:
                if "VOLUME" in paragraph.string:
                    break

                for b in paragraph.find_all('b'):
                    if story_content:
                        with open(f"{volume_folder}/{story_title}.txt", 'w', encoding='utf-8') as file:
                            file.write(story_content)
                    # Update the current story title
                    story_title = b.string
                    #paragraph.find('span', class_='s1').find('b').get_text().strip()
                    story_content = ""

        # Save the last story content to a file
        if story_content:
            with open(f"{volume_folder}/{story_title}.txt", 'w', encoding='utf-8') as file:
                file.write(story_content)

if __name__ == "__main__":
    html_file_path = "/Users/charlottepanuskova/Downloads/pg3090-h/pg3090-images.html" # Replace with the actual file path
    html_content = read_html_file(html_file_path)
    extract_stories(html_content)
