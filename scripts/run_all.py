#!/usr/bin/env python

from __future__ import print_function
import argparse
import os.path
import tempfile
import subprocess
import shutil
import sys
import timeit
import errno
import atexit

script_root = os.path.abspath(os.path.dirname(__file__))
cases_dir = os.path.join(script_root, '..')

skipdir = ('.git', 'extern', 'scripts')
default_gotm_url = 'https://github.com/gotm-model/code.git'

class TestPhase:
    def __init__(self, path, indent=0):
        print('%s%s...' % (' ' * indent, path.rsplit('/', 1)[-1]), end='', flush=True)
        self.indent = indent
        self.path = path
        self.has_children = False

    def start(self, name):
        if not self.has_children:
            print()
        self.has_children = True
        return TestPhase(self.path + '/' + name, indent=self.indent + 2)

    def complete(self, error=None):
        print(' SUCCESS' if error is None else (' FAILED (%s)' % error))

def run(phase, args, verbose=False, **kwargs):
    sys.stdout.flush()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, **kwargs)
    stdoutdata, _ = proc.communicate()
    if proc.returncode != 0:
        log_path = '%s.log' % phase.path.replace('/', '_')
        with open(log_path, 'w') as f:
            f.write(stdoutdata)
        logs.append(log_path)
        phase.complete('return code %i, log written to %s' % (proc.returncode, log_path))
    else:
        phase.complete()
    if verbose:
        print('Output:\n%s\n%s\n%s' % (80 * '-', stdoutdata, 80 * '-'))
    return proc.returncode

def git_clone(phase, url, workdir, branch=None):
    run(phase.start('clone'), ['git', 'clone', url, workdir])
    if branch is not None:
        run(phase.start('checkout'), ['git', 'checkout', branch], cwd=workdir)
    run(phase.start('submodule'), ['git', 'submodule', 'update', '--init', '--recursive'], cwd=workdir)

def cmake(phase, build_dir, source_dir, cmake_path='cmake', target=None, cmake_arguments=[]):
    # Create and change to build directory
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)

    if os.name == 'nt':
        x64 = sys.maxsize > 2**32
        cmake_arguments = ['-A', 'x64' if x64 else 'Win32'] + cmake_arguments

    # Build
    try:
        ret = run(phase.start('configure'), [cmake_path, source_dir] + cmake_arguments, cwd=build_dir)
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise
        print('\n\ncmake executable ("%s") not found. Specify its location on the command line with --cmake.' % cmake_path)
        sys.exit(2)

    if ret == 0:
        args = ['--config', 'Debug']
        if target is not None:
            args = args + ['--target', target]
        ret = run(phase.start('build'), [cmake_path, '--build', '.'] + args, cwd=build_dir)

    return ret == 0

def compare_netcdf(path, ref_path):
    import numpy
    import netCDF4
    perfect = True
    nc = netCDF4.Dataset(path)
    nc_ref = netCDF4.Dataset(ref_path)
    for varname in nc.variables.keys():
        if varname not in nc_ref.variables or varname in ('lon', 'lat', 'h', 'z', 'time'):
            continue
        ncvar = nc.variables[varname]
        ncvar_ref = nc_ref.variables[varname]
        dat = ncvar[...]
        valid = numpy.isfinite(dat)
        if not valid.all():
            print('    %s: %i of %i values are invalid' % (varname, valid.size - valid.sum(), valid.size))
            perfect = False
        else:
            delta = dat - ncvar_ref[...]
            maxdelta = numpy.abs(delta).max()
            perfect = perfect and maxdelta == 0.0
            print('    %s: max abs difference = %s' % (varname, maxdelta))
    nc.close()
    nc_ref.close()
    return perfect

def test(work_root, cmake_path='cmake', cmake_arguments=[], gotm_base=None):
    build_dir = os.path.join(work_root, 'build')

    if gotm_base is None:
        # Get latest GOTM [public]
        gotm_base = os.path.join(work_root, 'code')
        git_clone(TestPhase('git'), default_gotm_url, gotm_base)

    cmake(TestPhase('cmake'), build_dir, gotm_base, cmake_path, cmake_arguments=cmake_arguments)
    exe = os.path.join(build_dir, 'Debug/gotm.exe' if os.name == 'nt' else 'gotm')
    phase = TestPhase('cases')
    for name in os.listdir(cases_dir):
        path = os.path.join(cases_dir, name)
        if not os.path.isdir(path) or name in skipdirs:
            continue
        current_phase = phase.start(name)
        gotm_setup_dir = os.path.join(work_root, name)
        p = current_phase.start('copy')
        shutil.copytree(path, gotm_setup_dir)
        p.complete()
        run(current_phase.start('run'), [exe], cwd=gotm_setup_dir)

def clean(workdir):
    print('Clean-up: deleting %s' % workdir)
    shutil.rmtree(workdir, ignore_errors=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script runs all GOTM testcases.')
    parser.add_argument('--work_root', help='Path to use for code, testcases, results.', default=None)
    parser.add_argument('--gotm_base', help='Path to GOTM source code. If not provided this script will check out the latest verison of the master branch', default=None)
    parser.add_argument('--cmake', help='path to cmake executable', default='cmake')
    parser.add_argument('--compiler', help='Fortran compiler executable')
    parser.add_argument('-v', '--verbose', help='Enable more detailed output')
    args, cmake_arguments = parser.parse_known_args()
    if args.compiler is not None:
        cmake_arguments.append('-DCMAKE_Fortran_COMPILER=%s' % args.compiler)

    tmp = args.work_root is None
    if tmp:
        args.work_root = tempfile.mkdtemp()
        atexit.register(clean, args.work_root)
    args.work_root = os.path.abspath(args.work_root)
    print('Root of test directory: %s' % args.work_root)

    logs = []
    test(args.work_root, cmake_path=args.cmake, cmake_arguments=cmake_arguments, gotm_base=args.gotm_base)
    if logs:
        print('%i ERRORS! Check the logs:\n%s' % (len(logs), '\n'.join(logs)))
    else:
        print('ALL TESTS SUCCEEDED')


