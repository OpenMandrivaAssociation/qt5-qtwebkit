%define api %(echo %{version} |cut -d. -f1)
%define major %api

%define qtminor %(echo %{version} |cut -d. -f2)
%define qtsubminor %(echo %{version} |cut -d. -f3)
%define beta %nil

%define major_private 1

%define qtwebkit %mklibname qt%{api}webkit %{major}
%define qtwebkitd %mklibname qt%{api}webkit -d
%define qtwebkit_p_d %mklibname qt%{api}webkit-private -d

%define qtwebkitwidgets %mklibname qt%{api}webkitwidgets %{major}
%define qtwebkitwidgetsd %mklibname qt%{api}webkitwidgets -d
%define qtwebkitwidgets_p_d %mklibname qt%{api}webkitwidgets-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

%define _disable_lto 1
# ARMv7
%define _disable_neon 1

Name:		qt5-qtwebkit
Version:	5.6.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtwebkit-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtwebkit-opensource-src-%{version}
# 5.6.0 is not officially part of the release so get from snapshots (fedora)
Source0:	http://download.qt.io/snapshots/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/latest_src/submodules/%{qttarballdir}.tar.xz
%endif
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
Patch0:		0001-Add-ARM-64-support.patch
Patch1:		qtwebkit-5.4.2-system-leveldb.patch
Patch2:		qtwebkit-opensource-src-5.0.1-debuginfo.patch
# (tpg) -reduce-memory-overheads is ld.gold specific so remove it from below patch
Patch3:		qtwebkit-opensource-src-5.2.0-save_memory.patch
Patch4:		03_hide_std_symbols.diff
#Patch5:		link-qtcore.patch
# Still kept in the repository so we can re-enable it when we re-enable LTO
#Patch6:		qtwebkit-5.5.1-lto.patch
Patch7:		qtwebkit-opensource-src-5.2.1-no_rpath.patch
# WebKit use libpthread directly but is depending on other qt modules
# causing it to be linked against, which might break unless -lpthread
# is last.
Patch8:		0004-Fix-linking-with-libpthread.patch
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core) >= %{version}
BuildRequires:	pkgconfig(Qt5Gui) >= %{version}
BuildRequires:	pkgconfig(Qt5Network) >= %{version}
BuildRequires:	pkgconfig(Qt5Sql) >= %{version}
BuildRequires:	pkgconfig(Qt5Quick) >= %{version}
BuildRequires:	qt5-qtquick-private-devel >= %{version}
BuildRequires:	pkgconfig(Qt5Qml) >= %{version}
BuildRequires:	pkgconfig(Qt5OpenGL) >= %{version}
# fix me
#BuildRequires:	pkgconfig(Qt5Declarative) >= %{version}
BuildRequires:	pkgconfig(Qt5Widgets) >= %{version}
BuildRequires:	pkgconfig(Qt5PrintSupport) >= %{version}
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-app-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(leveldb)
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
%{_qt5_prefix}/libexec/QtWebPluginProcess
%{_qt5_prefix}/libexec/QtWebProcess
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
Requires: qt5-qtbase-devel >= %version

%description -n %{qtwebkitwidgetsd}
Devel files needed to build apps based on QtWebKitWidgets.

%files -n %{qtwebkitwidgetsd}
%{_qt5_libdir}/libQt5WebKitWidgets.so
%{_qt5_libdir}/libQt5WebKitWidgets.prl
%{_qt5_libdir}/pkgconfig/Qt5WebKitWidgets.pc
%{_qt5_includedir}/QtWebKitWidgets
%exclude %{_qt5_includedir}/QtWebKitWidgets/%version
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
%{_qt5_libdir}/libQt5WebKit.prl
%{_qt5_libdir}/pkgconfig/Qt5WebKit.pc
%{_qt5_includedir}/QtWebKit
%exclude %{_qt5_includedir}/QtWebKit/%version
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
%{_qt5_includedir}/QtWebKit/%version
%{_qt5_prefix}/mkspecs/modules/qt_lib_webkit_private.pri

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir
%apply_patches

export LDFLAGS="%{ldflags} -Wl,--as-needed"

# disable it when building without LLVM/clang
grep -rl "cruT" * | xargs sed -i 's/cruT/cru/g'

# Build scripts aren't ready for python3
grep -rl "env python" . |xargs sed -i -e "s,env python,env python2,g"
grep -rl "/python$" . |xargs sed -i -e "s,/python$,/python2,g"
grep -rl "'python'" . |xargs sed -i -e "s,'python','python2',g"
sed -i -e "s,python,python2,g" Source/*/DerivedSources.pri

# https://bugs.gentoo.org/show_bug.cgi?id=466216
sed -i -e '/CONFIG +=/s/rpath//' \
	Source/WebKit/qt/declarative/{experimental/experimental,public}.pri \
	Tools/qmake/mkspecs/features/{force_static_libs_as_shared,unix/default_post}.prf

# ensure bundled library cannot be used
rm -r Source/ThirdParty/leveldb

# remove rpath
find ./ -type f -name \*.pr\* | \
while read f; do
    sed -i 's|\(^CONFIG[[:space:]][[:space:]]*+=[[:space:]].*\)rpath|\1|' $f
    sed -i 's|\([[:space:]]CONFIG[[:space:]][[:space:]]*+=[[:space:]].*\)rpath|\1|' $f
done

# Fix up headers...
[ -d include ] || %{_libdir}/qt5/bin/syncqt.pl -version %{version} Source/sync.profile

%build
%qmake_qt5 \
%ifarch %{armx}
	DEFINES+=ENABLE_JIT=0 DEFINES+=ENABLE_YARR_JIT=0 DEFINES+=ENABLE_ASSEMBLER=0
%endif

%ifarch %{arm}
%make CC=gcc CXX=g++
%else
%make
%endif

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
