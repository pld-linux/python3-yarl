#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Yet another URL library
Summary(pl.UTF-8):	Yet another URL library - jeszcze jedna biblioteka do URL-i
Name:		python3-yarl
Version:	1.6.3
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/yarl/
Source0:	https://files.pythonhosted.org/packages/source/y/yarl/yarl-%{version}.tar.gz
# Source0-md5:	3b6f2da3db8c645a9440375fd6a414eb
URL:		https://pypi.org/project/yarl/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-idna >= 2.0
BuildRequires:	python3-multidict >= 4.0
BuildRequires:	python3-pytest >= 3.8.2
BuildRequires:	python3-pytest-cov
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-typing_extensions >= 3.7.4
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with doc}
BuildRequires:	python3-alabaster
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Yet another URL library.

%description -l pl.UTF-8
YARL (Yet another URL library) to jeszcze jedna biblioteka do URL-i.

%package apidocs
Summary:	API documentation for Python yarl module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona yarl
Group:		Documentation
%{?noarchpackage}

%description apidocs
API documentation for Python yarl module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona yarl.

%prep
%setup -q -n yarl-%{version}

%build
%py3_build

%if %{with tests}
# run from dir not containing yarl source dir without compiled yarl._quoting_c module)
cd tests
PYTHONPATH=$(echo $(pwd)/../build-3/lib.*) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python3} -m pytest
cd ..
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/yarl/_quoting_c.{c,pyx}

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
%{py3_sitedir}/yarl-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
