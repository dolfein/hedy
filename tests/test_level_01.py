import hedy
import textwrap
from Tester import HedyTester
from hedy import local_keywords_enabled


class TestsLevel1(HedyTester):
  level = 1

  # tests should be ordered as follows:
  # * commands in the order of hedy.py e..g for level 1: ['print', 'ask', 'echo', 'turn', 'forward']
  # * combined tests
  # * markup tests
  # * negative tests (inc. negative & multilevel)

  # test name conventions are like this:
  # * single keyword positive tests are just keyword or keyword_special_case
  # * multi keyword positive tests are keyword1_keywords_2
  # * negative tests should be
  # * situation_gives_exception



  # print tests
  def test_print(self):
    code = "print Hallo welkom bij Hedy!"
    expected = "print('Hallo welkom bij Hedy!')"

    self.single_level_tester(
      code=code,
      expected=expected,
      output='Hallo welkom bij Hedy!'
    )

  def test_print_has_no_turtle(self):
    result = hedy.transpile_inner("print koekoek", self.level)
    expected = False
    self.assertEqual(expected, result.has_turtle)


  def test_print_with_comma(self):
    code = "print iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is."
    expected = "print('iedereen zegt tegen hem: NERD, omdat hij de slimste van de klas is.')"

    self.single_level_tester(code=code, expected=expected)

  def test_print_multiple_lines(self):
    code = "print Hallo welkom bij Hedy\nprint Mooi hoor"
    expected = "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')"

    self.single_level_tester(code=code, expected=expected)


  def test_print_with_quotes(self):
    code = "print 'Welcome to OceanView!'"

    expected = textwrap.dedent("""\
    print('\\'Welcome to OceanView!\\'')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      output="'Welcome to OceanView!'")
    
  def test_print_with_slashes(self):
    code = "print 'Welcome to \\O/ceanView!'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    print('\\'Welcome to \\\\O/ceanView!\\'')""")

    self.single_level_tester(code=code, expected=expected)

    expected_output = HedyTester.run_code(result)
    self.assertEqual("'Welcome to \\O/ceanView!'", expected_output)
  def test_print_with_slashed_at_end(self):
    code = "print Welcome to \\"

    expected = textwrap.dedent("""\
    print('Welcome to \\\\')""")

    self.single_level_tester(
      code=code,
      expected=expected,
      output="Welcome to \\"
    )
    
  def test_print_with_spaces(self):
    code = "print        hallo!"
    expected = textwrap.dedent("""\
    print('hallo!')""")

    self.single_level_tester(code=code, expected=expected)
    
  if local_keywords_enabled:
    def test_print_dutch(self):
      result = hedy.transpile("print Hallo welkom bij Hedy!", self.level, lang="nl")
      expected = "print('Hallo welkom bij Hedy!')"
      self.assertEqual(expected, result.code)
      self.assertEqual(False, result.has_turtle)
      self.assertEqual('Hallo welkom bij Hedy!', HedyTester.run_code(result))
    def test_ask_dutch_error(self):
      code = textwrap.dedent("""ask Heb je er zin?""")

      with self.assertRaises(hedy.exceptions.ParseException) as context:
        result = hedy.transpile(code, self.level, lang="nl")
      self.assertEqual('Parse', context.exception.error_code)
      self.assertEqual(1, context.exception.error_location[0])
      self.assertEqual('?', context.exception.error_location[1])

  # ask tests
  def test_ask(self):
    code = "ask wat is je lievelingskleur?"
    expected = "answer = input('wat is je lievelingskleur?')"
    self.single_level_tester(code=code, expected=expected)

  def test_ask_Spanish(self):
    result = hedy.transpile("ask ask Cuál es tu color favorito?", self.level)
    expected = "answer = input('ask Cuál es tu color favorito?')"
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_ask_with_quotes(self):
    code = "ask 'Welcome to OceanView?'"
    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    answer = input('\\'Welcome to OceanView?\\'')""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  # echo tests
  def test_echo_without_argument(self):
    result = hedy.transpile("ask wat?\necho", self.level)
    expected = "answer = input('wat?')\nprint(answer)"
    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)
  def test_echo_with_quotes(self):
    code = textwrap.dedent("""\
    ask waar?
    echo oma's aan de""")

    result = hedy.transpile(code, self.level)

    expected = textwrap.dedent("""\
    answer = input('waar?')
    print('oma\\'s aan de '+answer)""")

    self.assertEqual(expected, result.code)
    self.assertEqual(False, result.has_turtle)

  # forward tests
  def test_forward(self):
    code = "forward 50"
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)""")
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_without_argument(self):
    code = textwrap.dedent("""forward""")
    expected = textwrap.dedent("""\
       t.forward(50)
       time.sleep(0.1)""")

    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_forward_with_text_gives_type_error(self):
    code = "forward lalalala"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException,
      extra_check_function=self.is_turtle()
    )

  def test_multiple_forward_without_arguments(self):
    result = hedy.transpile("forward\nforward", self.level)
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.forward(50)
    time.sleep(0.1)""")
    self.assertEqual(expected, result.code)
    self.assertEqual(True, result.has_turtle)

  # turn tests
  def test_turn_no_args(self):
    code = "turn"
    expected = "t.right(90)"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_one_turn_right(self):
    code = "turn right"
    expected = "t.right(90)"

    self.single_level_tester(code=code, expected=expected,
                             extra_check_function=self.is_turtle())

  def test_one_turn_left(self):
    code = "turn left"
    expected = "t.left(90)"

    self.single_level_tester(code=code, expected=expected,
                             extra_check_function=self.is_turtle())


  def test_turn_number(self):
    code = "turn 180"
    expected = "t.right(180)"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  def test_one_turn_with_text_gives_type_error(self):
    code = "turn koekoek"
    self.multi_level_tester(
      max_level=self.max_turtle_level,
      code=code,
      exception=hedy.exceptions.InvalidArgumentTypeException
    )

  # comment test
  def test_comment(self):
    code = "# geen commentaar, helemaal geen!"
    expected = "# geen commentaar, helemaal geen!"
    self.multi_level_tester(
      code=code,
      expected=expected
    )

  # combined keywords tests
  def test_print_ask_echo(self):
      code = textwrap.dedent("""\
      print Hallo
      ask Wat is je lievelingskleur
      echo je lievelingskleur is""")

      expected = textwrap.dedent("""\
      print('Hallo')
      answer = input('Wat is je lievelingskleur')
      print('je lievelingskleur is '+answer)""")

      self.single_level_tester(code=code, expected=expected,
                               extra_check_function=self.is_not_turtle())
  def test_forward_turn_combined(self):
    code = "forward 50\nturn\nforward 100"
    expected = textwrap.dedent("""\
    t.forward(50)
    time.sleep(0.1)
    t.right(90)
    t.forward(100)
    time.sleep(0.1)""")
    self.multi_level_tester(
      max_level=7,
      code=code,
      expected=expected,
      extra_check_function=self.is_turtle()
    )

  # markup tests
  def test_lines_may_end_in_spaces(self):
    code = "print Hallo welkom bij Hedy! "
    expected = "print('Hallo welkom bij Hedy! ')"
    self.single_level_tester(code=code, expected=expected,
                             extra_check_function=self.is_not_turtle(),
                             output='Hallo welkom bij Hedy!')

  # negative tests
  def test_lines_with_space_gives_invalid(self):
    code = " print Hallo welkom bij Hedy! "
    self.single_level_tester(code=code, exception=hedy.exceptions.InvalidSpaceException,
                             extra_check_function=self.is_not_turtle())

  def test_lines_with_spaces_gives_invalid(self):
    code = " print Hallo welkom bij Hedy!\n print Hallo welkom bij Hedy!"
    self.single_level_tester(code=code, exception=hedy.exceptions.InvalidSpaceException,
                             extra_check_function=self.is_not_turtle())

  def test_word_plus_period_gives_invalid(self):
    with self.assertRaises(hedy.exceptions.InvalidCommandException) as context:
      result = hedy.transpile("word.", self.level)
    self.assertEqual('Invalid', context.exception.error_code)
  def test_empty_gives_exception(self):
    with self.assertRaises(hedy.exceptions.EmptyProgramException) as context:
      result = hedy.transpile("", self.level)
  def test_non_keyword_gives_Invalid(self):
    with self.assertRaises(hedy.exceptions.InvalidCommandException) as context:
      result = hedy.transpile("groen", self.level)
    self.assertEqual('Invalid', context.exception.error_code)
  def test_lonely_echo_gives_LonelyEcho(self):
    code = "echo wat dan?"
    with self.assertRaises(hedy.exceptions.LonelyEchoException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Lonely Echo', context.exception.error_code)
  def test_echo_before_ask_gives_LonelyEcho(self):
    code = textwrap.dedent("""\
    echo what can't we do?
    ask time travel """)
    with self.assertRaises(hedy.exceptions.LonelyEchoException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Lonely Echo', context.exception.error_code)
  def test_newlines_only_gives_EmptyProgram(self):
    code = textwrap.dedent("""\
    """)
    with self.assertRaises(hedy.exceptions.EmptyProgramException) as context:
      result = hedy.transpile(code, self.level)
    self.assertEqual('Empty Program', context.exception.error_code)
  def test_incomplete_gives_Incomplete(self):
    with self.assertRaises(hedy.exceptions.IncompleteCommandException) as context:
      result = hedy.transpile("print", self.level)
    self.assertEqual('Incomplete', context.exception.error_code)
  def test_incomplete_on_line_2_gives_Incomplete(self):
    with self.assertRaises(hedy.exceptions.IncompleteCommandException) as context:
      result = hedy.transpile("print lalalala\nprint", self.level)
    self.assertEqual('Incomplete', context.exception.error_code)
    self.assertEqual('print', str(context.exception.arguments['incomplete_command']))
  def test_print_without_argument_gives_incomplete(self):
    self.multi_level_tester(
      max_level=22,
      code="print",
      exception=hedy.exceptions.IncompleteCommandException
    )
  def test_non_keyword_with_argument_gives_invalid(self):
    self.multi_level_tester(
      max_level=10,
      code="abc felienne 123",
      exception=hedy.exceptions.InvalidCommandException
    )

  # def test_other_2(self):
  #   with self.assertRaises(Exception) as context:
  #     result = hedy.transpile("abc felienne 123", self.level)
  #   self.assertEqual(str(context.exception), 'Invalid')
  #   self.assertEqual(str(context.exception.arguments),
  #                    "{'invalid_command': 'abc', 'level': 1, 'guessed_command': 'ask'}")

