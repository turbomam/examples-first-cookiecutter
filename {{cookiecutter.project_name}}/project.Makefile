## Add your own custom Makefile targets here

RUN = poetry run

.PHONY: check-jsonschema-example run-linkml-validation check-all-invalid-examples check-all-valid-examples

JSON_SCHEMA_FILE := project/jsonschema/{{cookiecutter.__project_slug}}.schema.json
INVALID_EXAMPLES_DIR := src/data/examples/invalid
INVALID_EXAMPLE_FILES := $(wildcard src/data/examples/invalid/*.yaml)
VALID_EXAMPLES_DIR := src/data/examples/valid
VALID_EXAMPLE_FILES := $(wildcard src/data/examples/valid/*.yaml)

check-all-invalid-examples: $(patsubst $(INVALID_EXAMPLES_DIR)/%.yaml,jsonschema-vs-invalid--%,$(INVALID_EXAMPLE_FILES))

jsonschema-vs-invalid--%: $(JSON_SCHEMA_FILE) $(INVALID_EXAMPLES_DIR)/%.yaml
	! $(RUN) check-jsonschema --schemafile $^

check-all-valid-examples: $(patsubst $(VALID_EXAMPLES_DIR)/%.yaml,jsonschema-vs-valid-%,$(VALID_EXAMPLE_FILES))

jsonschema-vs-valid-%: $(JSON_SCHEMA_FILE) $(VALID_EXAMPLES_DIR)/%.yaml
	$(RUN) check-jsonschema --schemafile $^


run-linkml-validation: {{cookiecutter.__source_path}} \
src/data/examples/invalid/{{cookiecutter.main_schema_class}}Collection-undefined-slot.yaml
	# {{cookiecutter.main_schema_class}}Collection is assumed as the target-class because it has been defined as the tree_root in the schema
	- $(RUN) linkml-validate \
	  --schema $^


src/data/dh_vs_linkml_json/{{cookiecutter.main_schema_class}}Collection_linkml_raw.yaml: src/data/dh_vs_linkml_json/{{cookiecutter.main_schema_class}}_dh.json
	$(RUN) dh-json2linkml \
		--input-file $< \
		--output-file $@ \
		--output-format yaml \
		--key entries

src/data/dh_vs_linkml_json/{{cookiecutter.main_schema_class}}Collection_linkml_normalized.yaml: src/data/dh_vs_linkml_json/{{cookiecutter.main_schema_class}}Collection_linkml_raw.yaml
	$(RUN) linkml-normalize \
		--schema {{cookiecutter.__source_path}} \
		--output $@ \
		--no-expand-all $<

src/data/dh_vs_linkml_json/entries.json: src/data/dh_vs_linkml_json/{{cookiecutter.main_schema_class}}Collection_linkml_normalized.yaml
	$(RUN) linkml-json2dh \
		--input-file $< \
		--input-format yaml \
		--output-dir $(dir $@)
