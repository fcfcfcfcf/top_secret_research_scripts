import os
from shutil import copyfile
from os.path import isfile, join
  
def rename( src, ext, new_ext, dest ):
   dir_contents = os.listdir( src ) 

   for file_name in dir_contents:
       full_name = join( src, file_name )
       if ( not isfile( full_name ) ):
           rename( full_name, ext, new_ext, dest )

       file_pre, file_ext = os.path.splitext( full_name ) 
       if ( ext == file_ext ):
           copyfile( full_name, dest + file_name + new_ext )

if __name__ == '__main__':
    _dir = os.getcwd()
    src = _dir + "/sitl"
    dest = _dir + "/llvm_ir/"
 
    ext = '.o'
    new_ext = '.ll'

    rename( src, ext, new_ext, dest )
