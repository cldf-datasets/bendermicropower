from pathlib import Path
import pylexibank
from clldutils.misc import slug


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "bendermicropower"

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"},
        separators=";/,",
        missing_data=("?", "-"),
        strip_inside_brackets=True,
    )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("1a_dat_MicPowNum_2021_04.csv", dicts=True, delimiter=";")

        concept_lookup = args.writer.add_concepts(
            id_factory=lambda x: x.id.split("-")[-1] + "_" + slug(x.gloss), lookup_factory="Name"
        )

        for row in data:
            args.writer.add_language(ID=row["lang_ID"], Glottocode=row["lang_ID"])

            for k, v in concept_lookup.items():
                if row[k]:
                    args.writer.add_form(
                        Value=row[k], Form=row[k], Language_ID=row["lang_ID"], Parameter_ID=v
                    )
