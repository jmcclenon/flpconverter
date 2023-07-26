import xml.etree.ElementTree as ET

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
    waypoints = root.findall('.//ATCCreateFlightPlan/FlightPlan/Waypoints/Waypoint')

    # Open the .fms file for writing
    with open(fms_filename, 'w') as fms_file:
        # Write the header to the .fms file
        # The second line specifies the version of the .fms file format (3 in this case)
        # The third and fourth lines are required by the .fms file format but their meaning is unclear
        # The fourth line seems to be the number of waypoints minus 1
        fms_file.write("I\n3 version\n1\n{}\n".format(len(waypoints) - 1))

        # For each waypoint in the .flp file
        for i, waypoint in enumerate(waypoints):
            # Extract the identifier, latitude, longitude, and altitude of the waypoint
            ident = waypoint.find('WaypointIdent').text
            lat = float(waypoint.find('WaypointLat').text)
            lon = float(waypoint.find('WaypointLon').text)
            alt = float(waypoint.find('WaypointAltitude').text)

            # Write the waypoint to the .fms file
            # The waypoint type is set to 11 (Fix), as there is no direct mapping from the .flp waypoint type
            fms_file.write("11 {} {} {} {}\n".format(ident, alt, lat, lon))

        # Add padding lines until a total of 100 lines have been written
        # Each padding line has the waypoint type set to 0 (unused) and the identifier set to "----"
        for i in range(len(waypoints), 100):
            fms_file.write("0 ---- 0.000000 0.000000 0.000000\n")
