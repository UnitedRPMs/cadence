%global debug_package %{nil}

%global gitdate 20180409
%global commit0 99b39989a010fae1acbce07af002b15e56a1d161
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}


Name:           cadence
BuildRequires:  jack-audio-connection-kit-devel
#BuildRequires:  PyQt4-devel
BuildRequires:  python3-qt5-devel
BuildRequires:  python3-dbus
BuildRequires:	a2jmidid ladish python-rdflib 
#BuildRequires:	zita-ajbridge
BuildRequires:  qt-devel
BuildRequires:  alsa-lib-devel
BuildRequires:	desktop-file-utils

Requires: 	python3-qt5
Requires:	jack_capture
Recommends:     pulseaudio-module-jack
Recommends:     a2jmidid
Recommends:	zita-ajbridge
Recommends:	ladish

Url:            http://kxstudio.sf.net/cadence
License:        GPLv2
Group:		Applications/Multimedia
Version:        0.9.0
Release:        1%{?gver}%{dist}
Summary:        A JACK Audio Toolbox
Source0: 	https://github.com/falkTX/Cadence/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch:		cadence-desktop.path

%description
Cadence is a set of tools useful for audio production.
Cadence itself is also an application (the main one), which this page will 
document.
There are other applications that are part of the Cadence suite, they are 
usually named as the "Cadence tools".
They are:

    Catarina
    Catia
    Claudia

Some of these also have sub-tools, such as Cadence-JackMeter 
and Claudia-Launcher.


%prep
%autosetup -n Cadence-%{commit0} -p1
sed -i 's|AudioEditing;||g' data/catarina.desktop \
data/catia.desktop \
data/claudia.desktop \
data/claudia-launcher.desktop \

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
find . -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python3|#!%{__python3}|'
rm -R data/unity/

%build
export CXXFLAGS="%{optflags}"
export CFLAGS="%{optflags}"
STRIP=/bin/true BASE_FLAGS=
%make_build

%install
make install DESTDIR=%buildroot PREFIX="%_prefix"

chmod a+x %{buildroot}/usr/share/cadence/pulse2jack/*.pa

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop \
%{buildroot}%{_datadir}/applications/catarina.desktop \
%{buildroot}%{_datadir}/applications/catia.desktop \
%{buildroot}%{_datadir}/applications/claudia-launcher.desktop \

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc COPYING TODO INSTALL.md README.md
%{_bindir}/*
%dir %{_datadir}/cadence
%{_datadir}/cadence/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/
%{_sysconfdir}/X11/xinit/xinitrc.d/61cadence-session-inject
%{_sysconfdir}/xdg/autostart/cadence-session-start.desktop


%changelog

* Fri Aug 11 2017 David Vásquez <davidva AT tutanota DOT com> - 0.9.0-1-git99b3998
- Updated to 0.9.0-1-git99b3998

* Fri Aug 11 2017 David Vásquez <davidva AT tutanota DOT com> - 0.8.1-1-git3ba7de2
- Initial build
