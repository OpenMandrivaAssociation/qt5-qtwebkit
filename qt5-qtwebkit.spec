%define api %(echo %{version} |cut -d. -f1)
%define major %api

%define qtminor %(echo %{version} |cut -d. -f2)
%define qtsubminor %(echo %{version} |cut -d. -f3)
%define beta alpha2

%define major_private 1

%define qtwebkit %mklibname qt%{api}webkit %{major}
%define qtwebkitd %mklibname qt%{api}webkit -d
%define qtwebkit_p_d %mklibname qt%{api}webkit-private -d

%define qtwebkitwidgets %mklibname qt%{api}webkitwidgets %{major}
%define qtwebkitwidgetsd %mklibname qt%{api}webkitwidgets -d
%define qtwebkitwidgets_p_d %mklibname qt%{api}webkitwidgets-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

%define _disable_lto 1

Name:		qt5-qtwebkit
Version:	5.212.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtwebkit-%{version}-%{beta}
# qtwebkit-opensource-src-5.212.0-alpha2.tar.xz
# qtwebkit-5.212.0-alpha2.tar.xz
Source0:	http://download.qt.io/community_releases/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtwebkit-%{version}
Source0:	http://download.qt.io/community_releases/%(echo %{version}|cut -d. -f1-2)/%{version}-final/%{qttarballdir}.tar.xz
%endif
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io

# Upstream patch to fix pagewidth issue with trojita
# https://github.com/annulen/webkit/issues/511
# https://github.com/annulen/webkit/commit/6faf11215e1af27d35e921ae669aa0251a01a1ab
# https://github.com/annulen/webkit/commit/76420459a13d9440b41864c93cb4ebb404bdab55
Patch0:         qt5-qtwebkit-5.212.0-alpha2-fix-pagewidth.patch

# Patch from Kevin Kofler to fix https://github.com/annulen/webkit/issues/573
Patch1:         qtwebkit-5.212.0-alpha2-fix-null-pointer-dereference.patch

# Patch for new CMake policy CMP0071 to explicitly use old behaviour.
Patch2:         qtwebkit-5.212.0_cmake_cmp0071.patch

# Patch to fix for missing source file.
Patch3:         qtwebkit-5.212.0_fix_missing_sources.patch

BuildRequires:	qmake5
BuildRequires:	cmake
BuildRequires:	qt5-macros
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	qt5-qtquick-private-devel
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5OpenGL)
# fix me
#BuildRequires:	pkgconfig(Qt5Declarative)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(leveldb)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5QuickTest)
BuildRequires:	cmake(Qt5Positioning)
BuildRequires:	cmake(Qt5Sensors)
BuildRequires:	cmake(Qt5WebChannel)
BuildRequires:	hyphen-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gperf
BuildRequires:	ruby
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(udev)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	icu-devel

%description
Qt WebKit library is an open source web browser engine.

%files
%{_qt5_prefix}/libexec/QtWebProcess
%{_qt5_prefix}/libexec/QtWebDatabaseProcess
%{_qt5_prefix}/libexec/QtWebNetworkProcess
%{_qt5_libdir}/qml/QtWebKit

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
Requires: qt5-qtbase-devel >= %version

%description -n %{qtwebkitwidgetsd}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitwidgetsd}
%{_qt5_libdir}/libQt5WebKitWidgets.so
%{_qt5_libdir}/libQt5WebKitWidgets.prl
%{_qt5_libdir}/pkgconfig/Qt5WebKitWidgets.pc
%{_includedir}/QtWebKitWidgets
%exclude %{_includedir}/QtWebKitWidgets/%version
%{_prefix}/mkspecs/modules/qt_lib_webkitwidgets.pri
%{_qt5_libdir}/cmake/Qt5WebKitWidgets

#------------------------------------------------------------------------------

%package -n %{qtwebkitwidgets_p_d}
Summary: Devel files needed to build apps based on QtWebKitWidgets
Group:    Development/KDE and Qt
Requires: %{qtwebkitwidgetsd} = %version

%description -n %{qtwebkitwidgets_p_d}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitwidgets_p_d}
%{_qt5_includedir}/QtWebKitWidgets/%version
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
%{_qt5_libdir}/pkgconfig/Qt5WebKit.pc
%{_qt5_libdir}/cmake/Qt5WebKit
%{_includedir}/QtWebKit
%exclude %{_includedir}/QtWebKit/%version
%{_prefix}/mkspecs/modules/qt_lib_webkit.pri

#------------------------------------------------------------------------------

%package -n %{qtwebkit_p_d}
Summary: Devel files needed to build apps based on QtWebKitWidgets
Group:    Development/KDE and Qt
Requires: %{qtwebkitd} = %version
Provides: qt5-qtwebkit-private-devel = %version

%description -n %{qtwebkit_p_d}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkit_p_d}
%{_includedir}/QtWebKit/%version
%{_prefix}/mkspecs/modules/qt_lib_webkit_private.pri

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir
%apply_patches

export LDFLAGS="%{ldflags} -Wl,--as-needed"

%build
%cmake_qt5 \
	-DPORT=Qt \
	-DENABLE_TOOLS=OFF \
	-DCMAKE_BUILD_TYPE=Release \
%ifarch %{arm}
	-DENABLE_JIT=OFF
%endif

%ifarch %{arm}
%make CC=gcc CXX=g++
%else
%make
%endif

#------------------------------------------------------------------------------

%install
%makeinstall_std INSTALL_ROOT=%{buildroot} -C build

# fix pkgconfig files
sed -i '/Name/a Description: Qt5 WebKit module' %{buildroot}%{_libdir}/pkgconfig/Qt5WebKit.pc
sed -i "s,Cflags: -I%{_qt5_libdir}/qt5/../../include/qt5/Qt5WebKit,Cflags: -I%{_qt5_headerdir}/QtWebKit,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKit.pc
sed -i "s,Libs: -L%{_qt5_libdir}/qt5/../ -lQt5WebKit,Libs: -L%{_qt5_libdir} -lQt5WebKit ,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKit.pc

sed -i '/Name/a Description: Qt5 WebKitWidgets module' %{buildroot}%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc
sed -i "s,Cflags: -I%{_qt5_libdir}/qt5/../../include/qt5/Qt5WebKitWidgets,Cflags: -I%{_qt5_headerdir}/QtWebKitWidgets,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc
sed -i "s,Libs: -L%{_qt5_libdir}/qt5/../ -lQt5WebKitWidgets,Libs: -L%{_qt5_libdir} -lQt5WebKitWidgets ,g" %{buildroot}%{_libdir}/pkgconfig/Qt5WebKitWidgets.pc

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a
