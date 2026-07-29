import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueshore_server.settings')
django.setup()

from django.template.loader import render_to_string

html = render_to_string('index.html')
if "200+" in html:
    print("FOUND 200+ IN RENDERED TEMPLATE!")
else:
    print("RENDERED TEMPLATE HAS NO 200+!")

idx = html.find("Projects Delivered")
while idx != -1:
    print("--- MATCH ---")
    print(html[max(0, idx-150):idx+100])
    idx = html.find("Projects Delivered", idx+1)
