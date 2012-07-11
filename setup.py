import os.path
import subprocess
import logging

import distutils
import distutils.core
import distutils.command

logging.basicConfig(format = '%(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)

version = '1.0.1c'
subject_name = "OpenSSL-Win32-Binaries" % locals()
tarball_fname = '%(subject_name)s.zip' % locals()
tarball_url = 'https://github.com/kevinw/openssl-setup-py/blob/master/%(tarball_fname)s?raw=true' % locals()


def call(*args):
    log.info('Executing: %r', args)
    subprocess.call(args)

start_dir = os.path.dirname(os.path.abspath(__file__))


class basic_command(distutils.core.Command):
    config_vars = []
    user_options = []
    config_vars = []
    install_dir = distutils.sysconfig.get_python_lib()
    install_scripts = None
    skip_build = False
    record = None
    optimize = 0

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class download(basic_command):
    user_options = []

    def run(self):
        # Download and unpack tarball if necessary. NOTE: there is NO validation here!
        if not os.path.isdir(subject_name):
            if not os.path.isfile(tarball_fname):
                call('curl', '-L', tarball_url, '--output', tarball_fname)

            call('unzip', tarball_fname)


#class configure(basic_command):
#    sub_commands = ['download']
#    user_options = []
#
#    def run(self):
#        self.run_command('download')
#        # Configure
#        os.chdir(subject_name)
#        call("perl", 'Configure', 'VC-WIN32')
#        os.chdir(start_dir)


# class patch(basic_command):
#    user_options = []
#
#    def run(self):
#        self.run_command('configure')
#        # Patch one of the build scripts to make sure it'll work with nmake
#        os.chdir(subject_name)
#        os.chdir('util')
#        call('patch', '-f', 'mk1mf.pl', os.path.join(start_dir, "mk1mf_chomp_newlines.patch"))
#        os.chdir(start_dir)


#class build_ext(basic_command):
#    user_options = []
#
#    def run(self):
#        #self.run_command('patch')
#        os.chdir(subject_name)
#        call('ms\\do_nasm.bat')
#        call('nmake', '-f', 'ms\\ntdll.mak')
#        os.chdir(start_dir)


class install_headers(basic_command):
    user_options = []

    def run(self):
        self.run_command('download')
        os.chdir(subject_name)
        includes_dir = os.path.join(distutils.sysconfig.PREFIX, 'PC')
        if not os.path.isdir(includes_dir):
            os.makedirs(includes_dir)
        assert os.path.isdir('include')
        call('cp', '-R', 'include/*', includes_dir)
        os.chdir(start_dir)


class install_lib(basic_command):
    user_options = []

    def run(self):
        self.run_command('download')
        os.chdir(subject_name)
        lib_dir = os.path.join(distutils.sysconfig.PREFIX, 'libs')
        if not os.path.isdir(lib_dir):
            os.makedirs(lib_dir)
        assert os.path.isdir('lib')
        call('cp', '-R', 'lib/*', lib_dir)
        os.chdir(start_dir)


class install_bin(basic_command):
    user_options = []

    def run(self):
        self.run_command('download')
        os.chdir(subject_name)
        bin_dir = os.path.join(distutils.sysconfig.PREFIX, 'DLLs')
        if not os.path.isdir(bin_dir):
            os.makedirs(bin_dir)
        assert os.path.isdir('dlls')
        call('cp', '-R', 'dlls/*', bin_dir)
        os.chdir(start_dir)


class install(basic_command):
    user_options = []

    def run(self):
        self.run_command('install_headers')
        self.run_command('install_lib')
        self.run_command('install_bin')


class develop(install):
    pass

if __name__ == '__main__':

    cmdclass = dict((x, globals()[x]) for x in (
        'develop',
        'install',
        'install_lib',
        'install_bin',
        'install_headers',
        'download'
    ))
    cmdclass['develop'] = install

    distutils.core.setup(
        name = 'OpenSSL',
        version = version,
        cmdclass = cmdclass
    )
    os.chdir(start_dir)
