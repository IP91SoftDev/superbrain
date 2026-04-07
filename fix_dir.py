for path in ['D:/superbrain/backend/start.py', 'D:/superbrain/superbrain-cli/payload/start.py']:
    content = open(path, 'r', encoding='utf-8').read()
    content = content.replace('BACKEND_DIR / ', 'BASE_DIR / ')
    open(path, 'w', encoding='utf-8').write(content)
    print(f'Fixed {path}')
