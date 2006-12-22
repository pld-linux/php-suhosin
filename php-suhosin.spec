%define		_modname	suhosin
Summary:	Advanced protection system for PHP installations
Summary(pl):	Zaawansowany system zabezpieczeñ dla instalacji PHP
Name:		php-%{_modname}
Version:	0.9.16
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://www.hardened-php.net/suhosin/_media/%{_modname}-%{version}.tgz
# Source0-md5:	83db16381732218d0d44fe60988dcaaa
URL:		http://www.hardened-php.net/suhosin/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Suhosin is an advanced protection system for PHP installations. It was
designed to protect servers and users from known and unknown flaws in
PHP applications and the PHP core.

Unlike Hardening-Patch Suhosin is binary compatible to normal PHP
installation, which means it is compatible to 3rd party binary
extension like ZendOptimizer.

%description -l pl
Suhosin to zaawansowany system zabezpieczeñ dla instalacji PHP. Zosta³
zaprojektowany do ochrony serwerów i u¿ytkowników przed znanymi i
nieznanymi lukami w aplikacjach PHP i samym PHP.

W przeciwieñstwie do ³aty Hardening-Patch Suhosin jest binarnie
kompatybilny ze zwyk³± instalacj± PHP, co oznacza, ¿e jest
kompatybilny z binarnymi rozszerzeniami innych producentów, takimi jak
ZendOptimizer.

%prep
%setup -q -n suhosin-%{version}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
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
