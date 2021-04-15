from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomLanguage(pylexibank.Language):
    lang_Var = attr.ib(default=None)
    lang_Br = attr.ib(default=None)
    comm_Source = attr.ib(default=None)
    Orth = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "bendermicropower"
    language_class = CustomLanguage

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"}, separators="/", missing_data=("?",), strip_inside_brackets=False,
    )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("1a_dat_MicPowNum_2021_04b_commForms.csv", dicts=True)
        args.writer.add_sources()

        concept_lookup = args.writer.add_concepts(
            id_factory=lambda x: x.id.split("-")[-1] + "_" + slug(x.gloss), lookup_factory="Name"
        )

        for row in data:
            args.writer.add_language(
                ID=row["ID"],
                Glottocode=row["lang_Code"],
                Name=row["lang_Name"],
                lang_Var=row["lang_Var"],
                lang_Br=row["lang_Br"],
                Orth=row["Orth"],
                comm_Source=row["comm_Source"],
            )

            for conc_gloss, conc_id in concept_lookup.items():
                comment = ""

                for com in row["comm_Forms"].split(";"):
                    if row[conc_gloss] in com:
                        comment = com.lstrip()

                if row[conc_gloss]:
                    args.writer.add_forms_from_value(
                        Value=row[conc_gloss],
                        Language_ID=row["ID"],
                        Parameter_ID=conc_id,
                        Source=row["source_Key"],
                        Comment=comment,
                    )
