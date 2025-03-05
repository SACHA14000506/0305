import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--solvers",
                metavar="solvers[latest solver, earlier solver1,...]",
                action="store",
                # type = str,
                dest="solvers",
                # default=['z3-4.13.4', 'z3-4.13.3', 'z3-4.13.2'],
                default = ['z3-4.8.9', 'z3-4.8.8', 'z3-4.8.7'],

                # default=['cvc5-1.2.0', 'cvc5-1.1.2', 'cvc5-1.1.1'],
                nargs='+',
                help="The target SMT Solvers for SPRFinder.py.",
                # required=True
)
parser.add_argument("-t", "--type",
                metavar="z3seq, z3str3 or cvc4",
                action="store",
                type = str,
                dest='type',
                default='z3seq',
                # default='cvc5',
                # default='z3str3',
               # nargs=1,
                help="The type of the solver.",
                # required=True
)

parser.add_argument('-l', '--string_length',
                    metavar="-l length_of_string",
                    action="store",
                    type = int,
                    dest="length",
                    default=10,
                    help="The init max string length"
                    )

parser.add_argument('-v', '--var_num',
                    metavar="variable_number",
                    action="store",
                    type = int,
                    dest="var_num",
                    default=3,
                    help="The init max variable number"
                    )
parser.add_argument('-a', '--assert_num',
                    metavar="number_of_assertion",
                    action="store",
                    type = int,
                    dest="assert_num",
                    default=4,
                    help="The init max assert number"
                    )
parser.add_argument('-d', '--max_depth',
                    metavar="init_depth",
                    action="store",
                    type = int,
                    dest="depth",
                    default=3,
                    help="The init max depth"
                    )

parser.add_argument('-T', '--time_out',
                    metavar='time_out',
                    action='store',
                    dest='timeout',
                    default=20,
                    help='The timeout setting'
                    )
# parser.add_argument()
args = parser.parse_args()
