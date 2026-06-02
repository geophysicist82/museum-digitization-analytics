# National Museum of Natural History (NMNH) Digitization Operations Analytics

An enterprise business intelligence and data engineering solution that designs an automated ETL pipeline and an interactive data warehouse model to track museum collection digitization throughput, labor investments, and storage infrastructure footprint.

## Project Architecture & Data Flow

The project is structured as a high-performance Star Schema data warehouse, decoupling the operational source extraction from the business analytics layer to optimize query performance and reporting scalability.



1. **Extraction & Synthesis (`data_pipeline/`)**: A modular Python script engineers synthetic operational telemetry mapping 7,500 collection items across distinct institutional departments, physical storage vaults, and curation units.
2. **Data Warehouse Modeling (`raw_data/`)**: Relational tables are structured into explicit Dimension tables (`Dim_Collection_Items`, `Dim_Storage_Vaults`, `Dim_Curation_Teams`) and a dense transactional Fact table (`Fact_Catalog_Transactions`) linked via one-to-many (1:*) numeric foreign keys.
3. **Analytics & Visual Layer (`power_bi/`)**: Ingested entities are structured into a strict single-direction filtering topology using Power BI Desktop, powered by custom Data Analysis Expressions (DAX) metrics and conditional data-mapping layers.

## Repository Directory Structure

```text
museum-digitization-analytics/
│
├── data_pipeline/
│   └── generate_museum_data.py       # Python ETL pipeline script
│
├── raw_data/                         # Star schema relational entities (Git ignored)
│   ├── Dim_Curation_Teams.csv
│   ├── Dim_Storage_Vaults.csv
│   ├── Dim_Collection_Items.csv
│   └── Fact_Catalog_Transactions.csv
│
├── power_bi/
│   └── digitization_ops.pbix         # Interactive Power BI dashboard layout
│
├── .gitignore                        # Prevents heavy raw data from polluting remote repo
└── README.md                         # Project documentation
```

# Core Analytical Capabilities & DAX Formats
The analytical canvas leverages optimized DAX formulas to translate granular transaction row logs into high-level operational indicators:

• Digitization Progress Rate (%): Dynamically tracks backlog completion velocity across distinct institutional units.

Digitization Rate = 
DIVIDE(
    CALCULATE(COUNTROWS('Fact_Catalog_Transactions'), 'Fact_Catalog_Transactions'[Is_Digitized] = 1),
    COUNTROWS('Fact_Catalog_Transactions'),
    0
)
• Total Cumulative Labor Invested (Hours): Aggregates total specialized staff time dedicated to conservation, stabilization, and asset ingestion.

Total Labor Hours = SUM('Fact_Catalog_Transactions'[Labor_Hours_Spent])
• Data Storage Footprint (Terabytes): Converts individual digital asset file markers from megabytes to institutional storage planning units.


Digital Storage (TB) = 
DIVIDE(
    SUM('Fact_Catalog_Transactions'[Digital_File_Size_MB]),
    1024 * 1024,
    0
)
# Executive Dashboard Interface
The finalized Power BI reporting layer applies enterprise-level UX/UI practices to maximize decision-making efficiency for stakeholders:

• High-Level KPI Banner: Fixed metric cards showcasing high-density operational metrics formatted with proper mathematical thousand separators and percentage signs.

• Backlog Bottleneck Detector: A clustered chart mapping total labor hour expenditures against specimen preservation states, instantly identifying structural friction points in the digitization workflow.

• Cross-Filter Layer: Interactive tile slicers driving instant, synchronous schema recalculations by building location.

• Operational Matrix Grid: A nested department-to-team matrix grid mapping throughput volumes directly against explicit status categories ("Physical Backlog" vs. "Digitized"), removing database binary flags in favor of clear business terms.

# Getting Started
Prerequisites
• Python 3.8 or higher

• Pandas and NumPy libraries

• Power BI Desktop (May 2026 build or higher)

Execution Pipeline
1. Clone the repository to your local directory.

2. Navigate to the pipeline path and execute the data engine script to regenerate or update the base relational data tables:

python data_pipeline/generate_museum_data.py

3. Open power_bi/digitization_ops.pbix in Power BI Desktop to inspect the live data model connections and interact with the executive canvas.

