%define		php_name	php%{?php_suffix}
%define		modname	suhosin
Summary:	Advanced protection system for PHP installations
Summary(pl.UTF-8):	Zaawansowany system zabezpieczeń dla instalacji PHP
Name:		%{php_name}-%{modname}
# NOTE: 0.9.35 drops support for PHP < 5.4, so do not upgrade until pld th main php is still 5.3
# NOTE: can't find tarball for 0.9.34
Version:	0.9.33
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://download.suhosin.org/%{modname}-%{version}.tgz
# Source0-md5:	0ce498a02a8281e4274ea8e390c2b487
URL:		http://www.hardened-php.net/suhosin/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-suhosin < 0.9.33-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Suhosin is an advanced protection system for PHP installations. It was
designed to protect servers and users from known and unknown flaws in
PHP applications and the PHP core.

Unlike Hardening-Patch Suhosin is binary compatible to normal PHP
installation, which means it is compatible to 3rd party binary
extension like ZendOptimizer.

%description -l pl.UTF-8
Suhosin to zaawansowany system zabezpieczeń dla instalacji PHP. Został
zaprojektowany do ochrony serwerów i użytkowników przed znanymi i
nieznanymi lukami w aplikacjach PHP i samym PHP.

W przeciwieństwie do łaty Hardening-Patch Suhosin jest binarnie
kompatybilny ze zwykłą instalacją PHP, co oznacza, że jest
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
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cp -p %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
