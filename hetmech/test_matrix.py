import hetio.readwrite
import numpy
import pytest
from scipy import sparse

from .matrix import metaedge_to_adjacency_matrix


def get_arrays(edge, mat_type, dtype):  # Define a dictionary
    rows_dict = {
        'GiG': ['CXCR4', 'IL2RA', 'IRF1', 'IRF8', 'ITCH', 'STAT3', 'SUMO1'],
        'GaD': ['CXCR4', 'IL2RA', 'IRF1', 'IRF8', 'ITCH', 'STAT3', 'SUMO1'],
        'DlT': ["Crohn's Disease", 'Multiple Sclerosis'],
        'TlD': ['Leukocyte', 'Lung']
    }
    cols_dict = {
        'GiG': ['CXCR4', 'IL2RA', 'IRF1', 'IRF8', 'ITCH', 'STAT3', 'SUMO1'],
        'GaD': ["Crohn's Disease", 'Multiple Sclerosis'],
        'DlT': ['Leukocyte', 'Lung'],
        'TlD': ["Crohn's Disease", 'Multiple Sclerosis']
    }
    adj_dict = {
        'GiG': [[0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [1, 1, 0, 1, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0]],
        'GaD': [[0, 1],
                [0, 1],
                [1, 0],
                [0, 1],
                [0, 0],
                [1, 1],
                [0, 0]],
        'DlT': [[0, 0],
                [1, 0]],
        'TlD': [[0, 1],
                [0, 0]]
    }
    return rows_dict[edge], cols_dict[edge], mat_type(adj_dict[edge],
                                                      dtype=dtype)


@pytest.mark.parametrize("test_edge", ['GiG', 'GaD', 'DlT', 'TlD'])
@pytest.mark.parametrize("mat_type", [numpy.array, sparse.csc_matrix,
                                      sparse.csr_matrix, numpy.matrix])
@pytest.mark.parametrize("dtype", [numpy.bool_, numpy.int64, numpy.int32])
def test_metaedge_to_adjacency_matrix(test_edge, mat_type, dtype):
    """
    Test the functionality of metaedge_to_adjacency_matrix in generating
    numpy arrays. Uses same test data as in test_degree_weight.py
    Figure 2D of Himmelstein & Baranzini (2015) PLOS Comp Bio.
    https://doi.org/10.1371/journal.pcbi.1004259.g002
    """
    url = 'https://github.com/dhimmel/hetio/raw/{}/{}'.format(
        '9dc747b8fc4e23ef3437829ffde4d047f2e1bdde',
        'test/data/disease-gene-example-graph.json',
    )
    graph = hetio.readwrite.read_graph(url)
    row_names, col_names, adj_mat = \
        metaedge_to_adjacency_matrix(graph, test_edge, matrix_type=mat_type,
                                     dtype=dtype)
    exp_row, exp_col, exp_adj = get_arrays(test_edge, mat_type, dtype)

    assert row_names == exp_row
    assert col_names == exp_col
    assert type(adj_mat) == type(exp_adj)  # Arrays same type
    assert not sparse.csc_matrix(adj_mat != exp_adj).nnz  # Arrays equal
    assert adj_mat.dtype == dtype
    assert isinstance(
        adj_mat, mat_type if mat_type != numpy.array else numpy.ndarray
    )
