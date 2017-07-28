 #!/usr/bin/python

import os
import sys
import os.path as path
sys.path.append(path.join(path.dirname(path.abspath(sys.argv[0])), "..", "repos", "mesa_ci"))
import build_support as bs


class MesaPerf:
    def __init__(self):
        self.opts = bs.Options()

        if self.opts.config == 'debug':
            print "ERROR: perf not supported for debug"
            assert(False)

        pm = bs.ProjectMap()
        self._src_dir = pm.project_source_dir("mesa")
        self._build_dir = "/tmp/mesa-perf/build_" + self.opts.arch

        # generated with `gcc -E -v -march=native - < /dev/null 2>&1 | grep cc1`
        self._flags = ['-march=skylake', '-mmmx',
                       '-mno-3dnow', '-msse', '-msse2',
                       '-msse3', '-mssse3', '-mno-sse4a',
                       '-mcx16', '-msahf', '-mmovbe',
                       '-maes', '-mno-sha', '-mpclmul',
                       '-mpopcnt', '-mabm', '-mno-lwp',
                       '-mfma', '-mno-fma4', '-mno-xop',
                       '-mbmi', '-mbmi2', '-mno-tbm',
                       '-mavx', '-mavx2', '-msse4.2',
                       '-msse4.1', '-mlzcnt', '-mno-rtm',
                       '-mno-hle', '-mrdrnd', '-mf16c',
                       '-mfsgsbase', '-mrdseed', '-mprfchw',
                       '-madx', '-mfxsr', '-mxsave',
                       '-mxsaveopt', '-mno-avx512f',
                       '-mno-avx512er', '-mno-avx512cd',
                       '-mno-avx512pf', '-mno-prefetchwt1',
                       '-mclflushopt', '-mxsavec',
                       '-mxsaves', '-mno-avx512dq',
                       '-mno-avx512bw', '-mno-avx512vl',
                       '-mno-avx512ifma', '-mno-avx512vbmi',
                       '-mno-clwb', '-mno-mwaitx',
                       '-mno-clzero', '-mno-pku', '--param',
                       'l1-cache-size=32', '--param',
                       'l1-cache-line-size=64', '--param',
                       'l2-cache-size=4096',
                       '-mtune=skylake']
        
    def build(self):
        options = ["--enable-glx-tls", 
                   "--enable-gles1",
                   "--enable-gles2",
                   "--with-dri-drivers=i965,i915",

                   # disable video drivers:
                   # bbe6f7f865cd4316b5f885507ee0b128a20686eb
                   # caused build failure unrelated to intel mesa
                   # team.
                   "--disable-xvmc",
                   "--disable-vdpau",

                   # gallium tested with mesa-buildtest
                   "--without-gallium-drivers"]

        save_dir = os.getcwd()
        bd = self._build_dir + "/skl"
        if not os.path.exists(bd):
            os.makedirs(bd)
        os.chdir(bd)

        flags = " ".join(self._flags)
        flags = ["CFLAGS=-O2 " + flags,
                 "CXXFLAGS=-O2 " + flags,
                 "CC=ccache gcc",
                 "CXX=ccache g++"]
        cmd = [self._src_dir + "/autogen.sh"] + flags + options
        bs.run_batch_command(cmd)
        bs.run_batch_command(["make", "-j", str(bs.cpu_count()),
                              "install"],
                             env={"DESTDIR" : "/tmp/build_root/" + self.opts.arch + "/skl"} )
        os.chdir(save_dir)
        bs.Export().export_perf()

    def clean(self):
        pm = bs.ProjectMap()
        bs.git_clean(pm.project_source_dir("mesa"))
        bs.rmtree(self._build_dir)

    def test(self):
        pass
       
bs.build(MesaPerf())
