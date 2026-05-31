from nova.data.profiler import DatasetProfiler

def test_csv_profile(tmp_path):
    p = tmp_path / 'data.csv'
    p.write_text('a,b\n1,x\n2,y\n')
    prof = DatasetProfiler().profile_csv(p)
    assert prof['rows_sampled'] == 2
    assert prof['columns']['a']['type'] == 'numeric'
