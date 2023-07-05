import click
import pandas as pd
import numpy as np
import math
from pathlib import Path

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:

    df = pd.read_csv("water-leakage.csv")
    df = pd.melt(df, id_vars='Period', var_name='Country', value_name='Observation')
    
    df['Country'] = df['Country'].str.rstrip()
    df.replace({'Country': {'N.Ireland': 'Northern Ireland'}}, inplace=True)
    
    # df['Country'] = df['Country'].apply(lambda x: 'K02000001' if 'UK' in x
    #                                     else ('N92000002' if 'Northern Ireland' in x
    #                                           else ('E92000001' if 'England' in x
    #                                                 else ('S92000003' if 'Scotland' in x
    #                                                       else ('W92000004' if 'Wales' in x else x)))))
        
    df['Marker'] = df.apply(lambda x: 'not available' if np.isnan(x['Observation']) else '', axis=1)
    # df['Observation'] = df.apply(lambda x: None if np.isnan(x['Observation']) else x['Observation'], axis=1)
    
    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()