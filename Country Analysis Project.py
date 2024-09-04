
def main(csvfile, region):
    """main function which calls calculation functions"""
    data = read_file(csvfile)
    """running each of the individual functions from the main function"""
    MaxMin = max_min(data, region)
    AvSd = average_standard_deviation(data,region)
    Densities = density(data,region)
    Corr = correlation(data,region)
    """return functions"""
    return MaxMin,AvSd,Densities,Corr


def read_file(csvfile):
    """reads file and splits data for given file"""
    data = [] 
    with open(csvfile, 'r') as file:
        file.readline()
        total_lines = file.readlines()
        for line in total_lines:
            line_info = line.strip().split(",")
            line_info[1] = float(line_info[1])
            line_info[2] = float(line_info[2])
            line_info[3] = float(line_info[3])
            line_info[4] = float(line_info[4])
            data.append(line_info)
    return data

def max_min(data, region):
    """maximum and minimum population calculation for given region"""
    max_population = float('-inf')
    max_names = []
    min_population = float('inf')
    min_names = []
    has_positive_net_change = False
    for row in data:
        name = row[0]
        population = row[1]
        net_change = row[3]
        if row[5] == region:
            if net_change > 0:
                has_positive_net_change = True
                if max_population < population:
                    max_population = population
                    max_names = [name]
                elif max_population == population:
                    max_names.append(name)
                if min_population > population:
                    min_population = population
                    min_names = [name]
                elif min_population == population:
                    min_names.append(name)
    if not has_positive_net_change:
        return []
    if len(max_names) > 1:
        max_names.sort()
    else:
        max_names = max_names[0]
    if len(min_names) > 1:
        min_names.sort()
    else:
        min_names = min_names[0]  
    return [max_names,min_names]


def average_standard_deviation(data,region):
    """average population and standard deviation calculation for given region"""
    total_population = 0
    average_population = ''
    variance = ''
    counter = 0
    region_populations = []
    for row in data:
        if row[5] == region:
            region_populations.append(row[1])
            counter += 1
            population = row[1]
            total_population += population
    if counter == 0:
        return [0, 0]
    if counter == 1:
        return [total_population,0]
    else:
        average_population = total_population/counter
        average_population = round(average_population,4)
        variance = sum((population - average_population) ** 2 for population in region_populations)/(counter-1)
        standard_deviation = variance ** (1/2)
        standard_deviation = round(standard_deviation,4)
        return[average_population,standard_deviation]


def density(data,region):
    """density calculation of countries for given region in descending order"""
    region_densities = [] 
    for row in data:
        name = row[0]
        land_area = row[4]
        population = row[1]
        if row[5] == region and land_area != 0:
            density = float(population/land_area)
            density = round(density,4)
            region_densities.append([name, density])
    region_densities.sort(key=lambda x: (-x[1], x[0]))
    return region_densities


def correlation(data, region):
    """correlation calculation for given region"""
    population = []
    land_area = []
    for row in data:
        if row[5] == region:
            population.append(float(row[1]))
            land_area.append(float(row[4]))   
    average_population = sum(population) / len(population)
    average_land_area = sum(land_area) / len(land_area)
    region_correlation = 0
    numerator = 0
    denominator_1 = 1
    denominator_2 = 1
    for index in range(len(population)):
        each_population = population[index]
        each_land_area = land_area[index]
        numerator += (each_population - average_population) * (each_land_area - average_land_area)
        denominator_1 += ((each_population - average_population) ** 2)
        denominator_2 += ((each_land_area - average_land_area) ** 2)
        denominator_total = denominator_1 * denominator_2
    if denominator_total == 0:
            return 0
    region_correlation = numerator / (denominator_total ** 0.5)
    region_correlation = round(region_correlation,4)
    return region_correlation