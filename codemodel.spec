%global pkg_name codemodel
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

Name:         %{?scl_prefix}%{pkg_name}
Version:      2.6
Release:      17.1%{?dist}
Summary:      Java library for code generators
License:      CDDL and GPLv2
URL:          http://codemodel.java.net
# svn export https://svn.java.net/svn/codemodel~svn/tags/codemodel-project-2.6/ codemodel-2.6
# tar -zcvf codemodel-2.6.tar.gz codemodel-2.6
Source0:      %{pkg_name}-%{version}.tar.gz
# Remove the dependency on istack-commons (otherwise it will be a
# recursive dependency with the upcoming changes to that package):
Patch0:       %{pkg_name}-remove-istack-commons-dependency.patch

BuildArch:     noarch

BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix_maven}maven-enforcer-plugin
BuildRequires: %{?scl_prefix_maven}maven-release-plugin
BuildRequires: %{?scl_prefix_maven}mvn(net.java:jvnet-parent:pom:)
BuildRequires: %{?scl_prefix_java_common}mvn(org.apache.ant:ant)
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)

%description
CodeModel is a Java library for code generators; it provides a way to
generate Java programs in a way much nicer than PrintStream.println().
This project is a spin-off from the JAXB RI for its schema compiler
to generate Java source files.

%package javadoc
Summary: Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
# Unpack and patch the original source:
%setup -n %{pkg_name}-%{version} -q
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%patch0 -p1

# Remove bundled jar files:
find . -name '*.jar' -print -delete

%mvn_file :%{pkg_name} %{pkg_name}
%mvn_file :%{pkg_name}-annotation-compiler %{pkg_name}-annotation-compiler
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{!?_licensedir:%global license %%doc}
%license LICENSE.html

%files javadoc -f .mfiles-javadoc
%license LICENSE.html

%changelog
* Tue Jul 14 2015 Michal Srb <msrb@redhat.com> - 2.6-17.1
- SCL-ize spec

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 2.6-16
- introduce license macro

* Tue Jun 24 2014 Michael Simacek <msimacek@redhat.com> - 2.6-15
- Chnage jvnet-parent BR to jvnet-parent:pom

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Michael Simacek <msimacek@redhat.com> - 2.6-13
- Change maven-surefire-provider-junit4 dependency to
  maven-surefire-provider-junit

* Thu Mar 20 2014 Michael Simacek <msimacek@redhat.com> - 2.6-12
- Remove BR java-devel

* Thu Mar 13 2014 Michael Simacek <msimacek@redhat.com> - 2.6-11
- Drop manual requires

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 2.6-10
- rebuilt FTBFS in rawhide
- swith to Xmvn
- adapt to new guideline

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-6
- Add maven-enforcer-plugin as build time dependeny

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-4
- Restore the dependency on jvnet-parent
- Remove the dependency on istack-commons

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-3
- Added build requirement for maven-surefire-provider-junit4

* Tue Feb 14 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6-2
- Cleanup of the spec file

* Mon Jan 16 2012 Marek Goldmann <mgoldman@redhat.com> 2.6-1
- Initial packaging
