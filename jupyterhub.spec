%define debug_package %{nil}
%global debug_package %{nil}

%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%define _binaries_in_noarch_packages_terminate_build   0

Name:           jupyterhub
Version:        0.9.4
Release:        1%{?dist}
Summary:        A multi-user server for Jupyter notebooks

License:        BSD
URL:            https://github.cop/jupyter/%{name}
Source0:        https://github.com/jupyter/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python36-devel
BuildRequires:  python36-setuptools
BuildRequires:  nodejs
BuildRequires:  git

Requires:       nodejs
Requires:       python36

%description
JupyterHub is a multi-user server that manages and proxies multiple instances
of the single-user Jupyter notebook server.

Three actors:

 *  multi-user Hub (tornado process)
 *  configurable http proxy (node-http-proxy)
 *  multiple single-user IPython notebook servers (Python/IPython/tornado)

Basic principles:

 *  Hub spawns proxy
 *  Proxy forwards ~all requests to hub by default
 *  Hub handles login, and spawns single-user servers on demand
 *  Hub configures proxy to forward url prefixes to single-user servers


%prep
%setup -q


%build
python36 setup.py build
easy_install-3.6 pip

%install
python36 setup.py install --skip-build --root %{buildroot}
pip3 install --target %{buildroot}/usr/lib/python3.6/site-packages -r %{_builddir}/%{name}-%{version}/requirements.txt
pip3 install --target %{buildroot}/usr/lib/python3.6/site-packages notebook jupyter

npm install -g --prefix %{buildroot}/usr/lib
npm install -g --prefix %{buildroot}/usr/lib configurable-http-proxy

mkdir -p %{buildroot}/etc/jupyterhub

%{buildroot}/usr/bin/jupyterhub --generate-config -f %{buildroot}/etc/jupyterhub/jupyterhub_config.py

mkdir -p %{buildroot}/usr/lib/systemd/system/
%{__cp} -rp %{_sourcedir}/jupyterhub.service %{buildroot}/usr/lib/systemd/system/

%files
%{_bindir}/jupyterhub
%{_bindir}/jupyterhub-singleuser
/usr/share/*
/usr/lib/*
/etc/jupyterhub/*

