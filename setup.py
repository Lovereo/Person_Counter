from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Video_processing_pics",
    ext_modules=cythonize(['api/video.py']),
    script_args=["install"]
)
