import click
import pandas as pd
import math
from pathlib import Path

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:

    df = pd.read_csv("d7i.csv")
    df['value'] = df['value'].astype(float).round(2)
    df = df.rename(columns={'year': 'Year','trendline': 'Trendline','value': 'Observation'})
    df = df[['Year', 'Trendline','Observation']]  

    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()