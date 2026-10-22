%define		php_name	php%{?php_suffix}
%define		modname	suhosin
Summary:	Advanced protection system for PHP installations
Summary(pl.UTF-8):	Zaawansowany system zabezpieczeń dla instalacji PHP
Name:		%{php_name}-%{modname}
# for PHP 5.3, see PHP_5_3 branch
Version:	0.9.38
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://download.suhosin.org/%{modname}-%{version}.tar.gz
# Source0-md5:	0c26402752b0aff69e4b891f062a52bf
Patch0:		php-suhosin-rfc1867-php-sync.patch
Patch1:		php-suhosin-bug78875.patch
Patch2:		php-suhosin-cve-2023-0662.patch
Patch3:		php-suhosin-cve-2024-8925.patch
Patch4:		php-suhosin-rfc1867-header-leak.patch
Patch5:		php-suhosin-cve-2026-109618.patch
Patch6:		php-suhosin-request-state.patch
Patch7:		php-suhosin-extract-globals.patch
Patch8:		php-suhosin-upload-totalname-length.patch
URL:		http://www.suhosin.org/stories/
BuildRequires:	%{php_name}-devel >= 4:5.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
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
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1

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
