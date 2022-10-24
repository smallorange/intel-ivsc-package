# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
%define buildforkernels current
#define buildforkernels akmod

%define repo rpmfusion

# name should have a -kmod suffix
Name:           intel-ivsc-kmod

Version:        0.0.1
Release:        1%{?dist}.1
Summary:        Intel iVSC Kernel module(s)

Group:          System Environment/Kernel

License:        GPL-2.0
URL:            https://github.com/intel/ivsc-driver
Source0:        https://github.com/smallorange/ivsc-driver/releases/download/v0.0.1-alpha/ivsc-driver-0.0.1.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{_bindir}/kmodtool


# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
ExclusiveArch:  x86_64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
# kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
# pushd foo-%{version}
# #patch0 -p1 -b .suffix
# popd

mv ivsc-driver-%{version}-alpha ivsc-driver-%{version}

for kernel_version in %{?kernel_versions} ; do
    cp -a ivsc-driver-%{version} _kmod_build_${kernel_version%%___*}
done


%build
echo %{?_smp_mflags}

for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    # make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}

    install -D -m 755 _kmod_build_${kernel_version%%___*}/gpio-ljca.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/gpio-ljca.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/intel_vsc.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/intel_vsc.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/ljca.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ljca.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/mei-vsc.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei-vsc.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_pse.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_pse.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/spi-ljca.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/spi-ljca.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_csi.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_csi.ko
    install -D -m 755 _kmod_build_${kernel_version%%___*}/mei_ace_debug.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/mei_ace_debug.ko
done
%{?akmod_install}


#%clean
#rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Oct 13 2022 Kate Hsuan <hpa@redhat.com> - 3:520.56.06-1
- First build
