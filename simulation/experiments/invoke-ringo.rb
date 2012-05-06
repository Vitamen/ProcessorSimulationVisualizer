#!/usr/bin/ruby

load "scripts/CONFIG.rb"

bmark_suite=ARGV[0]
bmark=ARGV[1]
expdir=ARGV[2]
outputdir=ARGV[3]
binrev=ARGV[4]
sim_cmdline=ARGV[5..-1].join ' '
#sim_cmdline += " -output #{outputdir}/sim.out -insn_output #{outputdir}/sim.insn"
sim_cmdline += " -output #{outputdir}/sim.out"

is_ckptrestore = (sim_cmdline =~ /-restore true/)

if File.exists? "#{outputdir}/sim.out"
    exit 0
end

basedir = find_suite(bmark_suite)
if basedir == nil
    $stderr.write "Could not find benchmark suite #{bmark_suite}.\n"
    exit 1
end

if not File.directory? "#{basedir}/#{bmark}"
    $stderr.write "Benchmark #{bmark} not found in #{basedir}.\n"
    exit 1
end

bmark_dir = "#{basedir}/#{bmark}"
args = File.readlines("#{bmark_dir}/args").join.strip
infile = File.readlines("#{bmark_dir}/input").join.strip

Dir.chdir bmark_dir
if is_ckptrestore
        c = "#{expdir}/bin/ringo.#{binrev} #{sim_cmdline}"
else
        c="#{expdir}/bin/ringo.#{binrev} #{sim_cmdline} -guest_stdin #{infile} -guest_stdout /dev/null -guest_stderr /dev/null -- #{args}"
end

$stderr.write "Simulator command: #{c}\n"
$stderr.write "CWD: #{Dir.pwd}\n"
system(c)