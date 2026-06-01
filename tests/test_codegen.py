from nova.codegen.project_generator import ProjectGenerator
from nova.codegen.analyzer import CodebaseAnalyzer
from nova.codegen.security_review import SecurityReviewer

def test_project_generator_and_analyzer(tmp_path):
    target = tmp_path/'app'
    ProjectGenerator().new('cli', target)
    assert (target/'README.md').exists()
    out = CodebaseAnalyzer().analyze(target)
    assert out['file_count'] >= 1

def test_security_reviewer(tmp_path):
    (tmp_path/'bad.py').write_text('import subprocess\nsubprocess.run("x", shell=True)\n', encoding='utf-8')
    out = SecurityReviewer().review(tmp_path)
    assert out['finding_count'] >= 1
