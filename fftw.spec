##%define _disable_ld_no_undefined 1
%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Fast fourier transform library
Name:		fftw
Version:	3.3.1
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.fftw.org
Source:		ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
BuildRequires:	gcc-gfortran
BuildConflicts:	%{develname}

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
%rename	%{name}

%description -n %{libname}
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.

%package -n %{develname}
Summary:	Headers, libraries, & docs for FFTW fast fourier transform library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}%{major}-devel = %{version}-%{release}
Obsoletes:	%{libname}-devel < 3.1.3
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier
transform library.

%prep
%setup -q

%build
export F77="gfortran"
mkdir build-std
pushd build-std
CONFIGURE_TOP=.. %configure2_5x \
		    --enable-shared \
		    --enable-threads \
		    --enable-fortran \
		    %ifarch x86_64
		    --disable-sse \
		    --enable-sse2 \
		    %endif
		    --infodir=%{_infodir}

%make
popd

mkdir build-float
pushd build-float
CONFIGURE_TOP=.. %configure2_5x \
		    --enable-float \
		    --enable-shared \
		    --enable-threads \
		    --enable-fortran \
		    %ifarch x86_64
		    --enable-sse \
		    --enable-sse2 \
		    %endif
		    --infodir=%{_infodir}
%make
popd

# SSE doesn't work with long-double:
mkdir build-long-double
pushd build-long-double
CONFIGURE_TOP=.. %configure2_5x \
		    --enable-long-double \
		    --enable-shared \
		    --enable-threads \
		    --enable-fortran \
		    --infodir=%{_infodir}
%make
popd

%check
# (tpg) export libraries
for i in build-std build-float build-long-double; do
export LD_LIBRARY_PATH=`pwd`/$i/.libs:`pwd`/$i/threads/.libs
make check -C $i; done

%install
rm -fr %{buildroot}
pushd build-std
%makeinstall_std
popd
pushd build-float
%makeinstall_std
popd
pushd build-long-double
%makeinstall_std
popd

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -fr %{buildroot}/%{_docdir}/Make*

%post -n %{develname}
%__install_info -e '* FFTW: (fftw%{major}).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw%{major}.info%{_extension} %{_infodir}/dir 2>/dev/null || :

%preun -n %{develname}
%__install_info -e '* FFTW: (fftw%{major}).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw%{major}.info%{_extension} %{_infodir}/dir --remove 2>/dev/null || :

%files -n %{name}-wisdom
%doc AUTHORS CO* NEWS README TODO 
%{_bindir}/fftw*-wisdom
%{_bindir}/fftw-wisdom-to-conf
%{_includedir}/fftw3.f
%{_mandir}/man1/fftw-wisdom-to-conf.*
%{_mandir}/man1/fftw*-wisdom.*

%files -n %{libname}
%{_libdir}/libfftw*.so.%{major}*

%files -n %{develname}
%{_includedir}/*fftw*.h
%{_includedir}/fftw3.f03
%{_infodir}/fftw%{major}.info*
%doc doc/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libfftw*.a
%{_libdir}/libfftw*.so

