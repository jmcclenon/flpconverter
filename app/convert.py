import xml.etree.ElementTree as ET
from flask import flash, redirect, request
import logging


def convert_fpl_to_fms(fpl_filename, fms_filename):
    # Parse the .flp file using the xml.etree.ElementTree library
    try:
        tree = ET.parse(fpl_filename)
    except ET.ParseError:
        flash('Failed to parse the file. Is it a well-formed XML document?')
        return redirect(request.url)

    root = tree.getroot()

    # Find all waypoints in the .flp file
    waypoints = root.findall(
        './/ATCCreateFlightPlan/FlightPlan/Waypoints/Waypoint')
    logging.info("Found %s waypoints", len(waypoints))

    for waypoint in waypoints:
        ident = waypoint.find('WaypointIdent').text
        lat = float(waypoint.find('WaypointLat').text)
        lon = float(waypoint.find('WaypointLon').text)
        logging.info(f"Waypoint: ident={ident}, lat={lat}, lon={lon}")

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

            # Convert altitude to feet if it's in meters
            # alt = alt * 3.28084 # Uncomment this line if altitude is in meters in .fpl file

            logging.info(
                "Writing waypoint to fms: ident=%s, alt=%s, lat=%s, lon=%s", ident, alt, lat, lon)
            # Write lon, lat, alt instead of alt, lat, lon
            fms_file.write("11 {} {} {} {}\n".format(ident, lon, lat, alt))

        for i in range(len(waypoints), 100):
            logging.info("Writing padding line to fms")
            fms_file.write("0 ---- 0.000000 0.000000 0.000000\n")
