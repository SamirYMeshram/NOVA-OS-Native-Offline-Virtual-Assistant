from nova.codegen.templates import ProjectTemplates

def test_python_cli_template(tmp_path):
    root = ProjectTemplates().python_cli(tmp_path / 'app', 'demo-tool')
    assert (root / 'pyproject.toml').exists()
    assert (root / 'demo_tool' / 'cli.py').exists()
