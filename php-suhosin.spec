%define		_modname	suhosin
Summary:	%{_modname} - advanced protection system for PHP installations
Name:		php-%{_modname}
Version:	0.9.24
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://download.suhosin.org/suhosin-%{version}.tgz
# Source0-md5:	1a0711bb4aaba90cc870611c503d1468
URL:		http://www.hardened-php.net/suhosin/index.html
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Suhosin is an advanced protection system for PHP installations. It was
designed to protect servers and users from known and unknown flaws in
PHP applications and the PHP core. Suhosin comes in two independent
parts, that can be used separately or in combination. The first part
is a small patch against the PHP core, that implements a few low-level
protections against bufferoverflows or format string vulnerabilities
and the second part is a powerful PHP extension that implements all
the other protections.

%prep
%setup -q -n %{_modname}-%{version}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
