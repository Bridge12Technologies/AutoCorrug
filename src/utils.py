#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: 1 May 2010
#   Last Modified: 1 September 2011
#   General Utilities for running MAGY simulations
#   Version 1.0 
 

import os

def recursive_delete(dirname):
    for path in (os.path.join(dirname,f) for f in os.listdir(dirname)):
        if os.path.isdir(path):
            rm_rf(path)
        else:
            os.unlink(path)
    os.rmdir(dirname)

