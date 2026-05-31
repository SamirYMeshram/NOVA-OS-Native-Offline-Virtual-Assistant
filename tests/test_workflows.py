from nova.workflows.project_review import ProjectReviewWorkflow

def test_project_review(tmp_path):
    (tmp_path / 'a.py').write_text('print("x")\n')
    result = ProjectReviewWorkflow().run(tmp_path)
    assert result['analysis']['python_files'] == 1
