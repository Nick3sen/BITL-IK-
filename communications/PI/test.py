test = "cheese ID deo kaas"

def parse_data(data):
    # Split the data into individual components
    data_parts = data.split()
    print(data_parts)
    for i in range(len(data_parts)):
        print(data_parts[i])

parse_data(test)