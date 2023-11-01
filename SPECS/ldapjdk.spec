################################################################################
Name:             ldapjdk
################################################################################

%global           product_id idm-ldapjdk

# Upstream version number:
%global           major_version 5
%global           minor_version 3
%global           update_version 0

# Downstream release number:
# - development/stabilization (unsupported): 0.<n> where n >= 1
# - GA/update (supported): <n> where n >= 1
%global           release_number 1

# Development phase:
# - development (unsupported): alpha<n> where n >= 1
# - stabilization (unsupported): beta<n> where n >= 1
# - GA/update (supported): <none>
#global           phase

%undefine         timestamp
%undefine         commit_id

Summary:          LDAP SDK
URL:              https://github.com/dogtagpki/ldap-sdk
License:          MPLv1.1 or GPLv2+ or LGPLv2+
Version:          %{major_version}.%{minor_version}.%{update_version}
Release:          %{release_number}%{?phase:.}%{?phase}%{?timestamp:.}%{?timestamp}%{?commit_id:.}%{?commit_id}%{?dist}

# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix ldap-sdk-<version>/ \
#     -o ldap-sdk-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/ldap-sdk/archive/v%{version}%{?phase:-}%{?phase}/ldap-sdk-%{version}%{?phase:-}%{?phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > ldap-sdk-VERSION-RELEASE.patch
# Patch: ldap-sdk-VERSION-RELEASE.patch

BuildArch:        noarch

################################################################################
# Java
################################################################################

%define java_devel java-17-openjdk-devel
%define java_headless java-17-openjdk-headless
%define java_home %{_jvmdir}/jre-17-openjdk

################################################################################
# Build Dependencies
################################################################################

BuildRequires:    ant
BuildRequires:    %{java_devel}
BuildRequires:    javapackages-local
BuildRequires:    slf4j
BuildRequires:    slf4j-jdk14
BuildRequires:    jss = 5.3

%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

################################################################################
%package -n %{product_id}
################################################################################

Summary:          LDAP SDK

Requires:         %{java_headless}
Requires:         jpackage-utils >= 0:1.5
Requires:         slf4j
Requires:         slf4j-jdk14
Requires:         jss = 5.3

Obsoletes:        ldapjdk < %{version}-%{release}
Provides:         ldapjdk = %{version}-%{release}
Provides:         ldapjdk = %{major_version}.%{minor_version}
Provides:         %{product_id} = %{major_version}.%{minor_version}

%description -n %{product_id}
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%license docs/ldapjdk/license.txt

################################################################################
%package -n %{product_id}-javadoc
################################################################################

Summary:          Javadoc for LDAP SDK

Obsoletes:        ldapjdk-javadoc < %{version}-%{release}
Provides:         ldapjdk-javadoc = %{version}-%{release}
Provides:         ldapjdk-javadoc = %{major_version}.%{minor_version}
Provides:         %{product_id}-javadoc = %{major_version}.%{minor_version}

%description -n %{product_id}-javadoc
Javadoc for LDAP SDK

################################################################################
%prep
################################################################################

%autosetup -n ldap-sdk-%{version}%{?phase:-}%{?phase} -p 1

################################################################################
%build
################################################################################

export JAVA_HOME=%{java_home}

./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    dist

################################################################################
%install
################################################################################

./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --java-lib-dir=%{_javadir} \
    --javadoc-dir=%{_javadocdir} \
    --install-dir=%{buildroot} \
    install

################################################################################
%files -n %{product_id}
################################################################################

%{_javadir}/ldapjdk.jar
%{_javadir}/ldapsp.jar
%{_javadir}/ldapfilt.jar
%{_javadir}/ldapbeans.jar
%{_javadir}/ldaptools.jar
%{_mavenpomdir}/JPP-ldapjdk.pom
%{_mavenpomdir}/JPP-ldapsp.pom
%{_mavenpomdir}/JPP-ldapfilter.pom
%{_mavenpomdir}/JPP-ldapbeans.pom
%{_mavenpomdir}/JPP-ldaptools.pom

################################################################################
%files -n %{product_id}-javadoc
################################################################################

%dir %{_javadocdir}/ldapjdk
%{_javadocdir}/ldapjdk/*

################################################################################
%changelog
* Fri Feb 10 2023 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.3.0-1
- Rebase to LDAP SDK 5.3.0

* Wed Nov 30 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.3.0-0.2.beta1
- Rebase to LDAP SDK 5.3.0-beta1

* Thu Jun 30 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.2.0-1
- Rebase to LDAP SDK 5.2.0

* Mon May 02 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.2.0-0.3.beta2
- Rebase to LDAP SDK 5.2.0-beta2
- Rename packages to idm-ldapjdk

* Mon Apr 18 2022 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.2.0-0.2.beta1
- Rebase to LDAP SDK 5.2.0-beta1

* Tue Oct 05 2021 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.0.0-1
- Rebase to LDAP SDK 5.0.0

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 5.0.0-0.3.alpha1
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Aug  2 2021 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.0.0-0.2
- Drop javadoc package

* Fri Jun 25 2021 Red Hat PKI Team <rhcs-maint@redhat.com> - 5.0.0-0.1
- Rebase to LDAP SDK 5.0.0-alpha1
