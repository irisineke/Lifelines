'''
Dit bestand test 3 functies uit `app.py`. Namelijk:
`read_config`, `widget_scatter` en `scatterplot_body`.
'''

import unittest
import panel as pn
import pandas as pd
import app


class TestApp(unittest.TestCase):
    '''
    test op 3 functies uit app.py
    '''
    def test_read_config(self):
        '''
        test of functie `read_config` van `app.py` het config file goed inleest.
        : param, self, Self@TestApp
        '''
        # config lezen:
        data, metadata, height, width, var_list, groupby_list = app.read_config()

        # de test:
        self.assertEqual(data, '../Dataset/betere_namen/Lifelines_Public_Health_dataset_2024.csv')
        self.assertEqual(metadata, 'metadata.txt')
        self.assertEqual(height, 350)
        self.assertEqual(width, 350)
        self.assertEqual(var_list, ('BIRTHYEAR', 'AGE_T1', 'AGE_T2', 'AGE_T3', 'ZIP_CODE',
       'BMI_T1', 'WEIGHT_T1', 'HIP_T1', 'HEIGHT_T1', 'WAIST_T1', 'BMI_T2',
       'WEIGHT_T2', 'HIP_T2', 'HEIGHT_T2', 'WAIST_T2', 'HEIGHT_T3',
       'WEIGHT_T3', 'HIP_T3', 'WAIST_T3', 'FINANCE_T1', 'DBP_T1', 'DBP_T2',
       'HBF_T1', 'HBF_T2', 'MAP_T1', 'MAP_T2', 'SBP_T1', 'SBP_T2', 'CHO_T1',
       'GLU_T1', 'CHO_T2', 'GLU_T2', 'LLDS', 'SUMOFALCOHOL', 'SUMOFKCAL', 'MWK_VAL',
       'SCOR_VAL', 'MWK_NO_VAL', 'SCOR_NO_VAL', 'PREGNANCIES', 'C_SUM_T1', 'A_SUM_T1',
       'SC_SUM_T1', 'I_SUM_T1', 'E_SUM_T1', 'SD_SUM_T1', 'V_SUM_T1',
       'D_SUM_T1', 'NSES_YEAR', 'NSES', 'NEIGHBOURHOOD1_T2', 'NEIGHBOURHOOD2_T2',
       'NEIGHBOURHOOD3_T2', 'NEIGHBOURHOOD4_T2', 'NEIGHBOURHOOD5_T2',
       'NEIGHBOURHOOD6_T2', 'MENTAL_DISORDER_T1', 'MENTAL_DISORDER_T2'))
        self.assertEqual(groupby_list, ('GENDER','EDUCATION_LOWER_T1',
       'EDUCATION_LOWER_T2', 'WORK_T1', 'WORK_T2',
       'LOW_QUALITY_OF_LIFE_T1', 'LOW_QUALITY_OF_LIFE_T2',
       'HTN_MED_T1', 'RESPIRATORY_DISEASE_T1', 'SMOKING', 'METABOLIC_DISORDER_T1',
       'METABOLIC_DISORDER_T2', 'SPORTS_T1',
       'CYCLE_COMMUTE_T1', 'VOLUNTEER_T1', 'OSTEOARTHRITIS',
       'BURNOUT_T1', 'DEPRESSION_T1', 'SLEEP_QUALITY', 'DIAG_CFS_CDC',
       'DIAG_FIBROMYALGIA_ACR', 'DIAG_IBS_ROME3', 'NEIGHBOURHOOD1_T2', 'NEIGHBOURHOOD2_T2',
       'NEIGHBOURHOOD3_T2', 'NEIGHBOURHOOD4_T2', 'NEIGHBOURHOOD5_T2',
       'NEIGHBOURHOOD6_T2', 'MENTAL_DISORDER_T1', 'MENTAL_DISORDER_T2'))

    def test_widget_scatter(self):
        '''
        test of functie `widget_scatter` van `app.py` de juiste widgets aanmaakt.
        : param, self, Self@TestApp
        '''
        # tijdelijk makkelijke lists aanmaken:
        var_list = ['var1', 'var2', 'var3']
        groupby_list = ['group1', 'group2', 'group3']

        # de test:
        widget_scatter_first, widget_scatter_second, widget_groupby_scat, switch_button = app.widget_scatter(var_list, groupby_list)
        self.assertIsInstance(widget_scatter_first, pn.widgets.Select)
        self.assertIsInstance(widget_scatter_second, pn.widgets.Select)
        self.assertIsInstance(widget_groupby_scat, pn.widgets.Select)
        self.assertIsInstance(switch_button, pn.widgets.Checkbox)


    def test_scatterplot_body(self):
        '''
        test of functie `scatterplot_body` van `app.py` een output geeft.
        : param, self, Self@TestApp
        '''
        # tijdelijke data en widget info aanmaken:
        data = pd.DataFrame({
            'var1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'var2': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            'group1': ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c', 'c']
        })
        widget_scatter_first = 'var1'
        widget_scatter_second = 'var2'
        widget_groupby_scat = 'group1'
        switch_button = False

         # de test:
        result = app.scatterplot_body(data, widget_scatter_first, widget_scatter_second,
                                      widget_groupby_scat, switch_button)
        self.assertTrue(result is not None)


if __name__ == '__main__':
    unittest.main()
