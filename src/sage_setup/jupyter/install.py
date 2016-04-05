"""
Installing the SageMath Jupyter Kernel and extensions

Kernels have to register themselves with Jupyter so that they appear
in the Jupyter notebook's kernel drop-down. This is done by
:class:`SageKernelSpec`.
"""

import os
import errno

from sage.env import (
    SAGE_DOC, SAGE_LOCAL, SAGE_EXTCODE, SAGE_SRC,
    SAGE_VERSION
)
from jupyter_core.paths import ENV_JUPYTER_PATH
JUPYTER_PATH = ENV_JUPYTER_PATH[0]


class SageKernelSpec(object):

    def __init__(self):
        """
        Utility to manage SageMath kernels and extensions

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec._display_name    # random output
            'SageMath 6.9'
        """
        from sage.repl.ipython_kernel.kernel import SageKernel
        kernel_identifier = SageKernel.identifier()
        self._display_name = 'SageMath {0}'.format(SAGE_VERSION)
        self.kernel_dir = os.path.join(SAGE_SRC, "build", "spec" , "kernels", kernel_identifier)
        self._mkdirs()

    def _mkdirs(self):
        """
        Create necessary parent directories

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec._mkdirs()
            sage: os.path.isdir(spec.nbextensions_dir)
            True
        """
        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise
        mkdir_p(self.kernel_dir)

    def symlink(self, src, dst):
        """
        Symlink ``src`` to ``dst``

        This is not an atomic operation.

        Already-existing symlinks will be deleted, already existing
        non-empty directories will be kept.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: path = tmp_dir()
            sage: spec.symlink(os.path.join(path, 'a'), os.path.join(path, 'b'))
            sage: os.listdir(path)
            ['b']
        """
        try:
            os.remove(dst)
        except OSError as err:
            if err.errno == errno.EEXIST:
                return
        os.symlink(src, dst)

    def use_local_mathjax(self):
        """
        Symlink SageMath's Mathjax install to the Jupyter notebook.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec.use_local_mathjax()
            sage: mathjax = os.path.join(spec.nbextensions_dir, 'mathjax')
            sage: os.path.isdir(mathjax)
            True
        """
        src = os.path.join(SAGE_LOCAL, 'share', 'mathjax')
        dst = os.path.join(self.nbextensions_dir, 'mathjax')
        self.symlink(src, dst)

    def use_local_jsmol(self):
        """
        Symlink jsmol to the Jupyter notebook.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec.use_local_jsmol()
            sage: jsmol = os.path.join(spec.nbextensions_dir, 'jsmol')
            sage: os.path.isdir(jsmol)
            True
        """
        src = os.path.join(SAGE_LOCAL, 'share', 'jsmol')
        dst = os.path.join(self.nbextensions_dir, 'jsmol')
        self.symlink(src, dst)

    def _kernel_cmd(self):
        """
        Helper to construct the SageMath kernel command.

        OUTPUT:

        List of strings. The command to start a new SageMath kernel.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec._kernel_cmd()
            ['python2.7',
             '-m',
             'sage.repl.ipython_kernel',
             '-f',
             '{connection_file}']
        """
        return [
            'python2.7',
            '-m', 'sage.repl.ipython_kernel',
            '-f', '{connection_file}',
        ]

    def kernel_spec(self):
        """
        Return the kernel spec as Python dictionary

        OUTPUT:

        A dictionary. See the Jupyter documentation for details.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec.kernel_spec()
            {'argv': ..., 'display_name': 'SageMath ...'}
        """
        return dict(
            argv=self._kernel_cmd(),
            display_name=self._display_name,
        )

    def _build_spec(self):
        """
        Install the SageMath Jupyter kernel

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec._install_spec()    # not tested
        """
        jsonfile = os.path.join(self.kernel_dir, "kernel.json")
        import json
        with open(jsonfile, 'w') as f:
            json.dump(self.kernel_spec(), f)

    def _symlink_resources(self):
        """
        Symlink miscellaneous resources

        This method symlinks additional resources (like the SageMath
        documentation) into the SageMath kernel directory. This is
        necessary to make the help links in the notebook work.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec._install_spec()         # not tested
            sage: spec._symlink_resources()    # not tested
        """
        path = os.path.join(SAGE_EXTCODE, 'notebook-ipython')
        for filename in os.listdir(path):
            self.symlink(
                os.path.join(path, filename),
                os.path.join(self.kernel_dir, filename)
            )
        self.symlink(
            os.path.join(SAGE_DOC, 'html', 'en'),
            os.path.join(self.kernel_dir, 'doc')
        )

    @classmethod
    def ipython_extra_files(cls):
        """
        Return a data_files style list of files that will be
        installed for the SageMath Jupyter kernel to work

        This method prepares the kernel and notebook extensions for installation.
        There shouldn't be any needs to call any of the other methods directly.

        EXAMPLES::

            sage: from sage_setup.jupyter.install import SageKernelSpec
            sage: spec = SageKernelSpec()
            sage: spec.ipython_extra_files()  # not tested
        """
        instance = cls()
        instance._build_spec()

        from sage.repl.ipython_kernel.kernel import SageKernel
        kernel_identifier = SageKernel.identifier()
        kernel_installdir = os.path.join(JUPYTER_PATH, "kernels", kernel_identifier)
        kernelpath = os.path.join("build", "spec" , "kernels", kernel_identifier, "kernel.json")
        data_files = [(kernel_installdir, [kernelpath])]

        return data_files

