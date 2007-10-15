%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Fast fourier transform library
Name:		fftw
Version:	3.1.2
Release:	%mkrel 8
License:	GPL
Group:		System/Libraries
URL:		http://www.fftw.org
Source:		ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.bz2
BuildRequires:	gcc-gfortran
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
Obsoletes:	%{name}

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
Obsoletes:	%{libname}-devel
Provides:	%{name}-devel

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
CONFIGURE_TOP=.. %configure2_5x --enable-shared --enable-threads --enable-fortran --infodir=%{buildroot}%{_infodir}
%make
popd
mkdir build-float
pushd build-float
CONFIGURE_TOP=.. %configure2_5x --enable-float --enable-shared --enable-threads --enable-fortran --infodir=%{buildroot}%{_infodir}
%make
popd

%check
make check -C build-std
make check -C build-float

%install
rm -fr %{buildroot}
pushd build-std
%makeinstall
popd
pushd build-float
%makeinstall
popd

rm -fr %{buildroot}/%{_docdir}/Make*

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

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
