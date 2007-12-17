%define	name	geogebra
%define	version	2.6a
%define	release	%mkrel 1
%define	Summary	Interactive software for dynamical mathematics

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
Group:		Sciences/Mathematics
URL:		http://www.geogebra.at/
Source0:	geogebra_setup.jar
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
License:	GPL
BuildRequires:	java-rpmbuild ImageMagick
BuildArch:	noarch

%description
GeoGebra is a dynamic mathematics software for education in
secondary schools that joins geometry, algebra and calculus.
It received several international awards including the European
and German educational software awards.

%prep
jar -x < %{SOURCE0}
#/usr/src/RPM/SOURCES/geogebra_setup.jar

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}
#mkdir -p %{buildroot}/usr/lib

cd D_/deploy/source
cp -a * %{buildroot}/usr/share/%{name}/

mkdir -p %{buildroot}%{_bindir}
cat << EOF > %{buildroot}%{_bindir}/%{name}
#!/bin/sh
java -jar %{_datadir}/%{name}/%{name}.jar \$@
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}):command="%{name}" \
		icon=%{name}.png \
		needs="x11" \
		section="More Applications/Sciences/Mathematics" \
		title="GeoGebra"\
		longtitle="%{Summary}"
EOF

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
convert ../geogebra16.gif -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert ../geogebra32.gif -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert ../geogebra32.gif -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_menudir}/%{name}

