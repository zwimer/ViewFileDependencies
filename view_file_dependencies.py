import sys
import re
from pathlib import Path

# The global dictionary to hold dependencies
depends = {}

# Get dependencies of the file x
# Add the dependencies of x to dict_to_add_to
# Purposefully does not remove redundancies
def add_depend(x):

    # Get the include files
    with open(str(x)) as f:
        txt = [ i.strip() for i in f.read().split('\n') if i.strip().startswith('#') ]
    txt = [ i for i in txt if re.match('^.*include\\s*".*"\\s*$', i) ]
    includes = [ i.split('"')[1].strip() for i in txt ]

    # Add x to dict
    depends[str(x.name)] = includes

    # Add includes to dict
    for i in includes:
        if i not in depends:
            depends[i] = []

# Create the uml diagram of dependencies
# If combine_cpp_hpp, combines cpp and hpp files of the same name together
def create_uml( combine_cpp_hpp ):
    stng = ''
    for i in depends:
        for k in depends[i]:
            if combine_cpp_hpp:
                i = i.split('.')[0]; k = k.split('.')[0]
            stng += i + ' --|> ' + k + '\n'
        stng += '\n'
    return stng.strip()

# Creates the uml diaggram of dependencies
def view_file_dependencies( where_in, where_out_split, where_out_joined ):

    # Get files
    files = [ i for i in where.glob('*pp') if i.is_file() ]

    # Create dict
    for i in files:
        add_depend(i)

    # Create the uml
    uml_split = create_uml( False )
    uml_joined = create_uml( True )

    # Output the uml
    with open(where_out_split, 'w') as f:
        f.write(uml_split)
    with open(where_out_joined, 'w') as f:
        f.write(uml_joined)
    print('Just run the following to get the diagram')
    print('\tpython -m plantuml ' + where_out_split)
    print('\tpython -m plantuml ' + where_out_joined)

# Do not run on imports
if __name__ == '__main__':

    # Check args
    assert len(sys.argv) == 4

    # Get directory
    where = Path(sys.argv[1])
    assert where.exists()
    assert where.is_dir()

    # Create the uml
    view_file_dependencies( sys.argv[1], sys.argv[2], sys.argv[3] )
