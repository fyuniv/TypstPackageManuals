import os

# HTML code to be inserted
html_code_to_insert = '<li><a href="https://fyuniv.github.io/TypstPackageManuals/">Back to Site Home</a></li><li><a href="{filename}.html">Back to Cover Page</a></li>'

# Directory containing the HTML files
directory = 'manuals'

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        file_path = os.path.join(directory, filename)
        file_title = os.path.splitext(filename)[0]
        
        # Read the content of the file with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the position to insert the HTML code
        insert_position = content.find('<div id="outline">\n<ul>') + len('<div id="outline">\n<ul>')
        
        # Insert the HTML code with the correct filename
        new_content = content[:insert_position] + '\n' + html_code_to_insert.format(filename=file_title) + '\n' + content[insert_position:]
        
        # Write the new content back to the file with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

print("HTML code has been successfully inserted into all HTML files in the folder.")
