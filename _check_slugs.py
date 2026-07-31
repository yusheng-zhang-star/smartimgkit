import importlib.util, os
spec = importlib.util.spec_from_file_location('gen', '_generate_new_tools.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for t in mod.ALL_NEW_TOOLS:
    slug = t['slug']
    exists = os.path.exists(f'tools/{slug}.html')
    status = 'OK' if exists else 'MISSING'
    print(f'{status}: {slug}')
