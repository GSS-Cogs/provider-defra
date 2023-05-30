import click
import pandas as pd
import math
from pathlib import Path

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output", default=Path("./output.csv"), type=click.Path(path_type=Path))
def wrangle(input: Path(), output: Path()) -> None:

    df1 = pd.read_csv("b3a.csv")
    df2 = pd.read_csv("b3b.csv")
    df3 = pd.read_csv("b3c.csv")

    df = pd.concat([df1, df2, df3], axis=0, ignore_index=True, sort=False)

    df["Year"] = df["variable"].str.extract(r"(\d+)")
    df["Year"] = df["Year"].str.extract(r"(\d+)")
    df["variable"] = df["variable"].str.extract(r"([^(\d+)]+)")
    df = df.fillna("")

    df["Year"] = df.apply(
    lambda x: "2019"
    if x["variable"] == "" and x["site"] == ""
    else (
        "2019"
        if "(2019)" in x["site"]
        else "2022"
        if "(2022)" in x["site"]
        else x["Year"]
    ),
    axis=1,
    )
    df["Year"] = df.apply(lambda x: "year/" + x["Year"], axis=1)

    df["Region"] = "E92000001"
    df["Measure Type"] = df.apply(
    lambda x: "status-of-surface-waters"
    if x["variable"] == "" and x["site"] == ""
    else "status-of-ground-waters"
    if x["site"] == ""
    else "status-of-waters-specially-protected-for-specific-uses"
    if x["variable"] == ""
    else "Measure",
    axis=1,
    )
    df["Unit"] = df.apply(
    lambda x: "percentage-of-area"
    if x["site"]
    else "percentage-of-water-bodies-assessed",
    axis=1,
    )

    df["site"] = df["site"].str.extract(r"([^(\d+)]+)")
    df = df.fillna("")
    df = df.rename(columns={"Year": "Period", "status": "Status", "percentage": "Value"})

    df["Environment Surveyed"] = df.apply(
    lambda x: x["water_body"]
    if x["variable"] == "" and x["site"] == ""
    else x["variable"]
    if x["water_body"] == "" and x["site"] == ""
    else x["site"]
    if x["water_body"] == "" and x["variable"] == ""
    else "",
    axis=1,
    )

    df = df.drop(['water_body', 'variable', 'site'], axis = 1)
    df = df[['Period', 'Region', 'Environment Surveyed', 'Status', 'Measure Type', 'Unit', 'Value']]

    df.to_csv(output, index=False)
    return

if __name__ == "__main__":
    wrangle()