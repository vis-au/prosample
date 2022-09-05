Linearization-file convention:

- Csv format with delimiter ';'
- Column content: ID; lon; lat; attribute1; attribute2; ... (for non spatial data, lon and lat are omitted)

- In folder pipeline/linearizations/datasets/
- One header line, specifying the attributes
- Naming convention: dataset_name + 'Data.csv' (e.g. 'taxisData.csv')