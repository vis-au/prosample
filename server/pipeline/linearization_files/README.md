Linearization-file convention:

- Csv format with delimiter ';'
- Column content: ID; lon; lat; attribute1; attribute2; ... (for non spatial data, lon and lat are omitted)

- In folder modules/linearization_files/
- One header line, specifying the attributes
- Naming convention: dataset_name + 'Linearization' + technique + '.csv' (e.g. 'mountainPeaksLinearizationZOrder.csv')