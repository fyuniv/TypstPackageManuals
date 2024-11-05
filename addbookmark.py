import PyPDF2
import re
import os

def extract_section_title(page_text):
    date_pattern = re.compile(
        r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s*(January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{1,2}',
        re.IGNORECASE
    )

    upcoming_event_pattern = re.compile(r'upcoming.*event(s)?|event(s)?.*upcoming', re.IGNORECASE)

    cleaned_lines = []
    for line in page_text.splitlines():
        line = line.strip()
        if date_pattern.match(line) or upcoming_event_pattern.search(line):
            cleaned_lines.append(line)

    return cleaned_lines[0].strip() if cleaned_lines else ''

def extract_semester_year(page_text):
    lines = page_text.splitlines()
    for line in lines:
        line = line.strip()
        semester_year_match = re.search(r'(\w+)\s+(\d{4})', line)
        if semester_year_match:
            semester_year = f"{semester_year_match.group(1)} {semester_year_match.group(2)}"
            return semester_year
    return ''

def add_bookmarks_to_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        semester_year = ''
        
        # Process the first page to get semester year and prepare for bookmarks
        if len(reader.pages) > 0:
            first_page_text = reader.pages[0].extract_text()
            
            if first_page_text:
                semester_year = extract_semester_year(first_page_text)

        # First pass to add the title page bookmark if available
        if semester_year:
            title_page_bookmark = f'CUNY GC Seminars - {semester_year}'
            writer.add_outline_item(title_page_bookmark, 0)  # Page 0 is the title page

        # Second pass to add section title bookmarks
        for page in range(len(reader.pages)):
            writer.add_page(reader.pages[page])
            page_text = reader.pages[page].extract_text()
            if page_text:
                section_title = extract_section_title(page_text)
                if section_title:
                    writer.add_outline_item(section_title, page)

        # Overwrite the original PDF file with bookmarks
        with open(pdf_path, 'wb') as output_file:
            writer.write(output_file)

def process_pdfs_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_file_path = os.path.join(folder_path, filename)
            add_bookmarks_to_pdf(pdf_file_path)
            print(f'Bookmarks added for {filename}')

# Example usage
folder_path = 'manuals'  # Change this to your folder path
process_pdfs_in_folder(folder_path)
