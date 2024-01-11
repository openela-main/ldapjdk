################################################################################
Name:             ldapjdk
################################################################################

Summary:          LDAP SDK
URL:              http://www.dogtagpki.org/
License:          MPLv1.1 or GPLv2+ or LGPLv2+

BuildArch:        noarch

# For development (i.e. unsupported) releases, use x.y.z-0.n.<phase>.
# For official (i.e. supported) releases, use x.y.z-r where r >=1.
Version:          4.23.0
Release:          1%{?_timestamp}%{?_commit_id}%{?dist}
#global           _phase -alpha1

%global spname		ldapsp
%global filtname	ldapfilt
%global beansname	ldapbeans

# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix ldap-sdk-<version>/ \
#     -o ldap-sdk-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/ldap-sdk/archive/v%{version}%{?_phase}/ldap-sdk-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > ldap-sdk-VERSION-RELEASE.patch
# Patch: ldap-sdk-VERSION-RELEASE.patch

################################################################################
# Java
################################################################################

%if 0%{?fedora} && 0%{?fedora} <= 32 || 0%{?rhel} && 0%{?rhel} <= 8
%define java_devel java-1.8.0-openjdk-devel
%define java_headless java-1.8.0-openjdk-headless
%define java_home /usr/lib/jvm/java-1.8.0-openjdk
%else
%define java_devel java-11-openjdk-devel
%define java_headless java-11-openjdk-headless
%define java_home /usr/lib/jvm/java-11-openjdk
%endif

################################################################################
# Build Dependencies
################################################################################

BuildRequires:    ant
BuildRequires:    %{java_devel}
BuildRequires:    javapackages-local
BuildRequires:    slf4j
BuildRequires:    slf4j-jdk14
BuildRequires:    jss >= 4.9.0, jss < 5.0.0

################################################################################
# Runtime Dependencies
################################################################################

Requires:         %{java_headless}
Requires:         jpackage-utils >= 0:1.5
Requires:         slf4j
Requires:         slf4j-jdk14
Requires:         jss >= 4.9.0, jss < 5.0.0

%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%license docs/ldapjdk/license.txt

################################################################################
%package javadoc
################################################################################

Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}

################################################################################
%prep
################################################################################

%autosetup -n ldap-sdk-%{version}%{?_phase} -p 1

# Remove all bundled jars, we must build against build-system jars
rm -f ./java-sdk/ldapjdk/lib/{jss32_stub,jsse,jnet,jaas,jndi}.jar

################################################################################
%build
################################################################################

pushd java-sdk/ldapjdk/lib
build-jar-repository -s -p . jss
popd

ln -s /usr/lib/jvm-exports/java/{jsse,jaas,jndi}.jar java-sdk/ldapjdk/lib

pushd java-sdk
export JAVA_HOME=%{java_home}
sh -x ant dist
popd

################################################################################
%install
################################################################################

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 java-sdk/dist/packages/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 java-sdk/dist/packages/%{spname}.jar $RPM_BUILD_ROOT%{_javadir}/%{spname}.jar
install -m 644 java-sdk/dist/packages/%{filtname}.jar $RPM_BUILD_ROOT%{_javadir}/%{filtname}.jar
install -m 644 java-sdk/dist/packages/%{beansname}.jar $RPM_BUILD_ROOT%{_javadir}/%{beansname}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 java-sdk/ldapjdk/pom.xml %{buildroot}%{_mavenpomdir}/JPP-ldapjdk.pom
install -pm 644 java-sdk/ldapfilter/pom.xml %{buildroot}%{_mavenpomdir}/JPP-ldapfilter.pom
install -pm 644 java-sdk/ldapbeans/pom.xml %{buildroot}%{_mavenpomdir}/JPP-ldapbeans.pom
install -pm 644 java-sdk/ldapsp/pom.xml %{buildroot}%{_mavenpomdir}/JPP-ldapsp.pom

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r java-sdk/dist/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

################################################################################
%files
################################################################################

%{_javadir}/%{name}.jar
%{_javadir}/%{spname}*.jar
%{_javadir}/%{filtname}*.jar
%{_javadir}/%{beansname}*.jar
%{_mavenpomdir}/JPP-ldapjdk.pom
%{_mavenpomdir}/JPP-ldapsp.pom
%{_mavenpomdir}/JPP-ldapfilter.pom
%{_mavenpomdir}/JPP-ldapbeans.pom

################################################################################
%files javadoc
################################################################################

%dir %{_javadocdir}/%{name}
%{_javadocdir}/%{name}/*

################################################################################
%changelog
* Mon Jul 26 2021 Red Hat PKI Team <rhcs-maint@redhat.com> 4.23.0-1
- Rebase to LDAP SDK 4.23.0

* Fri Jun 11 2021 Red Hat PKI Team <rhcs-maint@redhat.com> 4.23.0-0.1
- Rebase to LDAP SDK 4.23.0-alpha1

* Tue May 26 2020 Red Hat PKI Team <rhcs-maint@redhat.com> 4.22.0-1
- Rebase to LDAP SDK 4.22.0

* Thu Oct 31 2019 Red Hat PKI Team <rhcs-maint@redhat.com> 4.21.0-2
- Bump min required JSS version to 4.6.0

* Mon Jun 10 2019 Red Hat PKI Team <rhcs-maint@redhat.com> 4.21.0-1
- Rebase to LDAP SDK 4.21.0

* Fri Aug 10 2018 Red Hat PKI Team <rhcs-maint@redhat.com> 4.20.0-0
- Rebase to LDAP SDK 4.20.0

