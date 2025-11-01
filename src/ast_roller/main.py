import optparse

from ast_roller.grammar import parser, transformer

def main():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('-v', dest='verbose', action='store_true')
    opts, args = opt_parser.parse_args()

    roll_string = " ".join(args) if args else '1d20'

    try:
        parse_tree = parser.parse(roll_string)
        eval_tree = transformer.transform(parse_tree)
        result_tree = eval_tree.evaluate()

        if opts.verbose:
            print(result_tree.pretty_print())
        else:
            print(result_tree.raw_result)

    except Exception as e:
        print(f"Could not process roll string {roll_string}")
        print(f"Error: {e}")