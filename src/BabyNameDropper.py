import argparse
import requests
import zipfile
import io
import csv
from pathlib import Path


def parse_args():
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


def trim_csv_to_limit(csvfile, gender, count_limit=0):
    names = []
    with open(csvfile) as f:
        for row in csv.reader(f):
            if row[1] == gender:
                names.append((row[0], int(row[2])))

    names.sort(key=lambda x: x[1], reverse=True)
    if count_limit:
        names = names[:count_limit]

    names.sort(key=lambda x: x[0])

    return names


def generate_output_csv(namelist, output_file='namelist.csv'):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['Name', 'Maybe', 'Yes'])

        for name in namelist:
            writer.writerow([name[0], '', ''])


def get_names(gender, input_file=None, limit=None):
    # Define output file name for caching
    cache_dir = Path('cache')
    cache_dir.mkdir(exist_ok=True)
    cache_file = Path(f"{cache_dir}/names_{gender}.csv")

    # Use input file if provided
    if input_file and Path(input_file).exists():
        source_file = input_file
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

    # Generate output csv
    generate_output_csv(names)
    print("Generated list of " + str(len(names)) + " at namelist.csv")

    return names


def main():
    args = parse_args()
    names = get_names(args.gender, args.input, args.limit)

    if not names:
        print("No names found!")
        return


if __name__ == "__main__":
    main()
