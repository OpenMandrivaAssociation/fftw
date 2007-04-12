%define name 	fftw
%define version 3.1.2
%define release %mkrel 2

%define major 	3
%define libname %mklibname %{name} %{major}

# define fortran compiler to use
# XXX where is it used for real?
%if %{mdkversion} >= 200600
%define fortran_compiler gfortran
BuildRequires: gcc-gfortran
%else
%define fortran_compiler g77
BuildRequires: gcc-g77
%endif

# do "make check" by default
%define do_check 1
%{?_without_check: %global do_check 0}

Name: 		%{name}
Summary: 	Fast fourier transform library
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Libraries
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: 	%{name}-%{version}.tar.bz2
# (gb) 3.0.1-6mdk libtool 1.4 fixes, don't bother with aclocal machinery
#Patch0:		fftw-3.0.1-libtool.patch.bz2
URL: 		http://www.fftw.org/
BuildRequires:	autoconf2.5 >= 2.54

%description
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.

%package 	wisdom
Summary:	FFTW-wisdom file generator
Group:		Development/Other

%description 	wisdom
fftw-wisdom is a utility to generate FFTW wisdom files, which contain saved
information about how to optimally compute (Fourier) transforms of various
sizes.

%package -n 	%libname
Summary: 	Fast fourier transform library
Group: 		System/Libraries
Provides: 	%name
Obsoletes:	%name

%description -n %libname
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.

%package -n %libname-devel
Summary: Headers, libraries, & docs for FFTW fast fourier transform library
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: fftw3-devel = %version-%release
Provides: %{name}-devel = %{version}-%{release}

%description -n %libname-devel
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier
transform library.

%prep
%setup -q
#%patch0 -p1 -b .libtool
#autoconf

%build
export F77="%{fortran_compiler}"
mkdir build-std
pushd build-std
CONFIGURE_TOP=.. %configure2_5x --enable-shared --enable-threads --infodir=$RPM_BUILD_ROOT%{_infodir}
%make
popd
mkdir build-float
pushd build-float
CONFIGURE_TOP=.. %configure2_5x --enable-float --enable-shared --enable-threads --infodir=$RPM_BUILD_ROOT%{_infodir}
%make
popd

# checking
%if %{do_check}
%make check -C build-std
%make check -C build-float
%endif

%install
rm -fr $RPM_BUILD_ROOT
pushd build-std
%makeinstall
popd
pushd build-float
%makeinstall
popd

rm -fr $RPM_BUILD_ROOT/%{_docdir}/Make*

%clean
rm -rf ${RPM_BUILD_ROOT}

%post   -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%post -n %libname-devel
%__install_info -e '* FFTW: (fftw).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw3.info.bz2 %{_infodir}/dir

%preun -n %libname-devel
%__install_info -e '* FFTW: (fftw).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw3.info.bz2 %{_infodir}/dir --remove

%files -n %name-wisdom
%defattr (-,root,root)
%{_bindir}/fftw*-wisdom
%{_bindir}/fftw-wisdom-to-conf
%{_includedir}/fftw3.f
%{_mandir}/man1/fftw-wisdom-to-conf.1.bz2
%{_mandir}/man1/fftw*-wisdom.1.bz2

%files -n %libname
%defattr (-,root,root)
%doc AUTHORS CO* NEWS README TODO 
%{_libdir}/libfftw*.so.*

%files -n %libname-devel
%defattr (-,root,root)
%{_includedir}/*fftw*.h
%doc %{_infodir}/*
%doc doc/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libfftw*.a
%{_libdir}/libfftw*.la
%{_libdir}/libfftw*.so


