Name:		qmmp-plugins-freeworld
Version:	0.9.6
Release:	1%{?dist}
Summary:	Plugins for qmmp (Qt-based multimedia player)

Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://qmmp.ylsoftware.com/
Source:		http://qmmp.ylsoftware.com/files/qmmp-%{version}.tar.bz2
Source2:	qmmp-filter-provides.sh
%define		_use_internal_dependency_generator 0
%define		__find_provides %{_builddir}/%{buildsubdir}/qmmp-filter-provides.sh

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	ffmpeg-devel
BuildRequires:	enca-devel
BuildRequires:	faad2-devel
BuildRequires:	libmad-devel qt-devel >= 4.3
BuildRequires:	libmms-devel
BuildRequires:	taglib-devel libcurl-devel
Requires:	qmmp%{?_isa} = %{version}

%description
Qmmp is an audio-player, written with help of Qt library.
This package contains plugins needed to play AAC, MPEG (.mp3) and WMA files,
and also the mplayer plugin for video playback.


%prep
%setup -q -n qmmp-%{version}
cp %{SOURCE2} .
chmod +x qmmp-filter-provides.sh
# adjust includes for the header move in latest ffmpeg
sed -i \
	-e 's|<avcodec.h|<libavcodec/avcodec.h|g' \
	-e 's|g/avcodec.h|g/libavcodec/avcodec.h|g' \
	-e 's|<avformat.h|<libavformat/avformat.h|g' \
	-e 's|g/avformat.h|g/libavformat/avformat.h|g' \
	src/plugins/Input/ffmpeg/decoder_ffmpeg.h \
	src/plugins/Input/ffmpeg/decoderffmpegfactory.cpp


%build
# the plugin groups, as separated by newlines, are:
# Transport, Input, Output, Effect, Visual, General, File Dialogs
%cmake \
	-D USE_CURL:BOOL=FALSE \
\
	-D USE_FLAC:BOOL=FALSE \
	-D USE_VORBIS:BOOL=FALSE \
	-D USE_MPC:BOOL=FALSE \
	-D USE_MODPLUG:BOOL=FALSE \
	-D USE_SNDFILE:BOOL=FALSE \
	-D USE_WAVPACK:BOOL=FALSE \
	-D USE_CUE:BOOL=FALSE \
	-D USE_CDA:BOOL=FALSE \
	-D USE_MIDI:BOOL=FALSE \
	-D USE_GME:BOOL=FALSE \
\
	-D USE_ALSA:BOOL=FALSE \
	-D USE_JACK:BOOL=FALSE \
	-D USE_OSS:BOOL=FALSE \
	-D USE_OSS4:BOOL=FALSE \
	-D USE_PULSE:BOOL=FALSE \
	-D USE_NULL:BOOL=FALSE \
	-D USE_WAVEOUT:BOOL=FALSE \
\
	-D USE_SRC:BOOL=FALSE \
	-D USE_BS2B:BOOL=FALSE \
	-D USE_LADSPA:BOOL=FALSE \
	-D USE_CROSSFADE:BOOL=FALSE \
	-D USE_STEREO:BOOL=FALSE \
\
	-D USE_ANALYZER:BOOL=FALSE \
	-D USE_PROJECTM:BOOL=FALSE \
\
	-D USE_MPRIS:BOOL=FALSE \
	-D USE_SCROBBLER:BOOL=FALSE \
	-D USE_STATICON:BOOL=FALSE \
	-D USE_NOTIFIER:BOOL=FALSE \
	-D USE_LYRICS:BOOL=FALSE \
	-D USE_HAL:BOOL=FALSE \
	-D USE_UDISKS:BOOL=FALSE \
	-D USE_HOTKEY:BOOL=FALSE \
	-D USE_FILEOPS:BOOL=FALSE \
	-D USE_COVER:BOOL=FALSE \
	-D USE_KDENOTIFY:BOOL=FALSE \
\
	-D USE_QMMP_DIALOG:BOOL=FALSE \
\
	-D CMAKE_INSTALL_PREFIX=/usr \
	-D LIB_DIR=%{_lib} \
	./

make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Engines/mplayer
make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Input/aac
make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Input/ffmpeg
make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Input/mad
make VERBOSE=1 %{?_smp_mflags} -C src/plugins/Transports/mms


%install
make DESTDIR=%{buildroot} install -C src/plugins/Engines/mplayer
make DESTDIR=%{buildroot} install -C src/plugins/Input/aac
make DESTDIR=%{buildroot} install -C src/plugins/Input/ffmpeg
make DESTDIR=%{buildroot} install -C src/plugins/Input/mad
make DESTDIR=%{buildroot} install -C src/plugins/Transports/mms
## install .desktop files for MimeType associations
mkdir -p %{buildroot}/%{_datadir}/applications/
# aac
sed -e "/MimeType/c\MimeType=audio/aac;audio/aacp;" -e "/Actions/,$ c\NoDisplay=true" \
    src/app/qmmp.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-aac.desktop
