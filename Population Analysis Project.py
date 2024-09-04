
def main(csvfile):
    """main function which calls calculation functions"""
    data = read_file(csvfile)
    """running the individual output functions from the main function"""
    Output_1 = output1(data)
    Output_2 = output2(data)
    """return functions"""
    return Output_1, Output_2

def read_file(csvfile):
    """reads file and splits data for given file"""
    data = {}
    countries = set()
    with open(csvfile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        header = lines[0].strip().lower().split(",")
        """error avoidance - tries to calculate the index of each column to account for them being in different orders
        and if required headers aren't found returns data"""
        try:
            country_index = header.index("country")
            population_index = header.index("population")
            net_change_index = header.index("net change")
            land_area_index = header.index("land area")
            region_index = header.index("regions")
        except ValueError as error:
            print("Required headers not found.")
            return None
        for line in lines[1:]:  
            line_info = line.lower().strip().split(",")
            """error avoidance - skips line if number of values doesn't match the number of headers"""
            if len(line_info) != len(header):
                continue
            """initializes column values"""
            country = line_info[country_index].strip()
            population = int(line_info[population_index])
            net_change = int(line_info[net_change_index])
            land_area = int(line_info[land_area_index])
            region = line_info[region_index].strip().lower()
            """error avoidance - skips line if population or land area isn't positive"""
            if population <= 0 or land_area <= 0:
                continue
            """error avoidance - skips line if country or region is empty"""
            if not country or not region:
                continue
            if country in countries:
                continue
            countries.add(country)
            """error avoidance - creates empty list for region if it doesn't exist in data"""
            if region not in data:
                data[region] = []
            data[region].append([country, population, net_change, land_area])
    return data

def standard_error(country_list):
    """Calculates standard error for each given region"""
    number_countries = len(country_list)
    total_population = 0
    for row in country_list:
        population = row[1]
        total_population += population
    """error avoidance - if there are no countries in the given region it returns 0 for standard error"""
    average_population = float(total_population / number_countries)
    variance = sum((row[1] - average_population) ** 2 for row in country_list) / (number_countries - 1)
    standard_deviation = variance ** 0.5
    standard_error = standard_deviation / (number_countries ** 0.5)
    standard_error = round(standard_error, 4)
    return standard_error

def cosine_similarity(country_list):
    """Calculates the cosine similarity between population and land area for each region"""
    number_countries = len(country_list)
    """error avoidance - if there are less than two countries in the given region it returns 0 for cosine similarity"""
    if number_countries < 2:
        return 0
    absolute_region_population = 0
    absolute_region_land_area = 0
    """numerator is the sum of each country in the regions' population multiplied by its land area"""
    numerator = 0
    for row in country_list:
        population = int(row[1])
        land_area = int(row[3])
        numerator += (population * land_area)
        absolute_region_population += (int(row[1]) ** 2)
        absolute_region_land_area += (int(row[3]) ** 2)
    """denominator is sum of the absolute value of the regions total popultion and absolute value of the regions total land area"""
    denominator = (absolute_region_population ** 0.5) * (absolute_region_land_area ** 0.5)
    if denominator == 0:
        return 0
    cosine_similarity = numerator / denominator
    cosine_similarity = round(cosine_similarity, 4)
    return cosine_similarity

def output1(data):
    """returns a dictionary for the given region which includes standard error and cosine similarity calculations"""
    output_dictionary_1 = {}
    for region, country_list in data.items():
        Std_Error = standard_error(country_list)
        Cos_Similarity = cosine_similarity(country_list)
        output_dictionary_1[region] = [Std_Error,Cos_Similarity]
    return output_dictionary_1
        
def total_population(country_list):
    """calculates total population of countries in a given region"""
    total_population_sum = sum(row[1] for row in country_list)
    return total_population_sum

def population_percentage(country_info, total_pop):
    """calculates countries percentage of population in a given region"""
    population = country_info[1]
    percentage = (population / total_pop) * 100
    percentage = round(percentage, 4)
    return percentage
    
def density(country_info):
    """calculates the population densities of countries in a given region""" 
    population = country_info[1]
    land_area = country_info[3]
    density = population/land_area
    density = round(density, 4)
    return density

def output2(data):
    """returns a dictionary for each country nested within each region dictionary
    which includes population percentage, density and population rank calculations"""
    output_dictionary_2 = {}
    for region, country_list in data.items():
        country_list.sort(key=lambda x: (-x[1], x[3], x[0]))
        country_dict = {}
        total_pop = total_population(country_list)
        for i, country_info in enumerate(country_list, 1):
            country = country_info[0]
            population = country_info[1]
            net_change = country_info[2]
            land_area = country_info[3]
            pop_percentage = population_percentage(country_info, total_pop)
            pop_density = density(country_info)
            pop_rank = i
            country_dict[country] = [population,net_change,pop_percentage,pop_density,pop_rank]
        output_dictionary_2[region] = country_dict
    return output_dictionary_2
