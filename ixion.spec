#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Generic formula compulation library
Summary(pl.UTF-8):	Ogólna biblioteka do obliczania wzorów
Name:		ixion
Version:	0.7.0
Release:	2
License:	MIT
Group:		Libraries
#Source0Download: http://gitorious.org/ixion/pages/Download
Source0:	http://kohei.us/files/ixion/src/libixion-%{version}.tar.bz2
# Source0-md5:	000157117801f9507f34b26ba998c4d1
Patch0:		%{name}-am.patch
URL:		http://gitorious.org/ixion/pages/Home
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.36
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	mdds-devel >= 0.7.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ixion aims to provide a library for calculating the results of formula
expressions stored in multiple named targets, or "cells". The cells
can be referenced from each other, and the library takes care of
resolving their dependencies automatically upon calculation. The
caller can run the calculation routine either in a single-threaded
mode, or a multi-threaded mode. The library also supports
re-calculation where the contents of one or more cells have been
modified since the last calculation, and a partial calculation of only
the affected cells gets performed. It is written entirely in C++, and
makes extensive use of the boost library to achieve portability across
different platforms.

%description -l pl.UTF-8
Projekt Ixion ma na celu dostarczenie biblioteki do obliczania wyników
wyrażeń określonych wzorami zapisanymi w wielu nazwanych miejscach -
"komórkach". Komórki mogą odwoływać się do siebie nawzajem, a
biblioteka dba o automatyczne rozwiązywanie ich zależności przy
obliczeniach. Procedura obliczająca może być wywołana w trybie
jednowątkowym lub wielowątkowym. Biblioteka obsługuje także ponowne
przeliczanie w przypadku zmiany zawartości jednej lub większej liczby
komórek od poprzednich obliczeń; wykonywane jest tylko przeliczanie
komórek, których zmiana dotyczy. Biblioteka jest napisana całkowicie w
C++ i intensywnie wykorzystuje bibliotekę boost, aby osiągnąć
przenośność na wiele platform.

%package devel
Summary:	Development files for ixion
Summary(pl.UTF-8):	Pliki nagłówkowe dla ixion
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.36
Requires:	libstdc++-devel
Requires:	mdds-devel >= 0.7.1

%description devel
This package contains the header files for developing applications
that use ixion.

%description devel -l pl.UTF-8
Pen pakiet zawiera pliki nagłówkowe do tworzenia aplikacji opartych na
ixion.

%package static
Summary:	Static ixion library
Summary(pl.UTF-8):	Statyczna biblioteka ixion
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ixion library.

%description static -l pl.UTF-8
Statyczna biblioteka ixion.

%prep
%setup -q -n libixion-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	boost_cv_lib_thread=yes \
	boost_cv_lib_thread_LIBS="-lboost_thread -lboost_system" \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/ixion-parser
%attr(755,root,root) %{_bindir}/ixion-sorter
%attr(755,root,root) %{_libdir}/libixion-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libixion-0.8.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libixion-0.8.so
%{_includedir}/libixion-0.8
%{_pkgconfigdir}/libixion-0.8.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libixion-0.8.a
%endif
