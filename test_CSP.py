import unittest
unittest.TestLoader.sortTestMethodsUsing = None
from CSP import CSP

class TestCSP(unittest.TestCase):
  
  def setUp(self):
    # CSP_1
    self.csp_1 = CSP()
    self.csp_1.extract_data_from_file("example1.txt")
    self.functions_1 = [self.csp_1.L_shape_1, self.csp_1.L_shape_2, self.csp_1.L_shape_3, self.csp_1.L_shape_4, self.csp_1.Full_block, self.csp_1.Outer_block]
    
    # CSP_2
    self.csp_2 = CSP()
    self.csp_2.extract_data_from_file("example2.txt")
    self.functions_2 = [self.csp_2.L_shape_1, self.csp_2.L_shape_2, self.csp_2.L_shape_3, self.csp_2.L_shape_4, self.csp_2.Full_block, self.csp_2.Outer_block]
   
  def tearDown(self):
    self.csp_1 = None
    self.csp_2 = None
    self.functions_1 = None
    self.functions_2 = None 

  # check if the path is found at all
  def test_csp_with_MRV_1(self):
    self.assertTrue(self.csp_1.csp_with_MRV(0, {1:0, 2:0, 3:0, 4:0}, self.functions_1))
  
  def test_csp_with_MRV_2(self):
    self.assertTrue(self.csp_2.csp_with_MRV(0, {1:0, 2:0, 3:0, 4:0}, self.functions_2))
  
  #check if the number of bushes in final state matches the target
  def test_apply_path_to_landscape_1(self):
    self.csp_1.csp_with_MRV(0, {1:0, 2:0, 3:0, 4:0}, self.functions_1)
    self.assertEqual(self.csp_1.apply_path_to_landscape(), self.csp_1.bushes_target)

  def test_apply_path_to_landscape_2(self):
    self.csp_2.csp_with_MRV(0, {1:0, 2:0, 3:0, 4:0}, self.functions_2)
    self.assertEqual(self.csp_2.apply_path_to_landscape(), self.csp_2.bushes_target)
  
    
if __name__ == '__main__':
  unittest.main()