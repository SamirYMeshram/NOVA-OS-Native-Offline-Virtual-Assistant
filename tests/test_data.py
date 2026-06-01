from nova.data.profiler import DatasetProfiler

def test_csv_profile(tmp_path):
    p = tmp_path/'x.csv'; p.write_text('a,b\n1,2\n3,\n', encoding='utf-8')
    out = DatasetProfiler().profile(p)
    assert out['rows'] == 2
    assert out['stats']['b']['missing'] == 1
