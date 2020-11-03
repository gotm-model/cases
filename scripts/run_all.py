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
import datetime
import platform

import yaml

script_root = os.path.abspath(os.path.dirname(__file__))
cases_dir = os.path.join(script_root, '..')

skipdirs = ('.git', 'extern', 'scripts', 'build')
default_gotm_url = 'https://github.com/gotm-model/code.git'

class TestPhase:
    def __init__(self, path='', depth=0):
        self.name = path.rsplit('/', 1)[-1]
        if path:
            print('%s- %s...' % ('  ' * (depth - 1), self.name), end='', flush=True)
        self.depth = depth
        self.path = path
        self.children = []
        self.error = None
        self.error_detail = None
        self.files = []

    def child(self, name):
        if self.path and not self.children:
            print()
        child = TestPhase(name if not self.path else self.path + '/' + name, depth=self.depth + 1)
        self.children.append(child)
        return child

    def set_error(self, error, detail=None):
        self.error = error
        self.error_detail = detail

    def __enter__(self):
        self.start_time = timeit.default_timer()
        return self

    def __exit__(self, type, value, traceback):
        self.duration = timeit.default_timer() - self.start_time
        failures = [child.name for child in self.children if child.error]
        print('  ' * (self.depth) if self.children else ' ', end='')
        if self.error is not None:
            print('FAILED (%s), ' % self.error, end='')
        elif failures:
            print('%i subtasks FAILED: %s, ' % (len(failures), ', '.join(failures)), end='')
        if self.files:
            print('logs: %s, ' % ', '.join(self.files), end='')
        print('duration: %.3f s' % self.duration)

    def get_files(self):
        files = list(self.files)
        for child in self.children:
            files.extend(child.get_files())
        return files

    def to_yaml(self):
        info = dict(name=self.name, duration=self.duration)
        for att in ['error', 'error_detail', 'files', 'children']:
            value = getattr(self, att, None)
            if value:
                info[att] = value
        if self.children:
            info['children'] = [c.to_yaml() for c in self.children]
        return info

def run(phase, args, verbose=False, **kwargs):
    with phase:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, **kwargs)
        stdoutdata, _ = proc.communicate()
        if proc.returncode != 0:
            log_path = '%s.log' % phase.path.replace('/', '_')
            with open(log_path, 'w') as f:
                f.write(stdoutdata)
            phase.files.append(log_path)
            lines = stdoutdata.rsplit('\n', 5)[-5:]
            phase.set_error('return code %i' % (proc.returncode,), detail='\n'.join(lines))
    if verbose:
        print('Output:\n%s\n%s\n%s' % (80 * '-', stdoutdata, 80 * '-'))
    return proc.returncode

def git_clone(phase, url, workdir, branch=None):
    run(phase.child('clone'), ['git', 'clone', url, workdir])
    if branch is not None:
        run(phase.child('checkout'), ['git', 'checkout', branch], cwd=workdir)
    run(phase.child('submodule'), ['git', 'submodule', 'update', '--init', '--recursive'], cwd=workdir)

def git_get_commit(workdir):
    proc = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, cwd=workdir)
    stdoutdata, _ = proc.communicate()
    return stdoutdata.strip()

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
        ret = run(phase.child('configure'), [cmake_path, source_dir] + cmake_arguments, cwd=build_dir)
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise
        print('\n\ncmake executable ("%s") not found. Specify its location on the command line with --cmake.' % cmake_path)
        sys.exit(2)

    if ret == 0:
        args = ['--config', 'Debug']
        if target is not None:
            args = args + ['--target', target]
        ret = run(phase.child('build'), [cmake_path, '--build', '.'] + args, cwd=build_dir)

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

def test(work_root, cmake_path='cmake', cmake_arguments=[], gotm_base=None, gotm_branch=None, extra_info=''):
    build_dir = os.path.join(work_root, 'build')
    with TestPhase() as root_phase:
        if gotm_base is None:
            # Get latest GOTM [public]
            gotm_base = os.path.join(work_root, 'code')
            with root_phase.child('git') as p:
                git_clone(p, default_gotm_url, gotm_base, branch=gotm_branch)
        gotm_id, cases_id = git_get_commit(gotm_base), git_get_commit(cases_dir)
        version = '%s-%s%s' % (gotm_id, cases_id, extra_info)
        os.makedirs(version, exist_ok=True)
        os.chdir(version)

        with root_phase.child('cmake') as p:
            cmake(p, build_dir, gotm_base, cmake_path, cmake_arguments=cmake_arguments)
        exe = os.path.join(build_dir, 'Debug/gotm.exe' if os.name == 'nt' else 'gotm')

        # Detect compiler version
        proc = subprocess.Popen([exe, '--version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        compiler = None
        for l in proc.stdout:
            if l.lstrip().startswith('Compiler: '):
                compiler = l[11:].strip()

        for name in sorted(os.listdir(cases_dir)):
            path = os.path.join(cases_dir, name)
            if not os.path.isdir(path) or name in skipdirs:
                continue
            with root_phase.child(name) as current_phase:
                gotm_setup_dir = os.path.join(work_root, name)
                with current_phase.child('copy'):
                    shutil.copytree(path, gotm_setup_dir)
                run(current_phase.child('run'), [exe], cwd=gotm_setup_dir)

    files = root_phase.get_files()
    if files:
        print('Please review the following log files:\n%s' % '\n'.join(files))

    os.chdir('..')
    outpath = '%s.log' % version
    print('Saving result to %s' % outpath)
    with open(outpath, 'w') as f:
        info = root_phase.to_yaml()
        info['datetime'] = datetime.datetime.now().isoformat()
        info['gotm_commit'] = gotm_id
        info['cases_commit'] = cases_id
        info['extra_info'] = extra_info
        info['compiler'] = compiler
        info['platform'] = platform.platform()
        yaml.dump(info, f)

def clean(workdir):
    print('Clean-up: deleting %s' % workdir)
    shutil.rmtree(workdir, ignore_errors=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script runs all GOTM testcases.')
    parser.add_argument('--work_root', help='Path to use for code, testcases, results.', default=None)
    parser.add_argument('--gotm_base', help='Path to GOTM source code. If not provided this script will check out the latest verison of the master branch', default=None)
    parser.add_argument('--gotm_branch', help='GOTM branch to check out', default=None)
    parser.add_argument('--cmake', help='path to cmake executable', default='cmake')
    parser.add_argument('--compiler', help='Fortran compiler executable')
    parser.add_argument('--extra_info', help='Extra identifying string for result file', default='')
    parser.add_argument('-v', '--verbose', help='Enable more detailed output')
    args, cmake_arguments = parser.parse_known_args()
    if args.compiler is not None:
        cmake_arguments.append('-DCMAKE_Fortran_COMPILER=%s' % args.compiler)
    assert args.gotm_branch is None or args.gotm_base is None, 'If you specify a local directory with GOTM source code (--gotm_base), you cannot also specify a GOTM branch to check out (--gotm_branch)'

    tmp = args.work_root is None
    if tmp:
        args.work_root = tempfile.mkdtemp()
        atexit.register(clean, args.work_root)
    args.work_root = os.path.abspath(args.work_root)
    print('Root of test directory: %s' % args.work_root)

    test(args.work_root, cmake_path=args.cmake, cmake_arguments=cmake_arguments, gotm_base=args.gotm_base, gotm_branch=args.gotm_branch, extra_info=args.extra_info)


