with open('backup.json', 'rb') as source_file:
    content = source_file.read()

with open('backup_utf8.json', 'wb') as target_file:
    target_file.write(content.decode('utf-16').encode('utf-8'))
