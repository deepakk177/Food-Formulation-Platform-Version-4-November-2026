# Dataset Profiling Report: Flavordb

*   **Domain**: Semi_structured
*   **Total Files**: 41
*   **Total Size**: 3533.6 KB
*   **Formats**: html, json

## Files Inspected

### `entity_1.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_1.html`
*   **MIME Type**: `text/html`
*   **Size**: 20.56 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_1.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_1.json`
*   **MIME Type**: `application/json`
*   **Size**: 8.15 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_10.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_10.html`
*   **MIME Type**: `text/html`
*   **Size**: 26.6 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_10.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_10.json`
*   **MIME Type**: `application/json`
*   **Size**: 17.32 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_11.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_11.html`
*   **MIME Type**: `text/html`
*   **Size**: 72.46 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_11.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_11.json`
*   **MIME Type**: `application/json`
*   **Size**: 64.46 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_12.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_12.html`
*   **MIME Type**: `text/html`
*   **Size**: 73.91 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_12.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_12.json`
*   **MIME Type**: `application/json`
*   **Size**: 65.85 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_13.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_13.html`
*   **MIME Type**: `text/html`
*   **Size**: 104.91 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_13.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_13.json`
*   **MIME Type**: `application/json`
*   **Size**: 95.84 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_14.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_14.html`
*   **MIME Type**: `text/html`
*   **Size**: 73.75 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_14.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_14.json`
*   **MIME Type**: `application/json`
*   **Size**: 65.89 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_15.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_15.html`
*   **MIME Type**: `text/html`
*   **Size**: 73.84 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_15.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_15.json`
*   **MIME Type**: `application/json`
*   **Size**: 65.79 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_16.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_16.html`
*   **MIME Type**: `text/html`
*   **Size**: 77.51 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_16.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_16.json`
*   **MIME Type**: `application/json`
*   **Size**: 67.3 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_17.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_17.html`
*   **MIME Type**: `text/html`
*   **Size**: 254.7 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_17.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_17.json`
*   **MIME Type**: `application/json`
*   **Size**: 259.56 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_18.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_18.html`
*   **MIME Type**: `text/html`
*   **Size**: 73.61 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_18.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_18.json`
*   **MIME Type**: `application/json`
*   **Size**: 65.64 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_19.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_19.html`
*   **MIME Type**: `text/html`
*   **Size**: 90.48 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_19.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_19.json`
*   **MIME Type**: `application/json`
*   **Size**: 82.93 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_2.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_2.html`
*   **MIME Type**: `text/html`
*   **Size**: 148.23 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_2.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_2.json`
*   **MIME Type**: `application/json`
*   **Size**: 167.1 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_20.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_20.html`
*   **MIME Type**: `text/html`
*   **Size**: 101.51 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_20.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_20.json`
*   **MIME Type**: `application/json`
*   **Size**: 96.41 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_3.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_3.html`
*   **MIME Type**: `text/html`
*   **Size**: 45.95 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_3.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_3.json`
*   **MIME Type**: `application/json`
*   **Size**: 40.03 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_4.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_4.html`
*   **MIME Type**: `text/html`
*   **Size**: 45.19 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_4.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_4.json`
*   **MIME Type**: `application/json`
*   **Size**: 37.52 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_5.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_5.html`
*   **MIME Type**: `text/html`
*   **Size**: 23.43 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_5.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_5.json`
*   **MIME Type**: `application/json`
*   **Size**: 16.33 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_6.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_6.html`
*   **MIME Type**: `text/html`
*   **Size**: 74.64 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_6.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_6.json`
*   **MIME Type**: `application/json`
*   **Size**: 75.0 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_7.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_7.html`
*   **MIME Type**: `text/html`
*   **Size**: 87.14 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_7.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_7.json`
*   **MIME Type**: `application/json`
*   **Size**: 81.25 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_8.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_8.html`
*   **MIME Type**: `text/html`
*   **Size**: 17.74 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_8.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_8.json`
*   **MIME Type**: `application/json`
*   **Size**: 7.06 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_9.html`
*   **Path**: `data/raw/semi_structured/flavordb/entity_9.html`
*   **MIME Type**: `text/html`
*   **Size**: 315.15 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `entity_9.json`
*   **Path**: `data/raw/semi_structured/flavordb/entity_9.json`
*   **MIME Type**: `application/json`
*   **Size**: 336.74 KB

