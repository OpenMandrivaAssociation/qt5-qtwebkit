%define api %(echo %{version} |cut -d. -f1)
%define major %api

%define qtminor %(echo %{version} |cut -d. -f2)
%define qtsubminor %(echo %{version} |cut -d. -f3)
%define beta %{nil}

%define major_private 1

%define qtwebkit %mklibname qt%{api}webkit %{major}
%define qtwebkitd %mklibname qt%{api}webkit -d
%define qtwebkit_p_d %mklibname qt%{api}webkit-private -d

%define qtwebkitwidgets %mklibname qt%{api}webkitwidgets %{major}
%define qtwebkitwidgetsd %mklibname qt%{api}webkitwidgets -d
%define qtwebkitwidgets_p_d %mklibname qt%{api}webkitwidgets-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

%define _disable_lto 1

# FIXME workaround for a dependency generator bug
%global __requires_exclude ^.*_dep.*$

Name:		qt5-qtwebkit
Version:	5.212.20200910
# Upstream sources live at https://github.com/qtwebkit/qtwebkit
# https://code.qt.io/qt/qtwebkit.git is a stripped down copy
# with just what is needed to build it.
# Unfortunately, as of 2020/09/09 the latter repository has been out
# of sync for 5 months, so we have to use the former.
# 
# Tarball is built from the latter repository using
# git archive -o qtwebkit-5.212.20200910.tar --prefix qtwebkit-5.212.20200910/ origin/5.212
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtwebkit-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/community_releases/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/%{qttarballdir}.tar.zst
%else
Release:	3
%define qttarballdir qtwebkit-opensource-src-%{version}
Source0:	qtwebkit-%{version}.tar.zst
%endif
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
Patch0:		0001-Add-ARM-64-support.patch
# Still kept in the repository so we can re-enable it when we re-enable LTO
#Patch6:		qtwebkit-5.5.1-lto.patch
Patch8:		qtwebkit-5.9.1-armv7-assembly.patch
Patch9:		qtwebkit-5.212-icu-true.patch
Patch10:		https://src.fedoraproject.org/rpms/qt5-qtwebkit/raw/rawhide/f/qt5-qtwebkit-glib-2.68.patch
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core) >= 5.15
BuildRequires:	pkgconfig(Qt5Gui) >= 5.15
BuildRequires:	pkgconfig(Qt5Network) >= 5.15
BuildRequires:	pkgconfig(Qt5Multimedia) >= 5.15
BuildRequires:	pkgconfig(Qt5Sql) >= 5.15
BuildRequires:	pkgconfig(Qt5Test) >= 5.15
BuildRequires:	pkgconfig(Qt5Quick) >= 5.15
BuildRequires:	pkgconfig(Qt5QuickTest) >= 5.15
BuildRequires:	pkgconfig(Qt5Positioning) >= 5.15
BuildRequires:	cmake(Qt5XcbQpa)
BuildRequires:	qt5-qtquick-private-devel >= 5.15
BuildRequires:	woff2-devel
BuildRequires:	pkgconfig(Qt5OpenGL) >= 5.15
BuildRequires:	pkgconfig(Qt5Qml) >= 5.15
BuildRequires:	pkgconfig(Qt5Sensors) >= 5.15
BuildRequires:	pkgconfig(Qt5WebChannel) >= 5.15
BuildRequires:	pkgconfig(Qt5Widgets) >= 5.15
BuildRequires:	pkgconfig(Qt5PrintSupport) >= 5.15
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(gstreamer-mpegts-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
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
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(xcb-renderutil)
BuildRequires:	pkgconfig(xcb-ewmh)
BuildRequires:	pkgconfig(xcb-cursor)
BuildRequires:	pkgconfig(xcb-image)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xcb-errors)

BuildRequires:	icu-devel
BuildRequires:	python2
BuildRequires:	pkgconfig(ruby)

%description
Qt WebKit library is an open source web browser engine.

%files
%{_qt5_prefix}/libexec/QtWebProcess
%optional %{_qt5_prefix}/libexec/QtWebPluginProcess
%{_qt5_prefix}/libexec/QtWebStorageProcess
%{_qt5_prefix}/libexec/QtWebNetworkProcess
%{_qt5_prefix}/qml/QtWebKit

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
Requires: qt5-qtbase-devel >= 5.13

%description -n %{qtwebkitwidgetsd}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitwidgetsd}
%{_qt5_libdir}/libQt5WebKitWidgets.so
%{_qt5_libdir}/pkgconfig/Qt5WebKitWidgets.pc
%{_qt5_includedir}/QtWebKitWidgets
%exclude %{_qt5_includedir}/QtWebKitWidgets/%(echo %version |cut -d. -f1-2).0
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
%{_qt5_includedir}/QtWebKitWidgets/%(echo %version |cut -d. -f1-2).0
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
%{_qt5_includedir}/QtWebKit
%exclude %{_qt5_includedir}/QtWebKit/%(echo %version |cut -d. -f1-2).0
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
%{_qt5_includedir}/QtWebKit/%(echo %version |cut -d. -f1-2).0
%{_qt5_prefix}/mkspecs/modules/qt_lib_webkit_private.pri

#------------------------------------------------------------------------------

%prep
%autosetup -p1 -n qtwebkit-%{version}

%build
%qmake_qt5 \
	-spec linux-clang \
%ifarch %{armx}
	DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0 DEFINES+=ENABLE_ASSEMBLER=0
%endif

%make_build

#------------------------------------------------------------------------------

%install
%make_install INSTALL_ROOT=%{buildroot}
