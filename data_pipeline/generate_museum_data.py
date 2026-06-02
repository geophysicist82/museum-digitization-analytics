# -*- coding: utf-8 -*-
"""
Module: generate_museum_data.py
Description: Generates a highly relational multi-table dataset simulating 
             museum collection logistics, digitization throughput, and storage capacity.
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_museum_star_schema(output_dir, num_items=5000):
    os.makedirs(output_dir, exist_ok=True)
    random.seed(42)
    np.random.seed(42)
    
    print(f"Engineering relational schema matrices for {num_items} items...")

    # --- 1. DIMENSION: Curation Teams ---
    teams_data = {
        "Team_ID": [101, 102, 103, 104, 105],
        "Team_Name": ["Alpha Archival", "Beta Botany", "Gamma Geo-Acoustic", "Delta Digitization", "Epsilon Ethnology"],
        "Department": ["Anthropology", "Botany", "Mineral Sciences", "Paleobiology", "Anthropology"],
        "Daily_Throughput_Target": [45, 60, 30, 75, 40]
    }
    df_teams = pd.DataFrame(teams_data)
    
    # --- 2. DIMENSION: Storage Vaults ---
    vault_rooms = ["Room A-10", "Room B-22", "Vault 4", "Sub-Basement C", "Offsite Archive"]
    vaults_data = []
    vault_id = 1
    for bld in ["Main Building", "Support Facility", "East Wing"]:
        for room in vault_rooms:
            for aisle in range(1, 6):
                vaults_data.append({
                    "Vault_ID": vault_id,
                    "Building": bld,
                    "Room": room,
                    "Aisle_Grid": f"Aisle-{aisle}",
                    "Max_Shelf_Capacity": random.randint(500, 1500)
                })
                vault_id += 1
    df_vaults = pd.DataFrame(vaults_data)

    # --- 3. DIMENSION: Collection Items ---
    divisions = ["Anthropology", "Botany", "Mineral Sciences", "Paleobiology"]
    preservation_states = ["Excellent", "Stable", "Fragile", "Critical - Requiring Stabilization"]
    
    items_data = []
    for item_id in range(100001, 100001 + num_items):
        div = random.choice(divisions)
        items_data.append({
            "Item_ID": item_id,
            "Catalog_Number": f"NMNH-{random.randint(10,99)}-{item_id}",
            "Division": div,
            "Collection_Object_Group": f"{div} Secondary Collection" if random.random() > 0.5 else f"{div} Primary Type",
            "Preservation_State": np.random.choice(preservation_states, p=[0.4, 0.4, 0.15, 0.05]),
            "Year_Acquired": random.randint(1920, 2025)
        })
    df_items = pd.DataFrame(items_data)

    # --- 4. FACT: Catalog Transactions ---
    start_date = datetime(2024, 1, 1)
    transactions = []
    
    # Filter arrays for quick relational matching in loop
    vault_ids = df_vaults["Vault_ID"].values
    
    for idx, row in df_items.iterrows():
        # Match team based on department alignment
        valid_teams = df_teams[df_teams["Department"] == row["Division"]]["Team_ID"].values
        if len(valid_teams) == 0:
            valid_teams = df_teams["Team_ID"].values
        team_assigned = random.choice(valid_teams)
        
        # Simulate processing timelines across the last 2.5 years
        days_offset = random.randint(0, 880)
        tx_date = start_date + timedelta(days=days_offset)
        
        # Unstructured metadata flags
        is_digitized = np.random.choice([1, 0], p=[0.65, 0.35])
        file_size_mb = round(random.uniform(15.5, 450.2), 2) if is_digitized else 0.0
        
        # Audit hours spent processing
        base_hours = {"Excellent": 0.5, "Stable": 1.0, "Fragile": 3.5, "Critical - Requiring Stabilization": 8.0}
        audit_hours = base_hours[row["Preservation_State"]] + random.uniform(-0.2, 1.5)

        transactions.append({
            "Transaction_ID": f"TXN-{1000000 + idx}",
            "Item_ID": row["Item_ID"],
            "Team_ID": team_assigned,
            "Vault_ID": random.choice(vault_ids),
            "Transaction_Date": tx_date.strftime("%Y-%m-%d"),
            "Is_Digitized": is_digitized,
            "Digital_File_Size_MB": file_size_mb,
            "Labor_Hours_Spent": round(max(0.2, audit_hours), 2),
            "Objects_Processed_Count": 1
        })
        
    df_fact = pd.DataFrame(transactions)

    # Export to disk as individual clean CSV entities
    df_teams.to_csv(os.path.join(output_dir, "Dim_Curation_Teams.csv"), index=False)
    df_vaults.to_csv(os.path.join(output_dir, "Dim_Storage_Vaults.csv"), index=False)
    df_items.to_csv(os.path.join(output_dir, "Dim_Collection_Items.csv"), index=False)
    df_fact.to_csv(os.path.join(output_dir, "Fact_Catalog_Transactions.csv"), index=False)
    
    print(f"ETL Generation Complete! Files exported to: {output_dir}")

if __name__ == "__main__":
    # 1. Get the absolute path of the directory where this script is actually saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Go up one level from the script directory to hit the project root
    project_root = os.path.dirname(script_dir)
    
    # 3. Explicitly point to the raw_data folder at the project root
    target_path = os.path.join(project_root, "raw_data")
    
    # Run the schema generator with the bulletproof absolute path
    create_museum_star_schema(target_path, num_items=7500)