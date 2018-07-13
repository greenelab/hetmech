import pandas
import scipy.special
import scipy.stats

import hetmech.degree_group
import hetmech.degree_weight
import hetmech.hetmat


def compute_save_dgp(hetmat, metapath, damping=0.5, compression='gzip', delete_intermediates=True):
    """
    Compute summary file of combined degree-grouped permutations (DGP). Aggregates across permutations,
    deleting intermediates if delete_intermediates=True. Saves resulting files as compressed .tsv files
    using compression method given by compression. Does not recompute previously saved files.
    """
    for mp in (metapath.inverse, metapath):
        combined_path = hetmat.get_summary_degree_group_path(metapath, 'dwpc', damping)
        if combined_path.exists():
            return

    _, _, matrix = hetmat.read_path_counts(metapath, 'dwpc', damping)
    matrix_mean = matrix.mean()

    for name, permat in hetmat.permutations.items():
        path = permat.get_degree_group_path(metapath, metric, damping)
        if not path.exists():
            degree_grouped_df = hetmech.degree_group.single_permutation_degree_group(
                permat, metapath, dwpc_mean=matrix_mean, damping=damping)
            path.parent.mkdir(parents=True, exist_ok=True)
            degree_grouped_df.to_csv(path, sep='\t')

    degree_stats_df = hetmech.degree_group.summarize_degree_grouped_permutations(
        hetmat, metapath, damping=damping, delete_intermediates=delete_intermediates)
    combined_path.parent.mkdir(parents=True, exist_ok=True)
    degree_stats_df.to_csv(combined_path, sep='\t', compression=compression)


def combine_dwpc_dgp(graph, metapath, damping):
    """
    Combine DWPC information with degree-grouped permutation summary metrics.
    Save resulting tables as one-per-metapath, compressed .tsv files that include
    gamma-hurdle significance estimates.
    """
    stats_path = graph.get_summary_degree_group_path(metapath, 'dwpc', damping)
    degree_stats_df = pandas.read_table(stats_path, compression='gzip')

    dwpc_row_generator = hetmech.degree_group.dwpc_to_degrees(graph, metapath)
    dwpc_df = pandas.DataFrame(dwpc_row_generator)
    df = (
        dwpc_df
        .merge(degree_stats_df, on=['source_degree', 'target_degree'])
        .drop(columns=['source_degree', 'target_degree'])
    )
    df['mean-nz'] = df['mean'] * df['n'] / df['nnz']
    df['beta'] = df['mean-nz'] / df['sd'] ** 2
    df['alpha'] = df['mean-nz'] * df['beta']
    df['p-value'] = df['nnz'] / df['n'] * scipy.special.gammaincc(df['alpha'], df['beta'] * df['dwpc'])
    return df
