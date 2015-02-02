%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define module_name atomhopper

Name:           python-%{module_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Python language bindings for Atom Hopper

License:        ASLv2
URL:            https://github.com/rackerlabs/python-atomhopper
Source0:        %{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       python-requests
Requires:       python-simplejson
Requires:       python-jinja2
Requires:       python-lxml
Requires:       python-pecan

%description

%prep
%setup -q -n %{module_name}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%doc README.md LICENSE.md CHANGELOG
%{python_sitelib}/*
%attr(0755,-,-) %{_bindir}/ahc

%changelog
* Thu Jan 29 2015 Greg Swift <gregswift@gmail.com> - 1.0.0-1
- Updated release

* Fri Sep 6 2013 Greg Swift <gregswift@gmail.com> - 0.1.0-1
- Initial spec
