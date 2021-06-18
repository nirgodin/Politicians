from PoliticalShapley import PoliticalShapley
import pandas as pd
import numpy as np

# Define PoliticalShapley module
shap = PoliticalShapley()
shap.add_parties(prty)
shap.add_restrictions(disagree)
shap.run()

