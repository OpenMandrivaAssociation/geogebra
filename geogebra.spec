Name:             geogebra
Summary:          Free mathematics software for learning and teaching
Version:          3.2.47.0
Release:          3
Group:            Sciences/Mathematics
Url:              http://www.geogebra.org
License:          GPLv2+ ; CC-BY-SAv3+ ; CC-BY-NC-SAv3+
Source:           geogebra-%{version}.tar.gz  
Source1:          %{name}.desktop
Requires:         java >= 1.5.0
Requires(post):   shared-mime-info
Requires(postun): shared-mime-info
BuildArch:        noarch

%description
This package provides GeoGebra.

GeoGebra is free and multi-platform dynamic mathematics software for all
levels of education that joins geometry, algebra, tables, graphing, statistics
and calculus in one easy-to-use package. It has received several educational
software awards in Europe and the USA.

Quick Facts:

- Graphics, algebra and tables are connected and fully dynamic
- Easy-to-use interface, yet many powerful features 
- Authoring tool to create interactive learning materials as web pages 
- Available in many languages for our millions of users around the world 
- Free and open source software



Authors:
--------
    Markus Hohenwarter (Austria & USA): Project leader since 2001
    Michael Borcherds (UK): Lead Developer since 2007
    Yves Kreis (Luxembourg): Developer since 2005

%prep
%setup -q -n geogebra-%{version}

%build
#

