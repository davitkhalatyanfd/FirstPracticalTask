import csv
import math
import time
import pandas as pd

def parse_tsv(file_path):
    """Parses the TSV file and returns the data as a list of dictionaries."""
    stars = pd.read_csv(file_path, sep='\t', skiprows=1)
    return stars

def calculate_distance(ra1, dec1, ra2, dec2):
    """Calculates the angular distance between two points in equatorial coordinates."""
    ra1, dec1, ra2, dec2 = map(math.radians, [ra1, dec1, ra2, dec2])
    delta_ra = ra1 - ra2
    delta_dec = dec1 - dec2
    a = math.sin(delta_dec / 2) ** 2 + math.cos(dec1) * math.cos(dec2) * math.sin(delta_ra / 2) ** 2
    return 2 * math.asin(math.sqrt(a))

def adjust_ra(ra, star_ra):
    new_ra = ra + star_ra
    if new_ra > 360: new_ra -= 360
    elif new_ra < 0: new_ra += 360
    return new_ra

def adjust_dec(dec, star_dec):
    new_dec = dec - star_dec
    if new_dec > 90: new_dec -= 180
    elif new_dec < -90: new_dec += 180
    return new_dec
def filter_stars(stars, ra, dec, fov_h, fov_v):
    """Filters stars within the specified field of view."""
    filtered_stars = []
    for _, star in stars.iterrows():
        star_ra = star["ra_ep2000"]
        star_dec = star["dec_ep2000"]
        if abs(star_ra - ra) <= fov_h / 2 and abs(star_dec - dec) <= fov_v / 2:
            filtered_stars.append(star)
    return filtered_stars

def sort_stars_by_brightness(stars):
    """
     Sorts a list of stars in ascending order by their brightness using Bubble Sort.

     Parameters:
         stars (list): A list of dictionaries, each representing a star with a 'brightness' key.

     Returns:
         list: The sorted list of stars.
     """
    n = len(stars)
    for i in range(n):
        for j in range(0, n - i - 1):
            if stars[j]["brightness"] > stars[j + 1]["brightness"]:
                # Swap if the current star is dimmer than the next star
                stars[j], stars[j + 1] = stars[j + 1], stars[j]
    return stars

def top_stars(stars, n):
    """Returns first N entries of a sorted stars list."""
    return stars[:n]
def write_to_csv(stars, file_name, ra, dec):
    """Writes the stars to a CSV file."""
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "RA", "DEC", "Brightness", "AngularDifference"])
        for star in stars:
            new_ra = adjust_ra(star["ra_ep2000"], ra)
            new_dec = adjust_ra(star["ra_ep2000"], dec)
            writer.writerow([star["source_id"], new_ra, new_dec, star["brightness"], star["distance"]])

def main():
    # Input parameters
    tsv_file = "337.all.tsv"
    ra = float(input("Enter RA: "))
    dec = float(input("Enter DEC: "))
    fov_h = float(input("Enter FOV Horizontal (fov_h): "))
    fov_v = float(input("Enter FOV Vertical (fov_v): "))
    n = int(input("Enter the number of stars (N): "))

    # Parse the TSV file
    stars = parse_tsv(tsv_file)

    # phot_g_mean_mag appears to show the magnitude/apparent brightness of the star.
    stars.rename(columns={"phot_g_mean_mag": "brightness"}, inplace=True)  # Replace with the actual brightness column name from the TSV file
    stars["distance"] = [calculate_distance(ra, dec, star_ra, star_dec) for star_ra, star_dec in zip(stars["ra_ep2000"], stars["dec_ep2000"])]

    # Filter stars within the field of view
    filtered_stars = filter_stars(stars, ra, dec, fov_h, fov_v)

    # Sort stars by distance
    sorted_stars = sort_stars_by_brightness(filtered_stars)

    # Select the top N the brightest stars
    top_n_stars = sorted_stars[:n]

    # Write the result to a CSV file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"{timestamp}.csv"
    write_to_csv(top_n_stars, output_file, ra, dec)

    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
