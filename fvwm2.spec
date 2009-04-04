# These are bogus as they're all internal, nothing else can use 'em
# The perl-Gtk requires is also not really necessary
# Inspired by Fedora - AdamW 2008/08
%define _requires_exceptions perl(FvwmCommand)\\|perl(FVWM*\\|perl(General*\\|perl(Gtk*
%define _provides_exceptions perl(FvwmCommand)\\|perl(FVWM*\\|perl(General*

Name:		fvwm2
Version:	2.5.26
Release:	%{mkrel 1}
Summary:	An improved version of the FVWM X-based window manager
URL: 		http://www.fvwm.org/
Source0:	ftp://ftp.fvwm.org/pub/fvwm/version-2/fvwm-%{version}.tar.bz2
Source1:	fvwm2.png
Source2:	fvwm2
Source3:	system.fvwm2rc
Source4:	configuration
Source5:	http://www.cl.cam.ac.uk/~pz215/fvwm-scripts/scripts/fvwm-xdg-menu.py
# From Gentoo, which got it from fvwm-user mailing list; enables fast
# translucent menus - AdamW 2008/08
Patch0:		fvwm-2.5.26-translucent-menus.diff
# From Fedora: use xdg-open instead of 'netscape' - AdamW 2008/08
Patch1:		fvwm-2.5.21-xdg-open.patch
# From Fedora: use mimeopen instead of just opening files with an
# editor - AdamW 2008/08
Patch2:		fvwm-2.5.21-mimeopen.patch
# From Fedora: generate menu using fvwm-xdg-menu.py (external source
# above) instead of hardcoding it
Patch3:		fvwm-2.5.21-menu-generate.patch
Patch4:		fvwm-2.5.26-fix-str-fmt.patch
License:	GPLv2+
Group:		Graphical desktop/FVWM based
Requires:	fvwm-icons
# for fvwm-bug
Requires:	sendmail-command
# for fvwm-menu-headlines
Requires:	xdg-utils
# for fvwm-menu-xlock
Requires:	xlockmore
# for auto-menu generation
Requires:	imagemagick pyxdg
Requires:	xterm
# for mimeinfo
Requires:	perl-File-MimeInfo
BuildRequires:	flex
BuildRequires:	libx11-devel
BuildRequires:	libxt-devel
BuildRequires:  libxft-devel
BuildRequires:	xpm-devel
BuildRequires:	png-devel
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:  fribidi-devel
BuildRequires:  rplay-devel
BuildRequires:  libstroke-devel
BuildRequires:	librsvg-devel
BuildRequires:	libxinerama-devel
Buildroot:      %{_tmppath}/%{name}-%{version}

%description
FVWM2 (the F stands for whatever you want, but the VWM stands for Virtual
Window Manager) is an improved version of the FVWM window manager for the X
Window System and shares the same characteristics as FVWM.

%prep
%setup -q -n fvwm-%{version}
%patch0 -p0 -b .translucent
%patch1 -p1 -b .xdgopen
%patch2 -p1 -b .mime
%patch3 -p1 -b .generate
%patch4 -p0 -b .str

%build
%configure2_5x \
    --disable-gtk \
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
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/fvwm2
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/X11/fvwm2

mkdir -p %{buildroot}%{_sysconfdir}/menu.d
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/menu.d

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

# menus
install -D -m0755 -p %{SOURCE2} %{buildroot}%{_bindir}/fvwm-xdg-menu

%find_lang %{name} --all-name

%files -f %{name}.lang
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

%post
%if %mdkversion < 200900
%update_menus
%endif
%make_session

%postun
%if %mdkversion < 200900
%clean_menus
%endif
%make_session

%clean
rm -rf %{buildroot}


