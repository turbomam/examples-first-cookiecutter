import csv
import click
import pandas as pd
from linkml.generators.excelgen import ExcelGenerator
from linkml_runtime import SchemaView
from schemasheets.schema_exporter import SchemaExporter


# todo add support for multiple base classes
# todo: add discovery of annotations
# todo modularize this code

@click.command()
@click.option('--meta-path',
              default="https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml",
              help='URL or filesystem path to the LinkML meta model YAML file')
@click.option('--meta-model-excel-file',
              default="meta.xlsx",
              help='Where should a local XLSX representation of the meta model be saved?')
@click.option('--base-class',
              default='slot_definition',
              help="Which class' definition should form the basis of the report?")
@click.option('--columns-to-insert',
              multiple=True,
              default=["slot", "class"],
              help="What LinkML meta slots (that don't appear in the base class) should be added to the report?")
@click.option('--columns-to-remove',
              multiple=True,
              default=["all_members", "all_of", "alt_descriptions", "annotations", "any_of", "enum_range",
                       "exactly_one_of", "extensions", "has_member", "name", "none_of", "path_rule", "range_expression",
                       "structured_aliases", "unit"],
              help='What LinkML meta slots from the base class should be added to the report?')
@click.option('--columns-to-use',
              multiple=True,
              help='Overrides any other determinant of which columns to use in the report.')
@click.option('--source-schema-path',
              required=True,
              help='URL or filesystem path to the schema that will populate the report')
@click.option('--destination-template',
              default='usage_template.tsv',
              help='Where should the template and usage reports TSVs be saved?')
def generate_and_populate_template(source_schema_path: str, meta_path: str, base_class: str, destination_template: str,
                                   columns_to_remove: list, columns_to_insert: list,
                                   meta_model_excel_file: str, columns_to_use: list) -> None:
    """Generate a TSV representation of slot usages in a schema, guided by an XLSX representation of the metamodel.

    Args:
        base_class (str): Name of the selected sheet in the intermediate Excel file, forming the basis of the usage report
        columns_to_insert (list): Columns to insert into the template.
        columns_to_remove (list): Columns to remove from the template.
        columns_to_use (list): Overrides any other determinant of which columns to use in the report
        destination_template (str): Path to the destination template TSV file.
        meta_model_excel_file (str): Where to store the Excel representation of the meta schema.
        meta_path (str): URL or filesystem path to the schema meta model YAML file.
        source_schema_path (str): URL or filesystem path to the source schema file.

    Returns:
        None
    """

    populated_file = destination_template.replace(".tsv", "_populated_raw.tsv")
    useful_file = destination_template.replace(".tsv", "_populated_no_blank_cols.tsv")

    meta_view = SchemaView(meta_path)
    excel_generator = ExcelGenerator(schema=meta_view.schema, output=meta_model_excel_file)
    excel_generator.serialize()

    df = pd.read_excel(meta_model_excel_file, sheet_name=base_class)
    columns_for_template = list(df.columns)

    for column in columns_to_remove:
        if column in columns_for_template:
            columns_for_template.remove(column)

    columns_for_template.sort()

    for column in columns_to_insert:
        columns_for_template.insert(0, column)

    columns_for_template = [x.replace(" ", "_") for x in columns_for_template]
    if len(columns_to_use) > 0:
        columns_for_template = list(columns_to_use)
    second_header_row = columns_for_template.copy()
    second_header_row[0] = f">{second_header_row[0]}"
    sheet = [dict(zip(columns_for_template, second_header_row))]

    with open(destination_template, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns_for_template, delimiter='\t')
        writer.writeheader()
        writer.writerows(sheet)

    exporter = SchemaExporter()
    sv = SchemaView(source_schema_path)
    exporter.export(sv, specification=destination_template, to_file=populated_file)

    populated = pd.read_csv(populated_file, sep='\t')
    populated = populated.iloc[1:]
    populated = populated.dropna(axis=1, how='all')
    populated.to_csv(useful_file, sep='\t', index=False)


if __name__ == '__main__':
    generate_and_populate_template()