sed -e "/MimeType/c\MimeType=audio/aac;audio/aacp;" \
    src/app/qmmp_enqueue.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-aac_enqueue.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-aac.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-aac_enqueue.desktop
# ffmpeg
sed -e "/MimeType/c\MimeType=audio/aac;audio/aacp;audio/x-ms-wma;audio/mpeg;audio/x-ffmpeg-shorten;audio/3gpp;audio/3gpp2;audio/mp4;audio/MP4A-LATM;audio/mpeg4-generic;audio/m4a;audio/ac3;audio/eac3;audio/dts;audio/true-hd;audio/x-matroska;" \
    -e "/Actions/,$ c\NoDisplay=true" \
    src/app/qmmp.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-ffmpeg.desktop
sed -e "/MimeType/c\MimeType=audio/aac;audio/aacp;audio/x-ms-wma;audio/mpeg;audio/x-ffmpeg-shorten;audio/3gpp;audio/3gpp2;audio/mp4;audio/MP4A-LATM;audio/mpeg4-generic;audio/m4a;audio/ac3;audio/eac3;audio/dts;audio/true-hd;audio/x-matroska;" \
    src/app/qmmp_enqueue.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-ffmpeg_enqueue.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-ffmpeg.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-ffmpeg_enqueue.desktop
# mad
sed -e "/MimeType/c\MimeType=audio/mp3;audio/mpeg;" -e "/Actions/,$ c\NoDisplay=true" \
    src/app/qmmp.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-mad.desktop
sed -e "/MimeType/c\MimeType=audio/mp3;audio/mpeg;" \
    src/app/qmmp_enqueue.desktop \
    > %{buildroot}/%{_datadir}/applications/%{name}-mad_enqueue.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-mad.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-mad_enqueue.desktop


