import sys
from eval import eval_statement
from textx import metamodel_from_file


if __name__ == "__main__":
    rules = sys.argv[1] if len(sys.argv) >= 2 else ''

    grammar_path = sys.argv[2] if len(sys.argv) >= 3 else 'grammar.tx'

    meta_model = metamodel_from_file(grammar_path)
    model = meta_model.model_from_str(rules)

    if type(model) != str and model.statements is not None:
        for statement in model.statements:
            eval_statement(statement)