%install
%{__install} -d -m755 %{buildroot}%{_datadir}/%{name}
%{__install} -d -m755 %{buildroot}%{_datadir}/%{name}/unsigned
%{__install} -m644 *.jar %{buildroot}%{_datadir}/%{name}
%{__install} -m644 unsigned/*.jar %{buildroot}%{_datadir}/%{name}/unsigned
%{__install} -d -m755 %{buildroot}%{_datadir}/mime/packages
%{__install} -m644 geogebra.xml %{buildroot}%{_datadir}/mime/packages/%{name}.xml
%{__install} -d -m755 %{buildroot}%{_datadir}/applications
%{__install} -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/
for SIZE in 16x16 22x22 32x32 48x48 64x64 128x128 256x256; do
%{__install} -d -m755 %{buildroot}%{_datadir}/icons/hicolor/$SIZE/apps
%{__install} -d -m755 %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes
%{__install} -m644 icons/hicolor/$SIZE/apps/geogebra.png %{buildroot}%{_datadir}/icons/hicolor/$SIZE/apps
%{__install} -m644 icons/hicolor/$SIZE/mimetypes/application-vnd.geogebra.file.png %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes
%{__install} -m644 icons/hicolor/$SIZE/mimetypes/application-vnd.geogebra.tool.png %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes
done
%{__install} -d -m755 %{buildroot}%{_docdir}/%{name}
%{__install} -m644 license.txt %{buildroot}%{_docdir}/%{name}/COPYING
%{__install} -d -m755 %{buildroot}%{_bindir}

# startscript
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
# simple script to start GeoGebra
func_usage()
{
cat << _USAGE
Usage: %{name} [Java-options] [GeoGebra-options] [FILE]

GeoGebra - Dynamic mathematics software

Java options:
  -Xms<size>                       Set initial Java heap size
  -Xmx<size>                       Set maximum Java heap size

GeoGebra options:
  --help                           Show this help message
  --language=<iso_code>            Set language using locale code, e.g. en, de_AT
  --showAlgebraInput=<boolean>     Show/hide algebra input field
  --showAlgebraWindow=<boolean>    Show/hide algebra window
  --showSpreadsheet=<boolean>      Show/hide spreadsheet
  --fontSize=<number>              Set default font size
  --showSplash=<boolean>           Enable/disable the splash screen
  --enableUndo=<boolean>           Enable/disable Undo
_USAGE
}
# prefer jre-sun, if exists
if [ -z "\$JAVACMD" ]; then
    if [ -e /etc/alternatives/jre_sun/bin/java ]; then
        JAVACMD=/etc/alternatives/jre_sun/bin/java
    else
        JAVACMD=java
    fi
fi
# check for option --help and pass memory options to Java, others to GeoGebra
for i in "\$@"; do
    case "\$i" in
    --help | --hel | --he | --h )
        func_usage; exit 0 ;;
    esac
    if [ \$(expr match "\$i" '.*-Xm') -ne 0 ]; then
        if [ -z "\$JAVA_OPTS" ]; then
            JAVA_OPTS="\$i"
        else
            JAVA_OPTS="\$JAVA_OPTS \$i"
        fi
        shift \$((1))
    else
        if [ \$(expr match "\$i" '.*--') -ne 0 ]; then
            if [ -z "\$GG_OPTS" ]; then
                GG_OPTS="\$i"
            else
                GG_OPTS="\$GG_OPTS \$i"
            fi
            shift \$((1))
        fi
    fi
done
# if memory not set, change to GeoGebra defaults
if [ \$(expr match "\$JAVA_OPTS" '.*-Xmx') -eq 0 ]; then
    JAVA_OPTS="\$JAVA_OPTS -Xmx512m"
fi
if [ \$(expr match "\$JAVA_OPTS" '.*-Xms') -eq 0 ]; then
    JAVA_OPTS="\$JAVA_OPTS -Xms32m"
fi
# run
exec \$JAVACMD \$JAVA_OPTS -jar %{_datadir}/%{name}/geogebra.jar \$GG_OPTS "\$@"
EOF
%{__chmod} 755 %{buildroot}%{_bindir}/%{name}

#%if 0%{?suse_version}
#%suse_update_desktop_file %{name}
#%else
#%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
#desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
#%endif
#%endif

%clean
rm -rf %{buildroot}

%post
%if 0%{?mandriva_version}
%{update_menus}
%update_desktop_database
%update_mime_database
%update_icon_cache hicolor
%else
%{_bindir}/update-mime-database %{_datadir}/mime >/dev/null
%endif

%postun
%if 0%{?mandriva_version}
%{clean_menus}
%clean_desktop_database
%clean_mime_database
%update_icon_cache hicolor
%else
%{_bindir}/update-mime-database %{_datadir}/mime >/dev/null
%endif

%files
%defattr(-,root,root)
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/16x16
%dir %{_datadir}/icons/hicolor/22x22
%dir %{_datadir}/icons/hicolor/32x32
%dir %{_datadir}/icons/hicolor/48x48
%dir %{_datadir}/icons/hicolor/64x64
%dir %{_datadir}/icons/hicolor/128x128
%dir %{_datadir}/icons/hicolor/256x256
%dir %{_datadir}/icons/hicolor/16x16/apps
%dir %{_datadir}/icons/hicolor/16x16/mimetypes
%dir %{_datadir}/icons/hicolor/22x22/apps
%dir %{_datadir}/icons/hicolor/22x22/mimetypes
%dir %{_datadir}/icons/hicolor/32x32/apps
%dir %{_datadir}/icons/hicolor/32x32/mimetypes
%dir %{_datadir}/icons/hicolor/48x48/apps
%dir %{_datadir}/icons/hicolor/48x48/mimetypes
%dir %{_datadir}/icons/hicolor/64x64/apps
%dir %{_datadir}/icons/hicolor/64x64/mimetypes
%dir %{_datadir}/icons/hicolor/128x128/apps
%dir %{_datadir}/icons/hicolor/128x128/mimetypes
%dir %{_datadir}/icons/hicolor/256x256/apps
%dir %{_datadir}/icons/hicolor/256x256/mimetypes
%{_docdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png



%changelog
* Sun Jul 24 2011 Sergey Zhemoitel <serg@mandriva.org> 3.2.47.0-1mdv2012.0
+ Revision: 691470
- fix build
- new version 3.2.47.0

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 2.6a-6mdv2011.0
+ Revision: 618449
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.6a-5mdv2010.0
+ Revision: 429191
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.6a-4mdv2009.0
+ Revision: 245882
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Jan 25 2008 Funda Wang <fwang@mandriva.org> 2.6a-2mdv2008.1
+ Revision: 157781
- fix desktop entry

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 2.6a-1mdv2008.1
+ Revision: 131552
- auto-convert XDG menu entry
- BR java-rpmbuild instead of jdk
- kill re-definition of %%buildroot on Pixel's request
- import geogebra


* Thu May 04 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.6a-1mdk
- initial release