%files
# there's only mplayer plugin now, so own the directory
%dir %{_libdir}/qmmp/Engines
%{_libdir}/qmmp/Engines/*.so
# Input & Transports dirs are owned by qmmp already
%{_libdir}/qmmp/Input/*.so
%{_libdir}/qmmp/Transports/*.so
%{_datadir}/applications/%{name}-aac.desktop
%{_datadir}/applications/%{name}-aac_enqueue.desktop
%{_datadir}/applications/%{name}-ffmpeg.desktop
%{_datadir}/applications/%{name}-ffmpeg_enqueue.desktop
%{_datadir}/applications/%{name}-mad.desktop
%{_datadir}/applications/%{name}-mad_enqueue.desktop


%post
/sbin/ldconfig
%{_bindir}/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
 
%postun
/sbin/ldconfig
/sbin/ldconfig
%{_bindir}/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%changelog
* Tue Jan 12 2016 Karel Volný <kvolny@redhat.com> 0.9.6-1
- version bump
- updated provides filtering
- add separate .desktop file for each plugin for MimeType associations
- spec cleanups as per newer guidelines
 - removed BuildRoot definition
 - no longer remove buildroot, dropped clean section
 - removed defattr

* Mon Jan 04 2016 Karel Volný <kvolny@redhat.com> 0.9.5-1
- version bump

* Mon Jun 29 2015 Karel Volný <kvolny@redhat.com> 0.8.3-1
- version bump

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.7.7-4
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.7-3
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.7.7-2
- Rebuilt for ffmpeg-2.3

* Thu Jun 12 2014 Karel Volný <kvolny@redhat.com> 0.7.7-1
- version bump

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 0.7.4-2
- Rebuilt for ffmpeg-2.2

* Wed Dec 11 2013 Karel Volný <kvolny@redhat.com> 0.7.4-1
- version bump

* Wed Dec 11 2013 Karel Volný <kvolny@redhat.com> 0.7.3-1
- version bump

* Wed Oct 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-2
- Rebuilt

* Wed Aug 28 2013 Karel Volný <kvolny@redhat.com> 0.7.2-1
- version bump

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.1-2
- Rebuilt for FFmpeg 2.0.x

* Fri Jun 21 2013 Karel Volný <kvolny@redhat.com> 0.7.1-1
- version bump

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-2
- Rebuilt for x264/FFmpeg

* Thu May 02 2013 Karel Volný <kvolny@redhat.com> 0.7.0-1
- version bump
- project URLs changed

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.6.8-2
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Apr 02 2013 Karel Volný <kvolny@redhat.com> 0.6.8-1
- version bump

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.6.6-2
- Rebuilt for ffmpeg

* Tue Jan 29 2013 Karel Volný <kvolny@redhat.com> 0.6.6-1
- version bump

* Tue Dec 11 2012 Karel Volný <kvolny@redhat.com> 0.6.5-1
- version bump

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.6.4-2
- Rebuilt for FFmpeg 1.0

* Tue Nov 06 2012 Karel Volný <kvolny@redhat.com> 0.6.4-1
- version bump

* Mon Jul 30 2012 Karel Volný <kvolny@redhat.com> 0.6.3-1
- version bump

* Mon Jul 30 2012 Karel Volný <kvolny@redhat.com> 0.6.2-1
- version bump

* Mon Jul 30 2012 Karel Volný <kvolny@redhat.com> 0.6.1-1
- version bump

* Tue Jul 03 2012 Karel Volný <kvolny@redhat.com> 0.6.0-1
- version bump

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.6-2
- Rebuilt for FFmpeg

* Mon Jun 18 2012 Karel Volný <kvolny@redhat.com> 0.5.6-1
- version bump
- adds support for ffmpeg-0.11

* Fri Jun 08 2012 Karel Volný <kvolny@redhat.com> 0.5.5-1
- version bump

* Fri Mar 02 2012 Karel Volný <kvolny@redhat.com> 0.5.4-1
- version bump
- removed patch to include usleep from QThread (qmmp-0.5.3-mms-include-usleep.patch)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.3-3
- Rebuilt for c++ ABI breakage

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.3-2
- Rebuilt for x264/FFmpeg

* Mon Jan 23 2012 Karel Volný <kvolny@redhat.com> 0.5.3-1
- version bump
- patch to include usleep from QThread (qmmp-0.5.3-mms-include-usleep.patch)

* Wed Nov 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-3
- Rebuilt for libcdio

* Thu Sep 08 2011 Karel Volný <kvolny@redhat.com> 0.5.1-2
- rebuild for new ffmpeg

* Fri Jun 24 2011 Karel Volný <kvolny@redhat.com> 0.5.1-1
- version bump

* Wed Dec 15 2010 Karel Volný <kvolny@redhat.com> 0.4.3-1
- version bump

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.2-2
- Rebuilt for gcc bug

* Thu Sep 16 2010 Karel Volný <kvolny@redhat.com> 0.4.2-1
- version bump
- fixes possible freezes with mplayer plugin

* Fri Jul 02 2010 Karel Volný <kvolny@redhat.com> 0.4.1-1
- version bump
- fixes in flv playback and mplayer support

* Tue Jun 15 2010 Karel Volný <kvolny@redhat.com> 0.4.0-1
- version bump
- new MMS transport plugin
- BuildRequires libmms-devel for MMS support
- BuildRequires enca-devel for encoding detection

* Tue Apr 20 2010 Karel Volný <kvolny@redhat.com> 0.3.4-1
- version bump

* Thu Jan 14 2010 Karel Volný <kvolny@redhat.com> 0.3.2-1
- version bump

* Fri Dec 04 2009 Karel Volný <kvolny@redhat.com> 0.3.1-2
- add %%{?_isa} to require architecture match (wrt Fedora bug #543963)

* Thu Nov 05 2009 Karel Volný <kvolny@redhat.com> 0.3.1-1
- version bump

* Tue Aug 25 2009 Karel Volný <kvolny@redhat.com> 0.3.0-1
- version bump
- new plugins aac and mplayer
- BuildRequires faad2-devel for AAC support

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2.3-3
- rebuild for new F11 features

* Sat Dec 20 2008 Dominik Mierzejewski <rpm@greysector.net> 0.2.3-2
- rebuild against new ffmpeg

* Mon Dec 08 2008 Karel Volny <kvolny@redhat.com> 0.2.3-1
- version bump

* Fri Sep 05 2008 Karel Volny <kvolny@redhat.com> 0.2.2-1
- version bump

* Wed Aug 20 2008 Karel Volny <kvolny@redhat.com> 0.2.0-4
- adjusted includes for the header move in latest ffmpeg
- upgraded ffmpeg-devel dependency

* Fri Aug 08 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2.0-3
- rebuild

* Mon Aug 04 2008 Karel Volny <kvolny@redhat.com> 0.2.0-2
- added BuildRequires: libcurl-devel

* Thu Jul 31 2008 Karel Volny <kvolny@redhat.com> 0.2.0-1
- version bump

* Tue May 13 2008 Karel Volny <kvolny@redhat.com> 0.1.6-1
- version bump

* Sat Mar 15 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 0.1.5-3
- rebuild for new ffmpeg

* Mon Jan 21 2008 Karel Volny <kvolny@redhat.com> 0.1.5-2
- fixed permissions issue for the helper sript qmmp-filter-provides.sh

* Mon Jan 14 2008 Karel Volny <kvolny@redhat.com> 0.1.5-1
- package renamed to match conventions (from "qmmp-plugins")
- added "BuildRequires: qmmp = %%{version}"

* Mon Dec 10 2007 Karel Volny <kvolny@redhat.com> 0.1.5-1
- version bump
- simplified setting of the libraries destination

* Wed Sep 12 2007 Karel Volny <kvolny@redhat.com> 0.1.4-2
- specfile improvements (Fedora bug #280751 comment #4)

* Tue Sep 11 2007 Karel Volny <kvolny@redhat.com> 0.1.4-1
- initial release of separate plugins, as suggested in comment #1 to (Livna) bug #1631
