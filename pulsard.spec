Summary:	UPS monitoring program for MGE Pulsar UPSes
Summary(pl):	Program do monitorowania UPS-ów MGE Pulsar
Name:		pulsard
Version:	1.0.1
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://download.sourceforge.net/pulsard/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-newinit.patch
URL:		http://pulsard.sourceforge.net/
BuildRequires:	libgpio-devel >= 0.0.2
BuildRequires:	automake
BuildRequires:	autoconf
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pulsard is a monitoring software for MGE Pulsar UPSes.

%description -l pl
Pulsard to program monitoruj±cy dla UPS-ów MGE Pulsar.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_sysconfdir}/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
	%{_sysconfdir}/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"%{_sysconfdir}/rc.d/init.d/%{name} start\" to start pulsard ups daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_var}/lock/subsys/%{name} ]; then
		%{_sysconfdir}/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS Protocol README
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/sysconfig/*
%{_mandir}/man?/*
