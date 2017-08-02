import hetio.readwrite
import numpy
import pytest

from .dwpc import dwpc_baab, categorize, get_segments


@pytest.mark.parametrize('metapath,expected', [
    ('DaGiGaD', [[0., 0.47855339],
                 [0.47855339, 0.]]),
    ('TeGiGeT', [[0, 0],
                 [0, 0]]),
    ('DaGiGeTlD', [[0, 0],
                   [0, 0]]),
    ('DaGeTeGaD', [[0, 0],
                   [0, 0]]),
    ('TlDaGiGeT', [[0., 0.47855339],
                   [0., 0.]])
])
def test_dwpc_baab(metapath, expected):
    node_dict = {
        'G': ['CXCR4', 'IL2RA', 'IRF1', 'IRF8', 'ITCH', 'STAT3', 'SUMO1'],
        'D': ["Crohn's Disease", 'Multiple Sclerosis'],
        'T': ['Leukocyte', 'Lung']
    }
    exp_row = node_dict[metapath[0]]
    exp_col = node_dict[metapath[-1]]
    url = 'https://github.com/dhimmel/hetio/raw/{}/{}'.format(
        '9dc747b8fc4e23ef3437829ffde4d047f2e1bdde',
        'test/data/disease-gene-example-graph.json',
    )
    graph = hetio.readwrite.read_graph(url)
    metapath = graph.metagraph.metapath_from_abbrev(metapath)

    row, col, dwpc_matrix = dwpc_baab(graph, metapath, damping=0.5)

    expected = numpy.array(expected, dtype=numpy.float64)

    assert abs(dwpc_matrix - expected).sum() == pytest.approx(0, abs=1e-7)
    assert exp_row == row
    assert exp_col == col


def get_baba_matrices(metapath):
    node_dict = {
        'G': ['CXCR4', 'IL2RA', 'IRF1', 'IRF8', 'ITCH', 'STAT3', 'SUMO1'],
        'D': ["Crohn's Disease", 'Multiple Sclerosis'],
        'T': ['Leukocyte', 'Lung']
    }
    edge_dict = {
        0: [[0.08838835, 0],
            [0.08838835, 0],
            [0, 0.125],
            [0.08838835, 0],
            [0, 0],
            [0, 0],
            [0, 0]],
        1: [[0, 0],
            [0, 0]],
        2: [[0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]],
        3: [[0.25, 0.],
            [0.25, 0.],
            [0., 0.],
            [0.25, 0.],
            [0., 0.],
            [0.1767767, 0.],
            [0., 0.]],
        4: [[0., 0.],
            [0., 0.],
            [0.125, 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.]],
        5: [[0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.25],
            [0., 0.]]
    }
    mat_dict = {
        'GaDaGaD': (0, 0),
        'DaGaDaG': (0, 1),
        'DlTlDlT': (1, 0),
        'TlDlTlD': (1, 1),
        'GeTeGeT': (2, 0),
        'TeGeTeG': (2, 1),
        'GaDlTeGaD': (3, 0),
        'DaGeTlDaG': (3, 1),
        'GeTlDaGaD': (4, 0),
        'DaGaDlTeG': (4, 1),
        'GaDaGeTlD': (5, 0),
        'DlTeGaDaG': (5, 1)
    }
    first = node_dict[metapath[0]]
    last = node_dict[metapath[-1]]
    edge = mat_dict[metapath]
    adj = numpy.array(edge_dict[edge[0]], dtype=numpy.float64)
    if edge[1]:
        adj = adj.transpose()
    return first, last, adj


@pytest.mark.parametrize('m_path', ('GaDaGaD', 'DaGaDaG', 'DlTlDlT',
                                    'TlDlTlD', 'GeTeGeT', 'TeGeTeG',
                                    'GaDlTeGaD', 'GeTlDaGaD', 'GaDaGeTlD'))
def test_dwpc_baba(m_path):
    url = 'https://github.com/dhimmel/hetio/raw/{}/{}'.format(
        '9dc747b8fc4e23ef3437829ffde4d047f2e1bdde',
        'test/data/disease-gene-example-graph.json',
    )
    graph = hetio.readwrite.read_graph(url)
    metagraph = graph.metagraph
    metapath = metagraph.metapath_from_abbrev(m_path)

    row_sol, col_sol, adj_sol = get_baba_matrices(m_path)
    row, col, dwpc = dwpc_baba(graph, metapath, damping=0.5)

    assert row_sol == row
    assert col_sol == col
    assert numpy.max(adj_sol - dwpc) == pytest.approx(0, abs=1e-8)

