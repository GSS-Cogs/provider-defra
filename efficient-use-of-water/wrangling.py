import click
import pandas as pd
import math
from pathlib import Path

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:

    df = pd.read_csv("water-leakage.csv").fillna('0')

    df = pd.melt(df, id_vars=['Period'])

    df.rename(columns={'variable': 'Countries',
                'value': 'Observation'}, inplace=True)
    
    df['Observation'] = df['Observation'].astype(str).astype(float)
    
    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()