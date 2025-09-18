import os

# Add this to the top of your script to modify zwoasi.__init__ without modifying the original file
def patch_zwoasi_init():
    import zwoasi
    import types

    # Define the new init function that will search in the package's lib directory first
    def new_init(library_file=None):
        global zwolib

        if zwoasi.zwolib is not None:
            # Library already initialized. do nothing
            return

        if library_file is None:
            # First try to find the library in the package directory
            package_dir = os.path.dirname(zwoasi.__file__)
            
            # Check for platform-specific library names
            if os.name == 'nt':  # Windows
                lib_names = ['ASICamera2.dll']
            elif os.name == 'posix':
                if sys.platform == 'darwin':  # macOS
                    lib_names = ['libASICamera2.dylib', 'ASICamera2.dylib']
                else:  # Linux and other Unix-like
                    lib_names = ['libASICamera2.so', 'ASICamera2.so']
            else:
                lib_names = []
            
            # Look in the package lib directory first
            lib_dir = os.path.join(package_dir, 'lib')
            for lib_name in lib_names:
                candidate_path = os.path.join(lib_dir, lib_name)
                if os.path.exists(candidate_path):
                    library_file = candidate_path
                    print(f"Found ASI SDK library at: {library_file}")
                    break
            
            # If not found in package, try system-wide search
            if library_file is None:
                library_file = zwoasi.find_library('ASICamera2')
            
            # Also check ZWO_ASI_LIB environment variable as fallback
            if library_file is None:
                env_lib = os.environ.get('ZWO_ASI_LIB')
                if env_lib and os.path.exists(env_lib):
                    library_file = env_lib

        if library_file is None:
            raise zwoasi.ZWO_Error('ASI SDK library not found')

        zwoasi.zwolib = zwoasi.c.cdll.LoadLibrary(library_file)

        # The rest of the original init function...
        # We're not touching the function signatures setup

    # Replace the original init function with our new one
    zwoasi.init = new_init

# Call this function before importing zwoasi in your main script
if __name__ == "__main__":
    import sys
    patch_zwoasi_init()
    import zwoasi as asi
    print("Patched zwoasi.init() to look in package lib directory first")
    
    # Your code that uses zwoasi...
    try:
        # Initialize with the patched init function
        asi.init()
        print(f"Found {len(asi.list_cameras())} cameras")
    except asi.ZWO_Error as e:
        print(f"Error: {e}")