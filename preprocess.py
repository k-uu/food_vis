import pandas as pd
import numpy as np

def load_dataset(file_path):
    return pd.read_csv(file_path, na_values="..")

greenhouse = load_dataset("raw_data.csv")

# Tomatoes include special tomatoes:
greenhouse['Tomatoes'] -= greenhouse['Special tomatoes'].fillna(0)

# Combine Lettuce subcategories into one:
greenhouse['Lettuces'] = greenhouse[['Butter-head lettuce',
                                     'Crisphead lettuce']].sum(axis=1, min_count=1)


greenhouse = greenhouse.drop(columns=['Special tomatoes',
                                      'Butter-head lettuce',
                                      'Crisphead lettuce',
                                      ])
# Drop the TOTALS also
greenhouse = greenhouse.drop(columns=['Region',
                                      'TOTAL (vegetables)',
                                      'TOTAL (berries)',
                                      ])

idx_cols = ['Year']

gh_yield = greenhouse.loc[greenhouse['Information'] == 'Yield (1,000 kg)'].drop(columns='Information').set_index(idx_cols)
gh_area = greenhouse.loc[greenhouse['Information'] == 'Area of greenhouses (1,000 m²)'].drop(columns='Information').set_index(idx_cols)

# replace area of 0 with nan so that result remains Nan (missing/ignored)
gh_eff = (gh_yield / gh_area.replace(0, np.nan))

crops = gh_eff.columns

gh_eff = gh_eff.reset_index().melt(id_vars='Year', 
                          var_name='Crop', 
                          value_name='Productivity')

gh_yield = gh_yield.reset_index().melt(id_vars='Year', 
                                  var_name='Crop', 
                                  value_name='Yield')

area = gh_area.reset_index().melt(id_vars='Year', 
                                  var_name='Crop', 
                                  value_name='Area')

gh_eff = gh_eff.merge(gh_yield, on=['Year', 'Crop']).merge(area, on=['Year', 'Crop'])

gh_eff.to_csv('gh_yields_s.csv', index=False)