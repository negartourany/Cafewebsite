import re
map_url = "https://www.google.com/maps/place/Trade/@51.5174476,-0.0738365,17z/data=!3m1!4b1!4m6!3m5!1s0x48761cb4ff2cd9cd:0x78e04fe516969bab!8m2!3d51.5174476!4d-0.0738365!16s%2Fg%2F1q5gpzjdx?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D"
pattern = r"(-?\d+\.\d+),(-?\d+\.\d+)"
match = re.search(pattern, map_url)
# lat = float(match[0])
# lng = float(match[1])
