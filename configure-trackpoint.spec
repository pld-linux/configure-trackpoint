%define		_name	trackpoint
Summary:	GNOME TrackPoint configuration tool for IBM laptops
Summary(pl):	Narzêdzie konfiguracyjne TrackPointa do laptopów IBM
Name:		configure-trackpoint
Version:	0.3.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/tpctl/%{name}-%{version}.tar.gz
# Source0-md5:	081b361f77d8510f3dab293b58d7a30d
Source1:	%{name}.init
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-makefile.patch
URL:		http://tpctl.sourceforge.net/http://tpctl.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libgnomeui-devel
Requires(post,preun):	/sbin/chkconfig
#Requires:	kernel >= 2.6.11 (with trackpoint subsystem via sysfs)
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME TrackPoint configuration tool for IBM laptops.

%description -l pl
Narzêdzie konfiguracyjne TrackPointa do laptopów IBM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/%{_name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{_name}
install etc/trackpoint/trackpoint.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{_name}/%{_name}.conf
> $RPM_BUILD_ROOT%{_sysconfdir}/%{_name}/%{_name}.conf.bak
ln -sf %{name}/%{_name}.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

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
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*
%{_pixmapsdir}/*
