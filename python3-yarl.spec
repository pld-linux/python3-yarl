#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Yet another URL library
Summary(pl.UTF-8):	Yet another URL library - jeszcze jedna biblioteka do URL-i
Name:		python3-yarl
Version:	1.18.3
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/yarl/
Source0:	https://files.pythonhosted.org/packages/source/y/yarl/yarl-%{version}.tar.gz
# Source0-md5:	80b89d2b28be7345a38f099b2f839d7d
URL:		https://pypi.org/project/yarl/
BuildRequires:	python3-Cython >= 3.0.11
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-expandvars
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-idna >= 2.0
BuildRequires:	python3-multidict >= 4.0
BuildRequires:	python3-propcache
BuildRequires:	python3-pytest >= 3.8.2
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-xdist
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-typing_extensions >= 3.7.4
%endif
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-alabaster
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Yet another URL library.

%description -l pl.UTF-8
YARL (Yet another URL library) to jeszcze jedna biblioteka do URL-i.

%package apidocs
Summary:	API documentation for Python yarl module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona yarl
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python yarl module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona yarl.

%prep
%setup -q -n yarl-%{version}

# keep *.c files so debuginfo will pick it up
sed -i -e 's#build_inplace: bool = False,#build_inplace: bool = True,#g' -e 's#build_inplace=False#build_inplace=True#g' packaging/pep517_backend/_backend.py

%build
%py3_build_pyproject

%if %{with tests}
%{__python} -m zipfile -e build-3/*.whl build-3-test
# run from dir not containing yarl source dir without compiled yarl._quoting_c module)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="benchmark,xdist" \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/yarl/_quoting_c.pyx

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%dir %{py3_sitedir}/yarl
%attr(755,root,root) %{py3_sitedir}/yarl/_quoting_c.cpython-*.so
%{py3_sitedir}/yarl/*.py
%{py3_sitedir}/yarl/*.pyi
%{py3_sitedir}/yarl/py.typed
%{py3_sitedir}/yarl/__pycache__
%{py3_sitedir}/yarl-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
