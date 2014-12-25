%define api 5
%define major %api

%define qtminor 4
%define qtsubminor 0

%define major_private 1
%define qtversion %{major}.%{qtminor}.%{qtsubminor}

%define qtwebkit %mklibname qt%{api}webkit %{major}
%define qtwebkitd %mklibname qt%{api}webkit -d
%define qtwebkit_p_d %mklibname qt%{api}webkit-private -d

%define qtwebkitwidgets %mklibname qt%{api}webkitwidgets %{major}
%define qtwebkitwidgetsd %mklibname qt%{api}webkitwidgets -d
%define qtwebkitwidgets_p_d %mklibname qt%{api}webkitwidgets-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

%define qttarballdir qtwebkit-opensource-src-%{qtversion}

Name:		qt5-qtwebkit
Version:	%{qtversion}
Release:	1
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt-project.org
Source0:	http://download.qt-project.org/official_releases/qt/%{major}.%{qtminor}/%{version}/submodules/%{qttarballdir}.tar.xz
Patch0:		0001-Add-ARM-64-support.patch
BuildRequires:	qt5-qtbase-devel = %{version}
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gperf
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(udev)
# fix me
#BuildRequires:	pkgconfig(Qt5Declarative) = %{version}
BuildRequires:	pkgconfig(Qt5Widgets)  = %{version}
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(Qt5Quick) = %{version}
BuildRequires:	pkgconfig(Qt5Qml) = %{version}
BuildRequires:	icu-devel

%description
Qt WebKit library is an open source web browser engine.

%files
%{_qt5_prefix}/libexec/QtWebPluginProcess
%{_qt5_prefix}/libexec/QtWebProcess

#------------------------------------------------------------------------------

%package -n %{qtwebkitwidgets}
Summary: Qt%{major} Lib
Group: System/Libraries

%description -n %{qtwebkitwidgets}
Qt%{major} Lib.

%files -n %{qtwebkitwidgets}
%{_qt5_libdir}/libQt5WebKitWidgets.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{qtwebkitwidgetsd}
Summary: Devel files needed to build apps based on QtWebKitWidgets
Group:    Development/KDE and Qt
Requires: %{qtwebkitwidgets} = %version
Requires: qt5-qtbase-devel = %version

%description -n %{qtwebkitwidgetsd}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitwidgetsd}
%{_qt5_libdir}/libQt5WebKitWidgets.so
%{_qt5_libdir}/libQt5WebKitWidgets.prl
%{_qt5_libdir}/pkgconfig/Qt5WebKitWidgets.pc
%{_qt5_includedir}/QtWebKitWidgets
%exclude %{_qt5_includedir}/QtWebKitWidgets/%qtversion
%{_qt5_prefix}/mkspecs/modules/qt_lib_webkitwidgets.pri
%{_qt5_libdir}/cmake/Qt5WebKitWidgets

#------------------------------------------------------------------------------

%package -n %{qtwebkitwidgets_p_d}
Summary: Devel files needed to build apps based on QtWebKitWidgets
Group:    Development/KDE and Qt
Requires: %{qtwebkitwidgetsd} = %version

%description -n %{qtwebkitwidgets_p_d}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitwidgets_p_d}
%{_qt5_includedir}/QtWebKitWidgets/%qtversion
%{_qt5_prefix}/mkspecs/modules/qt_lib_webkitwidgets_private.pri

#------------------------------------------------------------------------------

%package -n %{qtwebkit}
Summary: Qt%{major} Lib
Group: System/Libraries

%description -n %{qtwebkit}
Qt%{major} Lib.

%files -n %{qtwebkit}
%{_qt5_libdir}/libQt5WebKit.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{qtwebkitd}
Summary: Devel files needed to build apps based on QtWebKitWidgets
Group:    Development/KDE and Qt
Requires: %{qtwebkit} = %version

%description -n %{qtwebkitd}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitd}
%{_qt5_libdir}/libQt5WebKit.so
%{_qt5_libdir}/libQt5WebKit.prl
%{_qt5_libdir}/pkgconfig/Qt5WebKit.pc
%{_qt5_includedir}/QtWebKit
%exclude %{_qt5_includedir}/QtWebKit/%qtversion
%{_qt5_prefix}/mkspecs/modules/qt_lib_webkit.pri
%{_qt5_libdir}/cmake/Qt5WebKit

#------------------------------------------------------------------------------

%package -n %{qtwebkit_p_d}
Summary: Devel files needed to build apps based on QtWebKitWidgets
Group:    Development/KDE and Qt
Requires: %{qtwebkitd} = %version
Provides: qt5-qtwebkit-private-devel = %version

%description -n %{qtwebkit_p_d}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkit_p_d}
%{_qt5_includedir}/QtWebKit/%qtversion
%{_qt5_prefix}/mkspecs/modules/qt_lib_webkit_private.pri

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir
%apply_patches

# Build scripts aren't ready for python3
grep -rl "env python" . |xargs sed -i -e "s,env python,env python2,g"
grep -rl "/python$" . |xargs sed -i -e "s,/python$,/python2,g"
grep -rl "'python'" . |xargs sed -i -e "s,'python','python2',g"
sed -i -e "s,python,python2,g" Source/*/DerivedSources.pri

%build
%qmake_qt5 \
%ifarch aarch64
	DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0
%endif

%make

#------------------------------------------------------------------------------

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a
