#!/usr/bin/python
import os
import subprocess
import re
import socket
import commands

cols = "{0:<32}{1:<22}"
f = cols.format
print f("CHECK", "STATUS")
print "--------------------------------------------"

### SET SOME VARS FOR SYSTEM RUN ON:
mem_expect = 117
cpu_expect = 12
services = {"ipmi": False, "ipmievd": False, "nfs": False, "sgi-tempo-configuration": False, "systemd-tmpfiles-clean": False, "systemd-tmpfiles-setup": False, "after-local": True, "ap
ache2": True, "booted": True, "cmcdetectd": True, "conserver": True, "cron": True, "dbus": True, "dhcpd": True, "dm-event": True, "gmetad": True, "gmond": True, "haveged": True, "irqb
alance": True, "iscsi": True, "jexec": True, "kdump": True, "kmod-static-nodes": True, "libvirtd": True, "lk": True, "lldpad": True, "mysql": True, "named": True, "nfs-config": True, 
"nfs-idmapd": True, "nfs-mountd": True, "nfs-server": True, "nscd": True, "ntpd": True, "plymouth-start": True, "postfix": True, "rc-local": True, "rpc-statd": True, "rpcbind": True, 
"rsyslog": True, "sdr_logger": True, "sel_logger": True, "sgi-database-update": True, "sgi-power": True, "sgi_het": True, "smcrbd": True, "snmptrapd": True, "sshd": True, "SuSEfirewal
l2": True, "SuSEfirewall2_init": True, "sysstat": True, "systemd-journald": True, "systemd-logind": True, "systemd-modules-load": True, "systemd-random-seed": True, "systemd-remount-f
s": True, "systemd-sysctl": True, "systemd-tmpfiles-setup-dev": True, "systemd-udev-root-symlink": True, "systemd-udev-trigger": True, "systemd-udevd": True, "systemd-update-utmp": Tr
ue, "systemd-vconsole-setup": True, "systemimager-server-netbootmond": True, "systemimager-server-rsyncd": True, "tempo_imaging_auto_script": True, "warp_time_before_ntp": True, "wick
ed": True, "wickedd-auto4": True, "wickedd-dhcp4": True, "wickedd-dhcp6": True, "wickedd-nanny": True, "wickedd": True, "xinetd": True}
mounts = {'/mount1': True, '/mount2: False, '/mount1/home': False, '/mount2/bin': False,}
fsspace = {'/tmp': 95, '/': 90}

def get_fsspace(mnt):
        return int(commands.getoutput('df {0}'.format(mnt)).split('\n')[1].split()[4][:-1])

def get_memory():
        totalMemory = os.popen("free -g").readlines()[1].split()[1]
        return int(totalMemory)

def cpuTest():
        cpuCount = os.sysconf(os.sysconf_names["SC_NPROCESSORS_ONLN"])
        return int(cpuCount)

def is_service_running(svc):
        with open(os.devnull, 'wb') as hide_output:
                exit_code = subprocess.Popen(['systemctl', 'status', svc], stdout=hide_output, stderr=hide_output).wait()
                return exit_code == 0

def is_mounted(mnt):
        mounted = os.path.ismount(mnt)
        return mounted

###     MEMORY
M = get_memory()
if M == mem_expect:
    print f("MEMORY:", "PASS") 
else:
        print f("MEMORY:", "FAIL <-- is %s, but should be %s" % (M, mem_expect))

###     CPU COUNT
C = cpuTest()
if C == cpu_expect:
                print f("CPU ONLINE:", "PASS")
else:
                print f("CPU ONLINE:", "FAIL <-- is %s but should be %s" % (C, cpu_expect))

###     SERVICES CHECKS
errs = 0
for svc, value in services.iteritems():
        if is_service_running(svc) and value is True:
                next
        elif is_service_running(svc) and value is False:
                print f("SERVICE %s:" % svc.upper(), "FAIL <-- Unexpected Service")
                errs += 1
        elif not is_service_running(svc) and value is False:
                next
        else:   
                print f("SERVICE %s:" % svc.upper(), "FAIL <--")
                errs += 1
if errs is 0:
        print f("SERVICES:", "PASS")

###     MOUNTS
errs = 0
for mnt, value in mounts.iteritems():
        if is_mounted(mnt) and value is True:
                next
        elif is_mounted(mnt) and value is False:
                print f("MOUNT %s:" % mnt.upper(), "FAIL <-- Unexpected Mount")
                errs += 1
        elif not is_mounted(mnt) and value is False:
                next
        elif not is_mounted(mnt) and value is True:
                print f("MOUNT %s:" % mnt.upper(), "FAIL <--")
                errs += 1
if errs is 0:
        print f("MOUNTS:", "PASS")

### FS SPACE CHECK
errs = 0
#try:
#       fsspace
#except:
#       print f("FS SPACE:", "PASS")
#else:
for mnt, value in fsspace.iteritems():
        if get_fsspace(mnt) < int(value):
                next
        else:
                print f("FS SPACE %s:" % mnt.upper(), "FAIL <--")
                errs += 1
if errs is 0:
        print f("FS SPACE:", "PASS")
