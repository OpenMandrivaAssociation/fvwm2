%define	name	fvwm2
%define	version	2.5.18
%define	release	%mkrel 4

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	An improved version of the FVWM X-based window manager
URL: 		http://www.fvwm.org/
Source0:	ftp://ftp.fvwm.org/pub/fvwm/version-2/fvwm-%{version}.tar.bz2
Source1:    fvwm2.png
Source4:	fvwm2
Source8:	system.fvwm2rc
Source9:	configuration
Patch:      fvwm-2.5.18-translucent-menus.diff
License:	GPL
Group:		Graphical desktop/FVWM based
Provides:	    fvwm
BuildRequires:	flex
BuildRequires:	libx11-devel
BuildRequires:	libxt-devel
BuildRequires:  libxft-devel
BuildRequires:	xpm-devel
BuildRequires:	png-devel
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:	gtk+1.2-devel
BuildRequires:  fribidi-devel
BuildRequires:  rplay-devel
BuildRequires:  libstroke-devel
Buildroot:      %{_tmppath}/%{name}-%{version}

%description
FVWM2 (the F stands for whatever you want, but the VWM stands for Virtual
Window Manager) is an improved version of the FVWM window manager for the X
Window System and shares the same characteristics as FVWM.

Install the fvwm2 package if you'd like to use the FVWM2 window manager. If you
install fvwm2, you'll also need to install fvwm2-icons.

%package	gtk
Summary:	Gtk module for FVWM
Group:		Graphical desktop/FVWM based
Requires:	fvwm2

%description	gtk
Gnome/GTK module for FVWM

%prep
%setup -q -n fvwm-%{version}
%patch -p 1

%build
%configure \
    --disable-gtktest \
    --libexecdir=%{_libdir}/X11/fvwm2 \
    --sysconfdir=%{_sysconfdir}/X11/fvwm2 \
    --with-imagepath=%{_datadir}/icons


%make LOCALEDIR=%{_datadir}/locale localedir=%{_datadir}/locale

%install
rm -rf %{buildroot}
%{makeinstall_std} LOCALEDIR=%{_datadir}/locale localedir=%{_datadir}/locale

install -d -m 755 %{buildroot}%{_iconsdir}
install -m 644 %{SOURCE1} %{buildroot}%{_iconsdir}

mkdir -p %{buildroot}%{_sysconfdir}/X11/fvwm2
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/X11/fvwm2
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/X11/fvwm2

mkdir -p %{buildroot}%{_sysconfdir}/menu.d
install -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/menu.d

# session stuff
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat > %{buildroot}%{_sysconfdir}/X11/wmsession.d/09fvwm2 << EOF
NAME=Fvwm2
ICON=fvwm2.png
EXEC=%{_bindir}/fvwm2
DESC=A popular window manager
SCRIPT:
exec %{_bindir}/fvwm2
EOF

# OT fvwm is fvwm1
rm -f %{buildroot}%{_bindir}/fvwm2
mv %{buildroot}%{_bindir}/fvwm %{buildroot}%{_bindir}/fvwm2

%find_lang %name --all-name

%files -f %name.lang
%defattr(-,root,root)
%doc INSTALL README AUTHORS INSTALL.fvwm NEWS ChangeLog docs
%config(noreplace) %{_sysconfdir}/X11/fvwm2
%config(noreplace) %{_sysconfdir}/menu.d/fvwm2
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/09fvwm2
%{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/fvwm
%{_libdir}/X11/fvwm2
%{_iconsdir}/%{name}.png
%exclude %{_libdir}/X11/fvwm2/fvwm/%{version}/FvwmGtk

%files gtk
%defattr(-,root,root)
%doc modules/FvwmGtk/TODO
%{_libdir}/X11/fvwm2/fvwm/%{version}/FvwmGtk

%post
%update_menus
%make_session

%postun
%clean_menus
%make_session

%clean
rm -rf %{buildroot}


