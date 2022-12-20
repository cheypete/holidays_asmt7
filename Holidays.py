from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import date, datetime as dt
import requests
import json

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

@dataclass
class Holiday:
    name: str
    date: dt.date
    
    def __str__(self):
        return f'{self.name}: ({self.date.strftime("%Y-%m-%d")})'

# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

@dataclass
class HolidayList:
    innerHolidays: list
           
    def addHoliday(self):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        print('Add a Holiday\n')
        print('<><><><><><><><><><><><><>\n')
        name = input('Holiday: \n')
        
        while(True): 
            date = input('Date (Ex: 2022-12-25): ')
        
            try:
                date = dt.strptime(date,'%Y-%m-%d')
                break
            except:
                print('Error: invalid format\n')
                continue
            
        holidayObj = Holiday(name, date)
        
        if isinstance(holidayObj, Holiday):
            if holidayObj not in self.innerHolidays:
                print(f'{holidayObj} has been successfully added to the system.\n')
                self.innerHolidays.append(holidayObj)
            else:
                print(f'{holidayObj} already exists in the system.\n')
        else:
            print(f'Not a holiday object.\n')
        
        return self.innerHolidays
    
    def removeHoliday(self):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        print('Remove a Holiday\n')
        print('<><><><><><><><><><><><><>\n')
        
        while(True):
            
            name = input('Holiday: \n')
            
            
            holidayCheck = self.numHolidays()
            
            self.innerHolidays = [i for i in self.innerHolidays if i.name != name]
            
            if holidayCheck > self.numHolidays():
                print(f'{name} has been successfully removed from the system.')
                break
            else:
                print(f'{name} was not found in the system.')
                continue
    
    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        try:
            with open(filelocation, 'r') as jsonfile:
                holidayjson = json.load(jsonfile)
                for i in holidayjson['holidays']:
                    date_str = i['date']
                    formatDate = dt.strptime(date_str, '%Y-%m-%d')
                    holiday = Holiday(i['name'], formatDate)
                    self.innerHolidays.append(holiday)
        except:
            print(f'Error: Could not read file.')
    
    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        print('Save Holiday List\n')
        print('<><><><><><><><><><><><><>\n')
    
        while (True):
            saveChoice = input('Do you wish to save your changes? [Y/N]: \n').upper()
        
            if saveChoice == 'Y':
                with open(filelocation + '.json', 'w') as jsonFile:    
                    holidays = {'results': []}
                    for holiday in self.innerHolidays:
                        holidays['results'].append(holiday.__dict__)
                    jsonFile.write(json.dumps(holidays, indent = 2, default = str))
                    
                print(f'Your changes have been saved to {filelocation}.json')
                break
                
            elif saveChoice == 'N':
                print(f'Canceled: Your changes were not saved')
                break
            else:
                print(f'Error: Invalid input, please enter either Y or N.')
                continue
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.
        try:
            for i in range(2020, 2025):
                url = f"https://www.timeanddate.com/holidays/us/{str(i)}?hol=9565233"
                results = requests.get(url).text
                soup = BeautifulSoup(results, 'html.parser')
            
                holidays = soup.find_all("tr", class_="showrow")
                
                for row in holidays:
                    
                    name = row.find("a").text
                    date = dt.strptime(row.find("th").text + " " + str(i), "%b %d %Y")
                    
                    self.innerHolidays.append(Holiday(name, date.date()))
        except:
            print(f"Website cannot be reached.\n")
            
        return self.innerHolidays               
    
    def viewHolidays(self):
        
        currentWeek = (dt.today().isocalendar()[1])
        currentYear = (dt.today().isocalendar()[0])

        years = [int(currentYear - 2), int(currentYear - 1), int(currentYear), int(currentYear + 1), int(currentYear + 2)]
        weeks = [x for x in range(1, 53)]

        print('View Holidays\n')
        print('<><><><><><><><><><><><><>\n')
        
        while(True):
            try:
                yearChoice = int(input('Please select a year between 2020 to 2024: '))
                if yearChoice not in years:
                    raise
                else: 
                    break
            except:
                print(f"Error: Please choose a year between 2020 to 2024.")
                continue
            
        while(True):
            try:
                weekChoice = int(input('Choose a week between 1 and 52. Enter 0 for the current week: '))
                if int(weekChoice) not in weeks and weekChoice != 0:
                    raise
                else:
                    break
            except:
                print("Error: Invalid input.")
                continue
            
        if weekChoice == 0:
            print(f"Here are all the holidays for week {currentWeek} in {currentYear}:")
            self.displayHolidaysinWeek(currentYear,currentWeek)
        elif weekChoice not in range(1, 53):
            print(f'Error: Invalid input.')
        else:
            print(type(weekChoice))
            print(type(yearChoice))
            print(f"Here are all the holidays for week {weekChoice} in {yearChoice}:")
            self.displayHolidaysinWeek(yearChoice, weekChoice)
    
    def displayHolidaysinWeek(self, year, week):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        holiList = self.filter_holidays_by_week(year, week)
        for holiday in holiList:
            print(holiday)
    
    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        week = (dt.today().isocalendar()[1])
        year = (dt.today().isocalendar()[0])
        holiList = self.filter_holidays_by_week(year, week)
        for holiday in holiList:
            print(str(holiday) + " : " + str(holiday.date))
                 
    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)
    
    def filter_holidays_by_week(self, year, week):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        results = filter(lambda x: x.date.year == year, filter(lambda x: x.date.isocalendar()[1] == week, self.innerHolidays))
        return results
    
    def exitMenu():
               
        print('Exit\n')
        print('<><><><><><><><><><><><><>\n')
        print('Any unsaved changes will be lost!')
    
        while True:
            exitChoice = str(input('Are you sure you wish to exit? [Y/N]: \n')).strip().upper()

            if exitChoice == 'Y':
                print('Farewell!\n')
                return True
            elif exitChoice not in ['Y', 'N']:
                print('Error: Please choose either Y or N.')
            else:
                print(f'Returning to menu')
                break
    
def mainMenu():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
   
    holidaylist = HolidayList([])
    holidaylist.scrapeHolidays()
    holidaylist.read_json('holidays.json')
    print('Holiday Management')
    print('<><><><><><><><><><><><><>\n')
    print(f'There are {len(holidaylist.innerHolidays)} holidays stored in the system.')

    
    while(True):
        
        menuChoice = 0
        
        print("""
        Holiday Menu
        <><><><><><>
        1. Add a Holiday
        2. Remove a Holiday
        3. Save Holiday List
        4. View Holidays
        5. Exit\n""")
        
        menuChoice = input('Choose an option (1 - 5): \n')
        if menuChoice == '1':
            holidaylist.addHoliday()
        elif menuChoice == '2':
            holidaylist.removeHoliday()
        elif menuChoice == '3':
            filelocation = input('Enter the name for the JSON file: ')
            holidaylist.save_to_json(filelocation)
        elif menuChoice == '4':
            holidaylist.viewHolidays()
        elif menuChoice == '5':
            HolidayList.exitMenu()
        else:
            print('Error: Input invalid.')
mainMenu()
