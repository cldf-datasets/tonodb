import pathlib
import subprocess
import hashlib
from cldfbench import Dataset as BaseDataset
from cldfbench import CLDFSpec
try:
    from pytular.util import fetch_sheet
except ImportError:
    fetch_sheet = None


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
    # valueTableProperties = ['LanguageVariety', 'TriggeringContext' , 'Extra', 'Height', 'Contour', 'Phonation', 'ToneDescription', 'ChaoNumerals', 'Notes', 'EffectOnPitch', 'ResultantSystem', 'Type', 'Onset', 'Coda', 'Stress/quantity', 'Wordtype', 'long vowel']
    # valueTableProperties = ['LanguageVariety', 'TriggeringContext', 'Extra', 'Height', 'Contour', 'Phonation', 'ToneDescription' , 'ChaoNumerals', 'Notes', 'EffectOnPitch', 'ResultantSystem', 'Type', 'Onset', 'OnsetManner', 'OnsetVoicing', 'OnsetAspiration', 'Coda', 'CodaPhonation', 'CodaGlottal', 'CodaManner', 'Stress/quantity', 'NucleusATR', 'NucleusLength', 'NucleusHeight', 'Wordtype', 'Nucleus']
    valueTableProperties = ['LanguageVariety', 'Ordering', 'Ongoing', 'TriggeringContext', 'Tone ', 'Extra', 'Height', 'Contour', 'Phonation', 'ToneDescription', 'ChaoNumerals', 'RestrictedEnviroment', 'Notes', 'EffectOnPitch', 'ResultantSystem', 'Type', 'Onset', 'OnsetManner', 'OnsetVoicing', 'OnsetAspiration', 'Coda', 'CodaPhonation', 'CodaGlottal', 'CodaManner', 'Stress', 'SyllableCount', 'NucleusATR', 'NucleusLength', 'NucleusHeight', 'Nucleus']
    languageTableProperties = ['family_id', 'parent_id', 'bookkeeping', 'level', 'description', 'markup_description', 'child_family_count', 'child_language_count', 'child_dialect_count', 'country_ids']
    inventoryTableProperties = ['LanguageVariety', 'Family', 'Area', 'Notes', 'BibTex']

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module='StructureDataset')

    def cmd_download(self, args):
        subprocess.check_call(
            'git -C {} submodule update --remote'.format(self.dir.resolve()), shell=True)

    def create_schema(self, ds):
        # values.csv
        ds.remove_columns('ValueTable', 'Language_ID', 'Code_ID', 'Comment', 'Source')
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
        ds.add_component('ParameterTable')
        ds.remove_columns('ParameterTable', 'Description')

        # # languages.csv
        ds.add_component('LanguageTable', *self.languageTableProperties)

        # contributions.csv
        ds.add_component('ContributionTable')
        ds.remove_columns('ContributionTable', 'Name', 'Description')
        ds.add_columns(
            'ContributionTable',
            'Glottocode',
            *self.inventoryTableProperties,
        )
        ds.add_foreign_key('ValueTable', 'Inventory_ID', 'ContributionTable', 'ID')

    def cmd_makecldf(self, args):
        self.create_schema(args.writer.cldf)

        indexToLanguageID = {}
        # contributions.csv
        for row in self.raw_dir.read_csv(
            self.raw_dir / 'tonodb' / 'data' / 'Tonogenesis - Index.csv',
            dicts=True,
        ):
            args.writer.objects['ContributionTable'].append({
                'ID': row['ID'],
                'Citation': 'Lilja Saeboe, Alena Witzlack, Eitan Grossman, & Steven Moran. 2021. TonoDB: a database of tonogenesis events.',
                'Contributor': 'Lilja Saeboe',
                'Glottocode': row['Glottocode'],
                **{ k: row[k] for k in self.inventoryTableProperties}
            })
            indexToLanguageID[row['ID']] = row['Glottocode']

        tone_list = []
        counter = 1
        for row in self.raw_dir.read_csv(
            self.raw_dir / 'tonodb' / 'data' / 'Tonogenesis - Database.csv',
            dicts=True,
        ):
            tone = row['Tone ']
            tone_id = hashlib.md5(tone.encode('utf8')).hexdigest().upper()

            # values.csv
            args.writer.objects['ValueTable'].append({
                'ID': str(counter),
                'Inventory_ID': row['ID'],
                'Language_ID': indexToLanguageID[row['ID']] if row['ID'] in indexToLanguageID else None,
                'Parameter_ID': tone_id,
                'Value': tone,
                **{ k: row[k] for k in self.valueTableProperties}
            })

            # parameters.csv
            if tone not in tone_list:
                args.writer.objects['ParameterTable'].append({
                    'ID': tone_id,
                    'Name': tone,
                })

            tone_list.append(tone)
            counter = counter + 1

        # languages.csv
        glangs = {l.id: l for l in args.glottolog.api.languoids()}
        language_ids = list(map(lambda row: row['Glottocode'], args.writer.objects['ContributionTable']))
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
        