#### Schema Details
*   **Schema Type**: JSON Hierarchy
*   **Columns**: fema_number, molecular_weight, flavornet_id, fema_flavor_profile, charge, bond_stereo_count, odor, defined_bond_stereocenter_count, monoisotopic_mass, volume3d, cas_id, bitterdb_id, xlogp, undefined_bond_stereocenter_count, bitter, iupac_name, isotope_atom_count, common_name, supersweetdb_id, covalently_bonded_unit_count, defined_atom_stereocenter_count, flavor_profile, smile, num_rotatablebonds, hba_count, undefined_atom_stereocenter_count, pubchem_id, fooddb_flavor_profile, fooddb_id, heavy_atom_count, functional_groups, inchi, natural, synthetic, topological_polor_surfacearea, unknown_natural, exact_mass, atom_stereo_count, super_sweet, taste, fenoroli_and_os, complexity, hbd_count
*   **Nested JSON Paths**: natural_source_url, molecules[*].fema_number, molecules[*], molecules[*].molecular_weight, molecules[*].flavornet_id, molecules[*].fema_flavor_profile, molecules[*].charge, molecules[*].bond_stereo_count, entity_alias, molecules[*].odor, molecules[*].defined_bond_stereocenter_count, category_readable, molecules[*].monoisotopic_mass, molecules[*].volume3d, molecules[*].cas_id, entity_alias_basket, molecules[*].bitterdb_id, molecules[*].xlogp, entity_alias_url, molecules[*].undefined_bond_stereocenter_count, molecules[*].bitter, molecules[*].iupac_name, molecules[*].isotope_atom_count, molecules[*].common_name, molecules[*].supersweetdb_id, molecules[*].covalently_bonded_unit_count, molecules[*].defined_atom_stereocenter_count, natural_source_name, entity_alias_readable, molecules[*].flavor_profile, molecules[*].smile, molecules[*].num_rotatablebonds, molecules[*].hba_count, entity_alias_synonyms, molecules[*].undefined_atom_stereocenter_count, molecules[*].pubchem_id, category, entity_id, molecules[*].fooddb_flavor_profile, molecules[*].fooddb_id, molecules[*].heavy_atom_count, molecules, molecules[*].functional_groups, molecules[*].inchi, molecules[*].natural, molecules[*].synthetic, molecules[*].topological_polor_surfacearea, molecules[*].unknown_natural, molecules[*].exact_mass, molecules[*].atom_stereo_count, molecules[*].super_sweet, molecules[*].taste, molecules[*].fenoroli_and_os, molecules[*].complexity, molecules[*].hbd_count

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   Field `flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `functional_groups` $\rightarrow$ **Functional Role** (Confidence: 0.64)
*   Field `taste` $\rightarrow$ **Flavor** (Confidence: 1.0)
*   Field `molecules[*].fema_number` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*]` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].molecular_weight` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavornet_id` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fema_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].charge` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bond_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].odor` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].monoisotopic_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].volume3d` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].cas_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitterdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].xlogp` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_bond_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].bitter` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].iupac_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].isotope_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].common_name` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].supersweetdb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].covalently_bonded_unit_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].defined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].smile` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].num_rotatablebonds` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hba_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].undefined_atom_stereocenter_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].pubchem_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].fooddb_flavor_profile` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fooddb_id` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].heavy_atom_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].functional_groups` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].inchi` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].synthetic` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].topological_polor_surfacearea` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].unknown_natural` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].exact_mass` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].atom_stereo_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].super_sweet` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].taste` $\rightarrow$ **Flavor** (Confidence: 0.8)
*   Field `molecules[*].fenoroli_and_os` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].complexity` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)
*   Field `molecules[*].hbd_count` $\rightarrow$ **Flavor Molecule** (Confidence: 0.72)

#### Candidate Relationships Mapping
*   No relationships detected.

---
### `flavordb_home.html`
*   **Path**: `data/raw/semi_structured/flavordb/flavordb_home.html`
*   **MIME Type**: `text/html`
*   **Size**: 16.11 KB

#### Schema Details
*   **Schema Type**: HTML Page
*   **Columns**: table_data, list_data, meta_description

#### Data Quality
*   **Readiness Score**: 1.0
*   **Valid UTF-8**: True
*   **Broken Format**: False
*   **Duplicate Rows**: 0

#### Candidate Entities Mapping
*   No entities detected.

#### Candidate Relationships Mapping
*   No relationships detected.

---