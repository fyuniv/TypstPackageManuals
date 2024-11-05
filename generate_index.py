import os
import re
from datetime import datetime

def generate_index_html(directory):
    # List all HTML files in the directory
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    # Sort files by modification time, newest first
    html_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    
    # Generate HTML content
    html_content = """
    <html>
    <head>
        <title>Manuals for Typst Packages</title>
        <link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Gothic A1', sans-serif;
                margin: 8%;
            }
            h1 {
                text-align: center;
            }
            h2 {
                margin-top: 40px;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                text-decoration: none;
                color: #000;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
    """
    html_content += '<h1>Html Versions of Manuals of Typst Packages</h1>'
    
    html_content += "<ul>"
    for i, file in enumerate(html_files[:4]):
        file_title = os.path.splitext(file)[0]
        parts = re.split(r'[-_]', file_title)
        file_name = parts[0]
        version = parts[1]
        html_content += f"<li><a href='{file}'>{file_name} Version: {version}</a></li>"
    html_content += "</ul>"
    
    html_content += "</body></html>"
    
    # Write the index.html file
    with open(os.path.join(directory, 'index.html'), 'w') as f:
        f.write(html_content)

# Directory containing the HTML files
directory = 'manuals'

# Generate the index.html file
generate_index_html(directory)

print("index.html has been generated successfully.")
