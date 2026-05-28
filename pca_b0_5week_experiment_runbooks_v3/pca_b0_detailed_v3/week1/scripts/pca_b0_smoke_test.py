import importlib
mods=['torch','transformers','diffusers','datasets','PIL','pandas','numpy','open_clip']
for m in mods:
    try:
        mod=importlib.import_module(m); print('[OK]',m,getattr(mod,'__version__','version unknown'))
    except Exception as e: print('[FAIL]',m,e)
print('Smoke test finished.')
