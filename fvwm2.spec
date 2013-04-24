# These are bogus as they're all internal, nothing else can use 'em
# The perl-Gtk requires is also not really necessary
# Inspired by Fedora - AdamW 2008/08
%define __noautoreq 'perl(\\(FvwmCommand\\)|\\(FVWM::|\\(General::)'
%define __noautoprov 'perl(\\(FvwmCommand\\)|\\(FVWM::|\\(General::)'

Name:		fvwm2
Version:	2.6.5
Release:	1
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
Patch1:		fvwm-2.6.5-rosa-www-browser.patch
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
# for www-browser
Requires:	desktop-common-data
# for fvwm-bug
Requires:	sendmail-command
# for fvwm-menu-headlines
Requires:	xdg-utils
# for fvwm-menu-xlock
Requires:	xlockmore
# for auto-menu generation
Requires:	imagemagick pyxdg
Requires:	xterm
Requires:	xdg-compliance-menu
# for mimeinfo
#Requires:	perl-File-MimeInfo
BuildRequires:	flex
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xt)
BuildRequires:  pkgconfig(xft)
BuildRequires:	xpm-devel
BuildRequires:	png-devel
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:  fribidi-devel
BuildRequires:  rplay-devel
BuildRequires:  libstroke-devel
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(xinerama)

%description
FVWM2 (the F stands for whatever you want, but the VWM stands for Virtual
Window Manager) is an improved version of the FVWM window manager for the X
Window System and shares the same characteristics as FVWM.

%prep
%setup -q -n fvwm-%{version}
%patch0 -p0 -b .translucent
%patch1 -p1 -b .www
#patch2 -p1 -b .mime
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



%changelog
* Tue Feb 15 2011 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 2.5.26-3mdv2011.0
+ Revision: 637848
- Require xdg-compliance-menu (moved from desktop-common-data)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 2.5.26-2mdv2011.0
+ Revision: 437611
- rebuild

* Sat Apr 04 2009 Funda Wang <fwang@mandriva.org> 2.5.26-1mdv2009.1
+ Revision: 363986
- fix str fmt
- rediff translucent menu patch

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Aug 06 2008 Adam Williamson <awilliamson@mandriva.org> 2.5.26-1mdv2009.0
+ Revision: 264127
- clean up a couple of variables
- buildrequires librsvg-devel and libxinerama-devel to enable these functions
  (thanks Fedora)
- drop the GTK+ 1.2 buildrequire (and hence the old and useless GTK+ 1.2 module)
- add several requires (thanks Fedora)
- new license policy
- sync patches with Fedora: add xdg-open.patch, mimeopen.patch and menu-generate.patch
- update to latest translucent-menus.diff from Gentoo
- add fvwm-xdg-menu.py as a source (from Fedora, needed for a Fedora patch)
- reorder sources
- fix indentations
- get rid of some bogus requires and provides (thanks Fedora)
- remove some unnecessary %%defines
- new release 2.5.26

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.5.21-4mdv2009.0
+ Revision: 245567
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Mar 13 2008 Andreas Hasenack <andreas@mandriva.com> 2.5.21-2mdv2008.1
+ Revision: 187612
- rebuild for 2008.1

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue May 22 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.21-1mdv2008.0
+ Revision: 29904
- new version


* Thu Jan 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.18-4mdv2007.0
+ Revision: 110130
- revert to previous setup, with distinct configuration and menu files included from main configuration file

* Mon Dec 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.18-3mdv2007.1
+ Revision: 94775
- bump release
- buildrequires libxft-devel

* Fri Dec 08 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.18-2mdv2007.1
+ Revision: 92250
- return of the translucent menu patch

* Wed Nov 29 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.18-1mdv2007.1
+ Revision: 88337
- new version
  drop transclucy patch (merged upstream)

* Thu Nov 16 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.10-9mdv2007.1
+ Revision: 84723
- new release
- fix buildrequires name
- bump release
- fix buildrequires
- bump release
- removed unused macros
- unused anymore
- move icons into a distinct source package, as they are distributed separatly
- fix menus
- no more need for the cursor hack
- add icon in wmsession script
- switch to new menu conversion system
- no need for menu entries
- patch is now uncompressed
- use a single configuration file, as twm
- uncompressed all additional sources
- icons are now generated with convert
- revert previous change, seems this menu template is needed after all
- don't ship default menu, let's use standard menu system
- unused anymore
- convert old menu to new xdg menu
  fix old menu to use png icons
  use fvwm2 icons set
- drop old obsoletes
- %%{1}mdv2007.1
- spec cleanup
- fix prefix
- fix buildrequires
- Import fvwm2

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.5.10-5mdk
- rebuild for new readline

* Sun Jul 25 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.5.10-4mdk
- From Philippe Reynes <trem@zarb.org> 
    - fix the compilation problem

* Sun Jun 13 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.5.10-3mdk
- Fix missing binary (Thanks Gregoire Favre <Gregoire.Favre@freesurf.ch>)

* Fri Jun 11 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.5.10-2mdk
- apply transparency patch0 (ask by Yves Brissaud)

* Fri Jun 11 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.5.10-1mdk
- 2.5.10

* Fri Apr 23 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.4.18-1mdk
- 2.4.18

