import hetio.readwrite
import numpy
import pytest

from .dwpc import dwpc_general_case


def get_general_solutions(length):
    genes = ['CXCR4', 'IL2RA', 'IRF1', 'IRF8', 'ITCH', 'STAT3', 'SUMO1']
    mat_dict = {
        0: [[0, 0, 0.35355339, 0, 0.70710678, 0, 0],
            [0, 0, 0.5, 0, 0, 0, 0],
            [0.35355339, 0.5, 0, 0.5, 0, 0, 0.5],
            [0, 0, 0.5, 0, 0, 0, 0],
            [0.70710678, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0.5, 0, 0, 0, 0]],
        1: [[0, 0.1767767, 0, 0.1767767, 0, 0, 0.1767767],
            [0.1767767, 0, 0, 0.25, 0, 0, 0.25],
            [0, 0, 0, 0, 0.25, 0, 0],
            [0.1767767, 0.25, 0, 0, 0, 0, 0.25],
            [0, 0, 0.25, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0.1767767, 0.25, 0, 0.25, 0, 0, 0]],
        2: [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0.125, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0.125, 0, 0],
            [0, 0.125, 0, 0.125, 0, 0, 0.125],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0.125, 0, 0]],
        3: numpy.zeros((7, 7)),
        4: numpy.zeros((7, 7)),
        5: numpy.zeros((7, 7))
    }
    return genes, genes, mat_dict[length]


@pytest.mark.parametrize('length', list(range(6)))
def test_dwpc_general_case(length):
    """
    Test the functionality of dwpc_same_metanode to find DWPC
    within a metapath (segment) of metanode and metaedge repeats.
    """
    url = 'https://github.com/dhimmel/hetio/raw/{}/{}'.format(
        '9dc747b8fc4e23ef3437829ffde4d047f2e1bdde',
        'test/data/disease-gene-example-graph.json',
    )
    graph = hetio.readwrite.read_graph(url)
    metagraph = graph.metagraph
    m_path = 'GiG' + length*'iG'
    metapath = metagraph.metapath_from_abbrev(m_path)
    rows, cols, dwpc_mat = dwpc_general_case(graph, metapath, damping=0.5)
    exp_row, exp_col, exp_dwpc = get_general_solutions(length)

    # Test matrix, row, and column label output
    assert abs(dwpc_mat - exp_dwpc).sum() == pytest.approx(0, abs=1e-7)
    assert rows == exp_row
    assert cols == exp_col


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

    row, col, dwpc_matrix = dwpc_general_case(graph, metapath, damping=0.5)

    expected = numpy.array(expected, dtype=numpy.float64)

    assert pytest.approx(numpy.max(dwpc_matrix - expected) == 0)
    assert exp_row == row
    assert exp_col == col


def get_matrices(metapath):
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

    row_sol, col_sol, adj_sol = get_matrices(m_path)
    row, col, dwpc = dwpc_general_case(graph, metapath, damping=0.5)

    assert row_sol == row
    assert col_sol == col
    assert numpy.max(adj_sol - dwpc) == pytest.approx(0, abs=1e-8)
