%define name	jackmix
%define version	0.1.0.r1
%define release %mkrel 6
%define major 0
%define libname %mklibname %{name} %major

Name: 	 	%{name}
Summary: 	Fancy mixer for JACK audio server
Version: 	%{version}
Release: 	%{release}

Source:		http://roederberg.dyndns.org/~arnold/file_share/jackmix/%{name}-%{version}.tar.bz2
Patch0:		jackmix-0.1.0.r1-autotools.patch
Patch1:		jackmix-0.1.0.r1-x86_64.patch
URL:		https://pilatus.roederberg.dyndns.org/~arnold/jackmix/
License:	GPL
Group:		Sound
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	qt3-devel jackit-devel liblo-devel
Requires: 	%libname = %version-%release

%description
Ever struggled with a number of jack applications on your desktop everyone
using its own master volume-fader but not one common place for all the
volumes directly accessible?

The solution to your problem is JackMix, a mixer app for jack that looks
exaclty like the mixer you would use if you had to connect your analog
equipment.

%package -n %libname
Summary: Fancy mixer for JACK audio server
Group: Sound

%description -n %libname
Ever struggled with a number of jack applications on your desktop everyone
using its own master volume-fader but not one common place for all the
volumes directly accessible?

The solution to your problem is JackMix, a mixer app for jack that looks
exaclty like the mixer you would use if you had to connect your analog
equipment.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
make -f Makefile.cvs 
%configure2_5x \
	--with-qt-dir=%{qt3dir} \
	--with-qt-includes=%{qt3include} \
	--with-qt-libraries=%{qt3lib}
# crappy fix for an error that should not be
perl -p -i -e 's/CXXLD\)/CXXLD\)\ \-L\/usr\/lib\/qt3\/lib\ \-ljack/g' jackmix/Makefile
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat << EOF > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=Mixer for JACK audio server
Icon=sound_section
Exec=%{name}
Terminal=false
Type=Application
Categories=Qt;Mixer;Audio;AudioVideo;
StartupNotify=false
EOF

rm -f %buildroot%_libdir/{*.la,libcore.so,libmixingelements.so,libqosc.so}

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%name
%{_datadir}/applications/*.desktop

%files -n %libname
%defattr(-, root, root)
%_libdir/*.so*
