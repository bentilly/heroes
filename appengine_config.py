"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os.path
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

# update to gcloud tool stopped it accessing /System/Library/CoreServices/SystemVersion.plist
# from https://stackoverflow.com/questions/55166959/osx-dev-appserver-py-file-not-accessible-system-library-coreservices-systemve
try:
    from google.appengine.tools.devappserver2.python.runtime.stubs import FakeFile
    FakeFile._allowed_dirs.update(['/System/Library/CoreServices/'])    
except ImportError:
    pass
