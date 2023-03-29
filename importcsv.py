import csv

def import_csv(file_path):
    """
    Imports a CSV file and returns the data as a list of dictionaries.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        A list of dictionaries representing the data in the CSV file.
    """
    data = []
    
    with open(file_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            data.append(row)
    
    return data


my_data = import_csv('csv_files/totalgodiva-Sheet1.csv')
print(my_data)