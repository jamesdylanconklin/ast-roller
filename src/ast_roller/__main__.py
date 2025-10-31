from ast_roller.grammar import parser, transformer
import optparse

def main():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('-v', dest='verbose', action='store_true')
    opts, args = opt_parser.parse_args()

    roll_string = " ".join(args) if args else '1d20'
    parse_tree = parser.parse(roll_string)
    eval_tree = transformer.transform(parse_tree)
    result_tree = eval_tree.evaluate()
  
    if opts.verbose:
        print(result_tree.pretty_print())
    else:
        print(result_tree.raw_result)

if __name__ == "__main__":
  main()