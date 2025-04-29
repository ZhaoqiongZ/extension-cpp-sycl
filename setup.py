# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import torch
import glob

from setuptools import find_packages, setup

from torch.utils.cpp_extension import (
    CppExtension,
    SyclExtension,
    BuildExtension,
)

library_name = "extension_cpp"


def get_extensions():

    use_sycl = torch.xpu.is_available()
    extension = SyclExtension if use_sycl else CppExtension
    extra_compile_args = {
        "cxx": ["-g" ],
        "sycl": ["-O2"],
    }

    this_dir = os.path.dirname(os.path.curdir)
    extensions_dir = os.path.join(this_dir, library_name, "csrc")
    sources = list(glob.glob(os.path.join(extensions_dir, "*.cpp")))

    extensions_sycl_dir = os.path.join(extensions_dir, "sycl")
    sycl_sources = list(glob.glob(os.path.join(extensions_sycl_dir, "*.sycl")))

    if use_sycl:
        sources += sycl_sources

    ext_modules = [
        SyclExtension(
            name=f"{library_name}._C",
            sources=sources,
            extra_compile_args=extra_compile_args,
        )
    ]

    return ext_modules


setup(
    name=library_name,
    packages=find_packages(),
    ext_modules=get_extensions(),
    description="Example of PyTorch C++ and SYCL extensions",
    cmdclass={"build_ext": BuildExtension.with_options(use_xpu=True)},
)