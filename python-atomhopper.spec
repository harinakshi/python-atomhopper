%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define module atomhopper

Name:           python-${module}
Version:        0.1.0
Release:        1%{?dist}
Summary:        Python language bindings for Atom Hopper

License:        ASLv2
URL:            https://github.com/rackerlabs/python-atomhopper
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       python-requests
Requires:       python-simplejson
Requires:       python-jinja2
Requires:       pyrax


%description

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*
#%{_bindir}/

%changelog
* Fri Sep 6 2013 Greg Swift <gregswift@gmail.com> - 0.1.0-1
- Initial spec
