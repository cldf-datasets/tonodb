import pathlib
import subprocess
import unicodedata
from cldfbench import Dataset as BaseDataset
from cldfbench import CLDFSpec


# copy from https://github.com/cldf-datasets/phoible/blob/phoible-3.0/cldfbench_phoible.py#L91
def glang_attrs(glang, languoids):
    """
    Enrich language metadata with attributes we can fetch from Glottolog.
    """
    res = {k: None for k in 'Macroarea'.split(',')}

    if not glang.macroareas:
        if glang.level.name == 'dialect':
            for _, gc, _ in reversed(glang.lineage):
                if languoids[gc].macroareas:
                    res['Macroarea'] = languoids[gc].macroareas[0].name
                    break
    else:
        res['Macroarea'] = glang.macroareas[0].name

    return res

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "tonodb"
    valueTableProperties = ['TriggeringContext', 'Extra', 'Hight', 'Countour', 'Phonation', 'ToneDescription', 'ChaoNumerals', 'EffectOnPitch', 'Notes', 'ResultantSystem', 'Type', 'Onset', 'Coda', 'Stress/quantity', 'Wordtype', 'Nucleus']
    languageTableProperties = ['family_id', 'parent_id', 'bookkeeping', 'level', 'description', 'markup_description', 'child_family_count', 'child_language_count', 'child_dialect_count', 'country_ids']
    inventoryTableProperties = ['LanguageVariety', 'Family', 'Area']

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module='StructureDataset')

    def cmd_download(self, args):
        subprocess.check_call(
            'git -C {} submodule update --remote'.format(self.dir.resolve()), shell=True)

    def create_schema(self, ds):
        # values.csv
        ds.remove_columns('ValueTable', 'Language_ID', 'Parameter_ID', 'Code_ID', 'Comment', 'Source')
        ds.add_columns(
            'ValueTable',
            {
                "dc:extent": "singlevalued",
                "datatype": "string",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#languageReference",
                "required": False, # make it optinal for missing entries
                "name": "Language_ID"
            },
            {
                "dc:extent": "singlevalued",
                "datatype": "string",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference",
                "required": True,
                "name": "Inventory_ID"
            },
            *self.valueTableProperties,
        )

        # parameters.csv
        # ds.add_component('ParameterTable')

        # # languages.csv
        ds.add_component('LanguageTable', *self.languageTableProperties)

        # contributions.csv
        ds.add_component('ContributionTable')
        ds.remove_columns('ContributionTable', 'Name', 'Description', 'Citation')
        ds.add_columns(
            'ContributionTable',
            'Glottocode',
            *self.inventoryTableProperties,
        )
        ds.add_foreign_key('ValueTable', 'Inventory_ID', 'ContributionTable', 'ID')

    def cmd_makecldf(self, args):
        self.create_schema(args.writer.cldf)

        # values.csv
        counter = 1
        for row in self.raw_dir.read_csv(
            self.raw_dir / 'tonodb' / 'data' / 'Tonogenesis - Database.csv',
            dicts=True,
        ):
            args.writer.objects['ValueTable'].append({
                'ID': str(counter),
                'Inventory_ID': row['ID'],
                'Language_ID': row['Glottocode'].lstrip('(').rstrip(')').strip(),
                # 'Parameter_ID': str(counter),
                'Value': row['Tone '],
                **{ k: row[k] for k in self.valueTableProperties}
            })

            # parameters.csv
            # args.writer.objects['ParameterTable'].append({
            #     'ID': str(counter),
            #     'Name': row['Phoneme'],
            #     'Description': ' - '.join(unicodedata.name(c) for c in row['Phoneme']), 
            # })

            counter = counter + 1

        # languages.csv
        glangs = {l.id: l for l in args.glottolog.api.languoids()}
        language_ids = list(map(lambda row: row['Language_ID'], args.writer.objects['ValueTable']))
        language_ids = list(dict.fromkeys(language_ids))
        for row in self.raw_dir.read_csv(
            self.raw_dir / 'tonodb' / 'data' / 'languoid.csv',
            dicts=True,
        ):
            if row['id'] in language_ids:
                args.writer.objects['LanguageTable'].append({
                    'ID': row['id'],
                    'Name': row['name'],
                    'Glottocode': row['id'],
                    'ISO639P3code': row['iso639P3code'],
                    'Latitude': row['latitude'],
                    'Longitude': row['longitude'],
                    **(glang_attrs(glangs[row['id']], glangs) if row['id'] in glangs else {}),
                    **{ k: row[k] for k in self.languageTableProperties}
                })

        # contributions.csv
        for row in self.raw_dir.read_csv(
            self.raw_dir / 'tonodb' / 'data' / 'Tonogenesis - Index.csv',
            dicts=True,
        ):
            args.writer.objects['ContributionTable'].append({
                'ID': row['ID'],
                'Contributor': row['Reference'],
                'Glottocode': row['Glottocode'].lstrip('(').rstrip(')').strip(),
                **{ k: row[k] for k in self.inventoryTableProperties}
            })
        
