from email.policy import default
import click
import pandas as pd
from pathlib import Path

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:

    df = pd.read_csv(input, na_values="na")
    df.rename(columns={'year': 'Year', 'status': 'Status of salmon rivers', 'percentage': 'Observation'}, inplace=True)
    df['Observation'] = df['Observation'].astype(float).round(2)

    df = df[['Year', 'Status of salmon rivers', 'Observation']]
    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()