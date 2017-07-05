from collections import OrderedDict

import numpy

from .matrix import (normalize,
                     get_node_to_position,
                     metaedge_to_adjacency_matrix,
                     copy_array)


def diffusion_step(
        matrix, row_damping=0, column_damping=0, copy=True):
    """
    Return the diffusion adjacency matrix produced by the input matrix
    with the specified row and column normalization exponents.
    Note: the row normalization is performed second, so if a value
    of row_damping=1 is used, the output will be a row-stochastic
    matrix regardless of choice of column normalization.

    Parameters
    ==========
    matrix : numpy.ndarray
        adjacency matrix for a given metaedge, where the source nodes are
        rows and the target nodes are columns
    row_damping : int or float
        exponent to use in scaling each node's row by its in-degree
    column_damping : int or float
        exponent to use in scaling each node's column by its column-sum
    copy : bool
        `True` guarantees matrix will not be modified in place. `False`
        modifies in-place if and only if matrix.dtype == numpy.float64.
        Users are recommended not to rely on in-place conversion, but instead
        use `False` when in-place modification is acceptable and efficiency
        is desired.

    Returns
    =======
    numpy.ndarray
        Normalized matrix with dtype.float64.
    """
    # returns a newly allocated array if copy is True
    matrix = copy_array(matrix, copy=copy)

    # Perform column normalization
    if column_damping != 0:
        column_sums = numpy.array(matrix.sum(axis=0)).flatten()
        matrix = normalize(matrix, column_sums, 'columns', column_damping)

    # Perform row normalization
    if row_damping != 0:
        row_sums = numpy.array(matrix.sum(axis=1)).flatten()
        matrix = normalize(matrix, row_sums, 'rows', row_damping)

    return matrix


def diffuse(
        graph,
        metapath,
        source_node_weights,
        column_damping=0,
        row_damping=1
        ):
    """
    Performs diffusion from the specified source nodes.

    Parameters
    ==========
    graph : hetio.hetnet.Graph
        graph to extract adjacency matrices along
    metapath : hetio.hetnet.MetaPath
        metapath to diffuse along
    source_node_weights : dict
        dictionary of node to weight. Nodes not in dict are zero-weighted
    column_damping : scalar
        exponent of (out)degree in column normalization
    row_damping : scalar
        exponent of (in)degree in row normalization
    """

    # Initialize node weights
    source_metanode = metapath.source()
    source_node_to_position = get_node_to_position(graph, source_metanode)
    node_scores = numpy.zeros(len(source_node_to_position))
    for source_node, weight in source_node_weights.items():
        i = source_node_to_position[source_node]
        node_scores[i] = weight

    for metaedge in metapath:
        row_names, column_names, adjacency_matrix = (
            metaedge_to_adjacency_matrix(graph, metaedge))

        # Row/column normalization with degree damping
        adjacency_matrix = diffusion_step(
            adjacency_matrix, row_damping, column_damping)

        node_scores = node_scores @ adjacency_matrix

    node_to_score = OrderedDict(zip(column_names, node_scores))
    return node_to_score
