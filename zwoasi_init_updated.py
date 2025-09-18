import os

# Add this to the top of your script to modify zwoasi.__init__ without modifying the original file
def patch_zwoasi_init():
    import zwoasi
    
    # Define the new init function that will search in the package's lib directory first
    def new_init(library_file=None):
        import os
        
        if zwoasi.zwolib is not None:
            # Library already initialized. do nothing
            return

        if library_file is None:
            # First try to find the library in the package directory
            module_path = os.path.dirname(os.path.abspath(zwoasi.__file__))
            lib_path = os.path.join(module_path, 'lib', 'ASICamera2.dll')
            
            if os.path.isfile(lib_path):
                library_file = lib_path
            else:
                # Fall back to system-wide search
                library_file = zwoasi.find_library('ASICamera2')

        if library_file is None:
            raise zwoasi.ZWO_Error('ASI SDK library not found')

        zwoasi.zwolib = zwoasi.c.cdll.LoadLibrary(library_file)

        # The rest of the original init function remains unchanged
        # Function signatures setup remains the same as in the original

    # Replace the original init function with our new one
    zwoasi.init = new_init