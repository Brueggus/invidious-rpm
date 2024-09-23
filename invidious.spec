%global git_commit a021b93063f3956fc9bb3cce0fb56ea252422738


Name:           invidious
Version:        2.20240919.0
Release:        1+%{git_commit}%{?dist}
Summary:        An alternative front-end to YouTube.
License:        AGPL-3.0
URL:            https://github.com/iv-org/invidious
Source0:        https://github.com/iv-org/invidious/archive/%{git_commit}.tar.gz
Source1:        %{name}.sysusers
Source2:        %{name}.service


ExclusiveArch: x86_64


BuildRequires:  systemd-rpm-macros
BuildRequires:  pkg-config
BuildRequires:  git
BuildRequires:  crystal1.9
BuildRequires:  openssl-devel
BuildRequires:  libevent-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyaml-devel
BuildRequires:  gmp-devel
BuildRequires:  readline-devel
BuildRequires:  librsvg2-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel
BuildRequires:  gcc


%{?systemd_requires}
%{?sysusers_requires_compat}
Requires:  openssl
Requires:  libevent
Requires:  libxml2
Requires:  libyaml
Requires:  gmp
Requires:  readline
Requires:  librsvg2
Requires:  sqlite
Requires:  zlib
Requires:  open-sans-fonts


%description
An alternative front-end to YouTube.


%prep
%autosetup -n %{name}-%{git_commit}
sed --regexp-extended --in-place \
  --expression='s/^CURRENT_BRANCH.+$/CURRENT_BRANCH = "master"/' \
  --expression='s/^CURRENT_VERSION.+$/CURRENT_VERSION = "%{version}"/' \
  --expression='s/^CURRENT_COMMIT.+$/CURRENT_COMMIT = "%{git_commit}"/' \
  --expression='s/^ASSET_COMMIT.+$/ASSET_COMMIT = "%{git_commit}"/' \
  src/invidious.cr


%build
shards install --production
crystal build ./src/invidious.cr \
  --release \
  --warnings all \
  --threads %{_smp_build_ncpus}


%install
install --directory %{buildroot}%{_sharedstatedir}/invidious/config
install --preserve-timestamps -D config/config.example.yml %{buildroot}%{_sharedstatedir}/invidious/config/config.example.yml
install --directory %{buildroot}%{_sharedstatedir}/invidious/config/sql
cp --recursive config/sql/* %{buildroot}%{_sharedstatedir}/invidious/config/sql/
install --directory %{buildroot}%{_sharedstatedir}/invidious/assets
cp --recursive assets/* %{buildroot}%{_sharedstatedir}/invidious/assets/
install --directory %{buildroot}%{_sharedstatedir}/invidious/locales
cp --recursive locales/* %{buildroot}%{_sharedstatedir}/invidious/locales/
install --preserve-timestamps --mode=0755 -D invidious %{buildroot}%{_sharedstatedir}/invidious/invidious
install --preserve-timestamps -D %{SOURCE1} %{buildroot}%{_sysusersdir}/invidious.conf
install --preserve-timestamps -D %{SOURCE2} %{buildroot}%{_unitdir}/invidious.service


%files
%doc README.md
%license LICENSE
%defattr(0640,invidious,invidious,0750)
%dir %{_sharedstatedir}/invidious
%dir %{_sharedstatedir}/invidious/config
%defattr(0440,invidious,invidious,0550)
%config(noreplace) %{_sharedstatedir}/invidious/config/config.example.yml
%{_sharedstatedir}/invidious/config/sql/
%{_sharedstatedir}/invidious/assets/
%{_sharedstatedir}/invidious/locales/
%defattr(0550,invidious,invidious,-)
%{_sharedstatedir}/invidious/invidious
%defattr(-,root,root,-)
%{_sysusersdir}/invidious.conf
%{_unitdir}/invidious.service


%pre
%sysusers_create_compat %{SOURCE1}


%post
if [ ! -f %{_sharedstatedir}/invidious/config/config.yml ]; then
  echo Using '%{_sharedstatedir}/invidious/config/config.example.yml' create '%{_sharedstatedir}/invidious/config/config.yml' invidious config.
else
  echo 'Running invidious db migrations ...'
  runuser --login invidious --shell /bin/bash --command '%{_sharedstatedir}/invidious/invidious --migrate'
  echo 'Completed invidious db migrations.'
fi
%systemd_post invidious.service


%preun
%systemd_preun invidious.service


%postun
%systemd_postun_with_restart invidious.service


%changelog
%autochangelog
