import xml.etree.ElementTree as ET
import logging

# Set up logging
logging.basicConfig(filename='convert.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


def convert_fpl_to_fms(fpl_filename, fms_filename):
    """
    This function converts a .fpl flight plan file to a .fms file.

    Parameters:
    fpl_filename (str): The path to the input .flp file.
    fms_filename (str): The path to the output .fms file.

    Returns:
    None
    """

    # Parse the .flp file using the xml.etree.ElementTree library
    tree = ET.parse(fpl_filename)
    root = tree.getroot()

    # Find all waypoints in the .flp file
    waypoints = root.findall(
        './/ATCCreateFlightPlan/FlightPlan/Waypoints/Waypoint')
    logging.info("Found %s waypoints", len(waypoints))

    # Open the .fms file for writing
    with open(fms_filename, 'w') as fms_file:
        fms_file.write("I\n3 version\n1\n{}\n".format(len(waypoints) - 1))

        for i, waypoint in enumerate(waypoints):
            ident = waypoint.find('WaypointIdent').text
            lat = float(waypoint.find('WaypointLat').text)
            lon = float(waypoint.find('WaypointLon').text)

            # Check for WaypointAltitude, and use a default value if it doesn't exist
            altitude = waypoint.find('WaypointAltitude')
            if altitude is not None:
                alt = float(altitude.text)
            else:
                alt = 0.0

            logging.info(
                "Writing waypoint to fms: ident=%s, alt=%s, lat=%s, lon=%s", ident, alt, lat, lon)
            fms_file.write("11 {} {} {} {}\n".format(ident, alt, lat, lon))

        for i in range(len(waypoints), 100):
            logging.info("Writing padding line to fms")
            fms_file.write("0 ---- 0.000000 0.000000 0.000000\n")
