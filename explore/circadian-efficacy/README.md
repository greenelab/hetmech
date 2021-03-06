# Circadian Drug Efficacy

Evaluating unsupervised DWPC p-values and path contributions to predict whether a drug's efficacy is time-of-day dependent.


# Source datasets

+ [`downloads/HumCircMed2018v2.xlsx`](downloads/HumCircMed2018v2.xlsx) contains the data to generate Figure S1 from [version 1 of the "Dosing Time Matters" preprint](https://www.biorxiv.org/content/10.1101/570119v1.full).

+ [`downloads/aat8806_Data_file_S1.xlsx`](downloads/aat8806_Data_file_S1.xlsx) contains data from CircaDB, which provides tissue-specific rhythmical scores for human genes. 
  The data was downloaded from Data file S1 of [A database of tissue-specific rhythmically expressed human genes has potential applications in circadian medicine](https://doi.org/10.1126/scitranslmed.aat8806).
  The algorithm 'CYCLOPS', which was developed to score genes based on circadian rhythms, can be accessed from [CYCLOPS reveals human transcriptional rhythms in health and disease](https://doi.org/10.1073/pnas.1619320114).

+ [`downloads/GTEx_Analysis_2016-01-15_v7_RNASeQCv1.1.8_gene_median_tpm.gct.gz`](downloads/GTEx_Analysis_2016-01-15_v7_RNASeQCv1.1.8_gene_median_tpm.gct.gz) contains median expression of all genes in 55 GTEx tissues.
  The data was downloaded from [GTEx V7 RNA-seq data](https://storage.googleapis.com/gtex_analysis_v7/rna_seq_data/GTEx_Analysis_2016-01-15_v7_RNASeQCv1.1.8_gene_median_tpm.gct.gz)

# Generated datasets

+ [`data/disease_doid.tsv`](data/disease_doid.tsv) contains manually curated mapping from therapeutic area to disease ontology ID.

+ [`data/tissue_uberon.tsv`](data/tissue_uberon.tsv) contains manually curated mapping from CircaDB tissue terms to exact Uberon tissue IDs, hetionet Uberon tissue IDs(closest tissue available in hetionet), and GTEx tissue names.

+ [`data/HumCircMed2018v2_mapped.tsv`](data/HumCircMed2018v2_mapped.tsv) is a processed version of [`downloads/HumCircMed2018v2.xlsx`](downloads/HumCircMed2018v2.xlsx). 
  It mapped compound names to DrugBank IDs, mapped therapeutic areas to DOIDs

+ [`data/circa_db_mapped.tsv`](data/circa_db_mapped.tsv) is a processed version of [`downloads/aat8806_Data_file_S1.xlsx`](downloads/aat8806_Data_file_S1.xlsx).
  It organized circadian scores by gene, added median tissue-specific expression value of each gene from GTEx.

+ [`data/rephetio_significant_metapaths.tsv`](data/rephetio_significant_metapaths.tsv) contains 67 metapaths that are used for calculating the edge circadian score. These metapaths were extracted from [Project Rephetio](https://het.io/repurpose/metapaths.html). Metapaths with delta(AUROC)>0 and -log(P)>1.30 were considered. 

+ [`data/HumCircMed2018v2_mapped_edge_circa_scores.tsv`](data/HumCircMed2018v2_mapped_edge_circa_scores.tsv) contains calculated calculate edge circadian scores for drug-disease pairs from Ruben et al dataset.

+ [`data/indication_edge_circa_scores.tsv`](data/indication_edge_circa_scores.tsv) contains calculated edge circadian scores for drug-disease pairs from indication dataset.

# Notebook

+ [`data_id_mapping.ipynb`](data_id_mapping.ipynb) contains the codes that map treatment and CircaDB data to hetionet IDs.  

+ [`calculate_edge_circa_score_ruben.ipynb`](calculate_edge_circa_score_ruben.ipynb) contains the codes that calculate edge circadian scores for drug-disease pairs from Ruben et al dataset.

+ [`calculate_edge_circa_score_indication.ipynb`](calculate_edge_circa_score_indication.ipynb) contains the codes that calculate edge circadian scores for drug-disease pairs from indication dataset.

+ [`analyze_edge_circa_score.ipynb`](analyze_edge_circa_score.ipynb) contains the codes that analyze edge circadian scores of drug-disease pairs from Ruben et al dataset and indication dataset.

+ [`detail_edge_circa_score.ipynb`](detail_edge_circa_score.ipynb) contains the codes that obtain details of edge circadian score in each path.
