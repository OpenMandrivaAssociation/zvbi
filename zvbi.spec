%define libname %mklibname %name 0
%define develname %mklibname %name -d

Name: zvbi
Version: 0.2.33
Release: 7
Summary: Raw VBI, Teletext and Closed Caption decoding library
License: GPL
Group: Video
Url: http://zapping.sourceforge.net/
Source0:    http://prdownloads.sourceforge.net/zapping/%name-%version.tar.bz2
Patch0: zvbi-0.2.31-linkage_fix.diff
Patch2: zvbi-0.2.7-fix-build.patch
Patch3: zvbi-0.2.33-include_stat_h.patch
Patch4: zvbi-0.2.33-libpng15.patch
BuildRequires:	libx11-devel
BuildRequires:	gtk-doc
BuildRequires:	libpng-devel
BuildRequires:	doxygen
BuildRequires:	gettext-devel
Requires: gettext >= 0.10.36

%description
Non versionated files of zvbi, mainly libzvbi0 translations

%package -n %{libname}
Summary: Raw VBI, Teletext and Closed Caption decoding library
Group: Video
%description -n %{libname}
VBI stands for Vertical Blanking Interval, a gap between the image
data transmitted in an analog video signal. This gap is used to
transmit AM modulated data for various data services like Teletext and
Closed Caption.

The zvbi library provides routines to:
* read from raw VBI sampling devices (both V4L and V4L2 API are supported),
* a versatile raw vbi bit slicer,
* decoders for various data services and basic search,
* demodulate raw to sliced VBI data,
* interpret the data of several popular services.
* render and export functions for text pages.

The library is the vbi decoding backbone of the Zapping Gnome TV viewer
and Zapzilla Teletext browser.


%package -n %{develname}
Summary: Header files for developing apps which will use libzvbi
Group: Development/C
Requires: %{libname} = %{version}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel
Obsoletes: %{name}-devel
Obsoletes: %{mklibname zvbi 0 -d}

%description -n %{develname}
Header files and static library of bzip2 functions, for developing apps which
will use the zvbi library (aka libzvbi)

%prep
%setup -q
%patch0 -p1 -b .linkage_fix
%patch2 -p0 -b .build
%patch3 -p1 -b .stat
%patch4 -p1 -b .libpng15~

%build
autoreconf -fi

%configure2_5x
# gtkdoc fix:
cp /usr/share/gtk-doc/data/gtkdoc-common.pl doc/
%make

%install
rm -rf %{buildroot}
%{makeinstall_std}
%find_lang %name
             
%clean
rm -rf %{buildroot}


%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %_bindir/*
%attr(755,root,root) %_sbindir/*
%_mandir/man1/*


%files -n %libname
%defattr (-, root, root)
%doc AUTHORS COPYING NEWS README
%_libdir/libzvbi*.so.*

%files -n %{develname}
%defattr(644,root,root,755)
%doc BUGS ChangeLog COPYING TODO doc/html
%_libdir/lib*.so
%_libdir/lib*.a
%_libdir/pkgconfig/*
%_includedir/libzvbi.h


