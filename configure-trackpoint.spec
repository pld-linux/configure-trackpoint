#
# Conditional build:
%bcond_without	gnome	# don't build gnome configurator
#
%define		_name	trackpoint
Summary:	TrackPoint configuration service for IBM laptops
Summary(pl.UTF-8):	Usługa konfigurująca TrackPointa do laptopów IBM
Name:		configure-trackpoint
Version:	0.3.3
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/tpctl/%{name}-%{version}.tar.gz
# Source0-md5:	081b361f77d8510f3dab293b58d7a30d
Source1:	%{name}.init
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-makefile.patch
URL:		http://tpctl.sourceforge.net/
%if %{with gnome}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libgnomeui-devel
BuildRequires:	pkgconfig
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
# trackpoint subsystem via sysfs
#Requires:	uname(release) >= 2.6.11
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TrackPoint configuration service for IBM laptops.

%description -l pl.UTF-8
Usługa konfigurująca TrackPointa do laptopów IBM.

%package gnome
Summary:	GNOME TrackPoint configuration tool for IBM laptops
Summary(pl.UTF-8):	Narzędzie konfiguracyjne TrackPointa do laptopów IBM
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gnome
GNOME TrackPoint configuration tool for IBM laptops.

%description gnome -l pl.UTF-8
Narzędzie konfiguracyjne TrackPointa do laptopów IBM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%if %{with gnome}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/%{_name}}

%if %{with gnome}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{name}/%{_name}.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
%endif

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{_name}
install etc/trackpoint/trackpoint.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{_name}/%{_name}.conf
> $RPM_BUILD_ROOT%{_sysconfdir}/%{_name}/%{_name}.conf.bak

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{_name}
%service %{_name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{_name} stop
	/sbin/chkconfig --del %{_name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr (754,root,root) /etc/rc.d/init.d/%{_name}
%dir %{_sysconfdir}/%{_name}
%attr (754,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{_name}/%{_name}.conf
%attr (754,root,root) %ghost %{_sysconfdir}/%{_name}/%{_name}.conf.bak

%if %{with gnome}
%files gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%endif
