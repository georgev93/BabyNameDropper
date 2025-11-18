import argparse
import requests
import zipfile
import io
import csv
from pathlib import Path
from typing import List, Literal

NamesWithCounts = List[tuple[str, int]]
Gender = Literal['M', 'F']


def parse_args() -> argparse.Namespace:
    """
    The standard ArgumentParser argument parse, but wrapped in a function

    Returns:
    A namespace containing the parsed args
        
    """
    parser = argparse.ArgumentParser(
        description=(
            "Use Social Security Administration data on recent baby "
            "names to generate a fillable form to record preference of those names"
        )
    )
    parser.add_argument(
        "--gender",
        required=True,
        choices=["M", "F"],
        help="Filter by gender (M=Male, F=Female)",
    )
    parser.add_argument("--input", help="Use existing CSV file instead of downloading")
    parser.add_argument(
        "--limit", type=int, help="Limit number of results (default: use all)"
    )
    return parser.parse_args()


def trim_csv_to_limit(csvfile: Path, gender: Gender, count_limit:int =0) -> NamesWithCounts:
    """
    Trims an input CSV to a given input limit as well as downselects by gender.

    Args:
        csvfile (str): Path to a CSV file
        gender (Gender): "M" or "F"
        count_limit (int): Number of names to return (0: returns all names)

    Returns:
       NamesWithCounts: List of names with the number of children named with this name in the given year 
    """
    names: list[tuple[str, int]] = []
    with open(csvfile) as f:
        for row in csv.reader(f):
            if row[1] == gender:
                names.append((row[0], int(row[2])))

    names.sort(key=lambda x: x[1], reverse=True)
    if count_limit:
        names = names[:count_limit]

    names.sort(key=lambda x: x[0])

    return names


def generate_output_csv(namelist: NamesWithCounts, output_file: str ='namelist.csv'):
    """
    Generates an output CSV, ready to be filled in "tally" style

    Args:
        namelist (NamesWithCounts): A list of names with the number of children named with this name in the given year
        output_file (str): Where to save the output file
    """
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['Name', 'Maybe', 'Yes'])

        for name in namelist:
            writer.writerow([name[0], '', ''])


def get_names(gender: Gender, input_file: str="", limit: int =0):
    """
    Fetches baby names (male, or female) of babies named in the past year along with a count of how many babies were named that name that year.

    Args:
        gender (Gender): "M" or "F" 
        input_file (str): A pre-downloaded list of names/counts to avoid fetching from online or using the cache
        limit (int): Limit the output CSV to a number of names (0: no limit)
    """
    # Define output file name for caching
    cache_dir = Path('cache')
    cache_dir.mkdir(exist_ok=True)
    cache_file = Path(f"{cache_dir}/names_{gender}.csv")

    # Use input file if provided
    if input_file and Path(input_file).exists():
        source_file = Path(input_file)
    # Use cache if it exists
    elif cache_file.exists():
        source_file = cache_file
    # Download and extract if neither exists
    else:
        print("Downloading data from SSA...")
        try:
            response = requests.get("https://www.ssa.gov/oact/babynames/names.zip")
            response.raise_for_status()

            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                # Get most recent year's file
                newest_file = max(f for f in z.namelist() if f.startswith("yob"))
                print("Using most recent year: " + newest_file[3:7])

                # Extract and save as cache file
                with z.open(newest_file) as src, open(
                    cache_file, "w", newline=""
                ) as dst:
                    dst.writelines([line.decode() for line in src])

                source_file = cache_file
                print(f"Data saved to {cache_file}")
        except Exception as e:
            print(f"Error downloading or processing data: {e}")
            return []

    # Read and process the data
    names = trim_csv_to_limit(source_file, gender, limit)

    if not names:
        print("No names found!")
        return

    # Generate output csv
    generate_output_csv(names)
    print("Generated list of " + str(len(names)) + " at namelist.csv")


def main():
    args = parse_args()
    get_names(args.gender, args.input, args.limit)


if __name__ == "__main__":
    main()