@pytest.mark.parametrize('metapath,solution', [
    ('GiG', 'short_repeat'),
    ('GiGiGiG', 'long_repeat'),
    ('G' + 10 * 'iG', 'long_repeat'),
    ('GiGiGcGcG', 'long_repeat'),  # iicc
    ('GiGcGcGiG', 'long_repeat'),  # icci
    ('GcGiGcGaDrD', 'disjoint'),  # cicDD
    ('GcGiGaDrDrD', 'disjoint'),  # ciDDD
    ('CpDaG', 'no_repeats'),  # ABC
    ('DaGiGaDaG', 'other'),  # ABBAB
    ('DaGiGbC', 'short_repeat'),  # ABBC
    ('DaGiGaD', 'BAAB'),  # ABBA
    ('GeAlDlAeG', 'BAAB'),  # ABCBA
    ('CbGaDrDaGeA', 'BAAB'),  # ABCCBD
    ('AlDlAlD', 'BABA'),  # ABAB
    ('CrCbGbCbG', 'other'),  # BBABA
    ('CbGiGbCrC', 'other'),
    ('CbGiGiGbC', 'BAAB'),
    ('CbGbCbGbC', 'other'),
    ('CrCbGiGbC', 'other'),
    ('CrCbGbCbG', 'other'),
    ('CbGaDaGeAlD', 'BABA'),  # ABCBDC
    ('AlDaGiG', 'short_repeat'),  # ABCC
    ('AeGaDaGiG', 'short_repeat'),  # ABCB
    ('CbGaDpCbGaD', 'other'),  # ABCABC
    ('DaGiGiGiGiGaD', 'other'),  # ABBBBBA
    ('CbGaDrDaGbC', 'other'),  # ABCCBA
    ('DlAuGcGpBPpGaDlA', 'other'),  # ABCCDCAB
    ('CrCbGiGaDrD', 'disjoint'),  # AABBCC
    ('CbGbCbGbC', 'other')])  # ABABA
def test_categorize(metapath, solution):
    url = 'https://github.com/dhimmel/hetio/raw/{}/{}'.format(
        '9dc747b8fc4e23ef3437829ffde4d047f2e1bdde',
        'test/data/hetionet-v1.0-metagraph.json',
    )
    metagraph = hetio.readwrite.read_metagraph(url)
    metapath = metagraph.metapath_from_abbrev(metapath)
    if not solution:
        err_dict = {
            0: "Only two overlapping repeats currently supported",
            None: "Complex metapaths of length > 4 are not yet supported"}
        with pytest.raises(NotImplementedError) as err:
            categorize(metapath)
        assert str(err.value) == err_dict[solution]
    else:
        assert categorize(metapath) == solution


@pytest.mark.parametrize('metapath,solution', [
    ('AeGiGaDaG', '[AeG, GiGaDaG]'),  # short_repeat
    ('AeGiGeAlD', '[AeG, GiG, GeA, AlD]'),  # BAABC
    ('AeGiGaDlA', '[AeG, GiG, GaDlA]'),
    ('DaGaDaG', '[DaG, GaD, DaG]'),  # BABA
    ('CbGeAlDaGbC', '[CbG, GeAlDaG, GbC]'),
    # ('SEcCpDaGeAeGaDtC', '[SEcC, CpD, DaG, GeAeG, GaD, DtC]'), # for BAAB PR
    ('DlAeGaDaG', '[DlAeG, GaD, DaG]'),  # BCABA
    ('GaDlAeGaD', '[GaD, DlAeG, GaD]'),  # BACBA
    ('GiGiG', '[GiGiG]'),  # short_repeat
    ('GiGiGiG', '[GiGiGiG]'),  # long_repeat
    ('CrCbGiGiGaDrDlA', '[CrC, CbG, GiGiG, GaD, DrD, DlA]'),
    ('CrCrCbGiGeAlDrD', '[CrCrC, CbG, GiG, GeAlD, DrD]'),
    ('SEcCrCrCbGiGeAlDrDpS', '[SEcC, CrCrC, CbG, GiG, GeAlD, DrD, DpS]'),
    ('SEcCrCrCrC', '[SEcC, CrCrCrC]')
])
def test_get_segments(metapath, solution):
    url = 'https://github.com/dhimmel/hetio/raw/{}/{}'.format(
        '9dc747b8fc4e23ef3437829ffde4d047f2e1bdde',
        'test/data/hetionet-v1.0-metagraph.json',
    )
    metagraph = hetio.readwrite.read_metagraph(url)
    metapath = metagraph.metapath_from_abbrev(metapath)
    output = str(get_segments(metagraph, metapath))
    assert output == solution

