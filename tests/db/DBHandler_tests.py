import unittest
from apps.db.DBHandler import DBHandler


dbh = DBHandler()


class TestGetMemberId(unittest.TestCase):
    """
    Test accurate return of MOC IDs
    """
    '''
    def test_nancy_pelosi(self):
        member_id = dbh.get_mem_id_by_name('Pelosi', 'Nancy')
        print(member_id)
        self.assertEqual(member_id, 'P000197')
    
    # His dad is no longer in office
    def test_donald_payne_jr(self):
        member_id = dbh.get_mem_id_by_name('Payne', 'Donald')
        self.assertEqual(member_id, 'P000604')

    def test_donald_payne_sr(self):
        member_id = dbh.get_mem_id_by_region('Payne', 'NJ', 111, 10)
        self.assertEqual(member_id, 'P000149')

    def test_me(self):
        member_id = dbh.get_mem_id_by_name('Wolfe', 'Lauren')
        self.assertIsNone(member_id)
    '''

if __name__ == '__main__':
    unittest.main()
