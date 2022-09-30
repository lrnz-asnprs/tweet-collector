import os

""" Method made so that we can retrieve and reference the root-directory
    you will have to add the line
    sys.path.append(../(your-working-dir))
    if you are running it from a subfolder. 
    I will see if it possible to get that omitted too.
"""
    
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
CONFIG_PATH = os.path.join(ROOT_DIR, 'configuration.conf')  # requires `import os`
