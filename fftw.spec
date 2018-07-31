%define api 3
%define major 3
%define libname %mklibname %{name} %{api} %{major}
%define	libname_threads %mklibname %{name}%{api}_threads %{major}
%define	libname_omp %mklibname %{name}%{api}_omp %{major}
%define	libnamef %mklibname %{name}%{api}f %{major}
%define	libnamef_threads %mklibname %{name}%{api}f_threads %{major}
%define	libnamef_omp %mklibname %{name}%{api}f_omp %{major}
%define	libnamel %mklibname %{name}%{api}l %{major}
%define	libnamel_threads %mklibname %{name}%{api}l_threads %{major}
%define	libnamel_omp %mklibname %{name}%{api}l_omp %{major}
%define devname %mklibname %{name} -d

Summary:	Fast fourier transform library
Name:		fftw
Version:	3.3.8
Release:	2
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.fftw.org
Source0:	ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
Patch0:		fftw-3.3.4-clang.patch
BuildRequires:	gcc-gfortran
BuildRequires:	atomic-devel
%ifnarch %{armx} aarch64
BuildRequires:	quadmath-devel
%endif
BuildConflicts:	%{devname}

%description
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.

%package wisdom
Summary:	FFTW-wisdom file generator
Group:		Development/Other

%description wisdom
fftw-wisdom is a utility to generate FFTW wisdom files, which contain saved
information about how to optimally compute (Fourier) transforms of various
sizes.

%package -n %{libname}
Summary:	Fast fourier transform library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libname}
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.

%package -n %{libname_threads}
Summary:	Fast fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libname_threads}
This package contains a shared library for %{name}.

%package -n %{libname_omp}
Summary:	Fast OpenMP fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libname_omp}
This package contains a shared OpenMP library for %{name}.

%package -n %{libnamef}
Summary:	Fast fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libnamef}
This package contains a shared library for %{name}.

%package -n %{libnamef_threads}
Summary:	Fast fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libnamef_threads}
This package contains a shared library for %{name}.

%package -n %{libnamef_omp}
Summary:	Fast OpenMP fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libnamef_omp}
This package contains a shared OpenMP library for %{name}.

%package -n %{libnamel}
Summary:	Fast fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libnamel}
This package contains a shared library for %{name}.

%package -n %{libnamel_threads}
Summary:	Fast fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libnamel_threads}
This package contains a shared library for %{name}.

%package -n %{libnamel_omp}
Summary:	Fast OpenMP fourier transform library
Group:		System/Libraries
Conflicts:	%{_lib}fftw3 < 3.3.3-2

%description -n %{libnamel_omp}
This package contains a shared OpenMP library for %{name}.

%package -n %{devname}
Summary:	Headers, libraries, & docs for FFTW fast fourier transform library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libname_threads} = %{EVRD}
Requires:	%{libname_omp} = %{EVRD}
Requires:	%{libnamef} = %{EVRD}
Requires:	%{libnamef_threads} = %{EVRD}
Requires:	%{libnamef_omp} = %{EVRD}
Requires:	%{libnamel} = %{EVRD}
Requires:	%{libnamel_threads} = %{EVRD}
Requires:	%{libnamel_omp} = %{EVRD}
Provides:	%{name}%{api}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier
transform library.

%prep
%autosetup -p1

%build
export F77="gfortran"
mkdir build-std
pushd build-std
CONFIGURE_TOP=.. \
%configure \
	--disable-static \
	--enable-shared \
	--enable-threads \
	--enable-openmp \
	--enable-fortran \
%ifarch x86_64 znver1
	--disable-sse \
	--enable-sse2 \
	--enable-avx \
%endif
	--infodir=%{_infodir}

%make
popd

mkdir build-float
pushd build-float
CONFIGURE_TOP=.. \
%configure \
	--disable-static \
	--enable-float \
	--enable-shared \
	--enable-threads \
	--enable-openmp \
	--enable-fortran \
%ifarch x86_64 znver1
	--enable-sse \
	--enable-sse2 \
	--enable-avx \
%endif
	--infodir=%{_infodir}
%make
popd

# SSE doesn't work with long-double:
mkdir build-long-double
pushd build-long-double
CONFIGURE_TOP=.. \
%configure \
	--disable-static \
	--enable-long-double \
	--enable-shared \
	--enable-threads \
	--enable-fortran \
	--enable-openmp \
	--infodir=%{_infodir}
%make
popd

%install
%makeinstall_std -C build-std
%makeinstall_std -C build-float
%makeinstall_std -C build-long-double

rm -fr %{buildroot}/%{_docdir}/Make*

%files -n %{name}-wisdom
%doc AUTHORS CO* NEWS README TODO 
%{_bindir}/fftw*-wisdom
%{_bindir}/fftw-wisdom-to-conf
%{_includedir}/fftw3.f
%{_mandir}/man1/fftw-wisdom-to-conf.*
%{_mandir}/man1/fftw*-wisdom.*

%files -n %{libname}
%{_libdir}/libfftw%{api}.so.%{major}*

%files -n %{libname_threads}
%{_libdir}/libfftw%{api}_threads.so.%{major}*

%files -n %{libname_omp}
%{_libdir}/libfftw%{api}_omp.so.%{major}*

%files -n %{libnamef}
%{_libdir}/libfftw%{api}f.so.%{major}*

%files -n %{libnamef_threads}
%{_libdir}/libfftw%{api}f_threads.so.%{major}*

%files -n %{libnamef_omp}
%{_libdir}/libfftw%{api}f_omp.so.%{major}*

%files -n %{libnamel}
%{_libdir}/libfftw%{api}l.so.%{major}*

%files -n %{libnamel_threads}
%{_libdir}/libfftw%{api}l_threads.so.%{major}*

%files -n %{libnamel_omp}
%{_libdir}/libfftw%{api}l_omp.so.%{major}*

%files -n %{devname}
%doc doc/*
%{_includedir}/*fftw*.h
%{_includedir}/fftw3*.f03
%{_infodir}/fftw%{api}.info*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libfftw*.so
%{_libdir}/cmake/fftw3
