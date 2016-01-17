import unittest
from library import java_property_file as javaproperties

class TestProperties(unittest.TestCase):

  def test_change(self):
    p=javaproperties.fromStringWithChanges(('key = myvalue\n'),
                                           {'key': 'abc'})

    self.assertEqual(p.prop_dict['key'], 'abc')
    self.assertEqual(p.raw_string, ('key=abc\n'))

  def test_change_should_only_affect_desired_property(self):
    p=javaproperties.fromStringWithChanges(('# comment\n'
                                            'akey = myvalue  \n'
                                            'key = myvalue  \n'),
                                            {'key': 'abc'})

    self.assertEqual(p.prop_dict['akey'], u'myvalue  ')
    self.assertEqual(p.raw_string, (u'# comment\n'
                                    u'akey = myvalue  \n'
                                    u'key=abc\n'))

  def test_multiline_props(self):
    p=javaproperties.fromStringWithChanges(('targetCities=\ \n'
                                            '  Detroit,\ \n'
                                            '  Chicago,\ \n'
                                            '  Los Angeles\n'
                                            '\n'
                                           'a=b\n'),
                                          {'a': 'c'})

    self.assertEqual(p.prop_dict['targetCities'], 'Detroit,Chicago,Los Angeles')
    self.assertEqual(p.raw_string,('targetCities=\ \n'
                                   '  Detroit,\ \n'
                                   '  Chicago,\ \n'
                                   '  Los Angeles\n'
                                   '\n'
                                   'a=c\n'))


if __name__ == '__main__':
  unittest.main()
