<a name="ds-structuredatasetmetadatajson"> </a>

# StructureDataset tonodb

**CLDF Metadata**: [StructureDataset-metadata.json](./StructureDataset-metadata.json)

property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Hammarström, Harald & Forkel, Robert & Haspelmath, Martin & Bank, Sebastian. 2020. Glottolog 4.3. Jena: Max Planck Institute for the Science of Human History. https://doi.org/10.5281/zenodo.3754591 (Available online at http://glottolog.org, Accessed on 2020-09-30.)
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF StructureDataset](http://cldf.clld.org/v1.0/terms.rdf#StructureDataset)
[dc:identifier](http://purl.org/dc/terms/identifier) | https://github.com/uzling/tono_db
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | git@github.com:cldf-datasets/tonodb
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="git@github.com:cldf-datasets/tonodb/tree/aeb6bb8">git@github.com:cldf-datasets/tonodb aeb6bb8</a></li><li><a href="git@github.com:glottolog/glottolog/tree/f6531fcec3">Glottolog v4.4-20-gf6531fcec3</a></li><li><a href="https://github.com/uzling/tono_db/tree/ca5c624">uzling/tono_db ca5c624</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>python</strong>: 3.8.11</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | tonodb
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-valuescsv"></a>Table [values.csv](./values.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ValueTable](http://cldf.clld.org/v1.0/terms.rdf#ValueTable)
[dc:extent](http://purl.org/dc/terms/extent) | 229


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Value](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Inventory_ID](http://cldf.clld.org/v1.0/terms.rdf#contributionReference) | `string` | References [contributions.csv::ID](#table-contributionscsv)
`LanguageVariety` | `string` | 
`TriggeringContext` | `string` | 
`Extra` | `string` | 
`Height` | `string` | 
`Contour` | `string` | 
`Phonation` | `string` | 
`ToneDescription` | `string` | 
`ChaoNumerals` | `string` | 
`Notes` | `string` | 
`EffectOnPitch` | `string` | 
`ResultantSystem` | `string` | 
`Type` | `string` | 
`Onset` | `string` | 
`Coda` | `string` | 
`Stress/quantity` | `string` | 
`Wordtype` | `string` | 
`long vowel` | `string` | 

## <a name="table-parameterscsv"></a>Table [parameters.csv](./parameters.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 31


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 79


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal` | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal` | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string` | 
`family_id` | `string` | 
`parent_id` | `string` | 
`bookkeeping` | `string` | 
`level` | `string` | 
`description` | `string` | 
`markup_description` | `string` | 
`child_family_count` | `string` | 
`child_language_count` | `string` | 
`child_dialect_count` | `string` | 
`country_ids` | `string` | 

## <a name="table-contributionscsv"></a>Table [contributions.csv](./contributions.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ContributionTable](http://cldf.clld.org/v1.0/terms.rdf#ContributionTable)
[dc:extent](http://purl.org/dc/terms/extent) | 89


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Contributor](http://cldf.clld.org/v1.0/terms.rdf#contributor) | `string` | 
[Citation](http://cldf.clld.org/v1.0/terms.rdf#citation) | `string` | 
`Glottocode` | `string` | 
`LanguageVariety` | `string` | 
`Family` | `string` | 
`Area` | `string` | 
`Notes` | `string` | 
`BibTex` | `string` | 

