##%define _disable_ld_no_undefined 1

%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Fast fourier transform library
Name:		fftw
Version:	3.3
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.fftw.org
Source:		ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
BuildRequires:	gcc-gfortran
BuildConflicts:	%{develname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Provides:	%{name}
Obsoletes:	%{name} < 3.1.3

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

rm -fr %{buildroot}/%{_docdir}/Make*

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post -n %{develname}
%__install_info -e '* FFTW: (fftw%{major}).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw%{major}.info%{_extension} %{_infodir}/dir

%preun -n %{develname}
%__install_info -e '* FFTW: (fftw%{major}).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw%{major}.info%{_extension} %{_infodir}/dir --remove

%files -n %{name}-wisdom
%defattr (-,root,root)
%{_bindir}/fftw*-wisdom
%{_bindir}/fftw-wisdom-to-conf
%{_includedir}/fftw3.f
%{_mandir}/man1/fftw-wisdom-to-conf.*
%{_mandir}/man1/fftw*-wisdom.*

%files -n %{libname}
%defattr (-,root,root)
%doc AUTHORS CO* NEWS README TODO 
%{_libdir}/libfftw*.so.%{major}*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/*fftw*.h
%{_infodir}/fftw%{major}.info*
%doc doc/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libfftw*.a
%{_libdir}/libfftw*.la
%{_libdir}/libfftw*.so
