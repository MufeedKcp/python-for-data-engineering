"""'Day 2: 30 Days of python programming'"""

"Declare a first name variable and assign a value to it:"
first_name = "Mufeed"

"Declare a last name variable and assign a value to it"
last_name = "kcp"

"Declare a full name variable and assign a value to it"
full_name = "Mufeed Kcp"

"Declare a country variable and assign a value to it"
country = "India"

"Declare a city variable and assign a value to it"
city = "Kannur"

"Declare an age variable and assign a value to it"
age = 21

"Declare a year variable and assign a value to it"
year = 2027

"Declare a variable is_married and assign a value to it"
is_married = False

"Declare a variable is_true and assign a value to it"
is_true = True

"Declare a variable is_light_on and assign a value to it"
is_light = True

"Declare multiple variable on one line"
education, university, collage = "BCom Fianace", "Kannur University", "Pilathara Co-op Arts & Science Collage"


"""Check the data type of all your variables using type() built-in function"""
print(type(first_name))
print(type(last_name))
print(type(full_name))
print(type(country))
print(type(city))
print(type(age))
print(type(year))
print(type(is_married))
print(type(is_light))
print(type(is_true))
print(type(education))
print(type(university))
print(type(collage))

"Using the len() built-in function, find the length of your first name"
print(len(first_name))

"Compare the length of your first name and your last name"
print(len(first_name) - len(last_name))

"Declare 5 as num_one and 4 as num_two"
num_one = 5
numm_two = 4
"Add num_one and num_two and assign the value to a variable total"
Total = num_one + numm_two 
print(Total)

"Subtract num_two from num_one and assign the value to a variable diff"
diff = num_one - numm_two 
print(diff)

"Multiply num_two and num_one and assign the value to a variable product"
product = num_one * numm_two
print(product)

"Divide num_one by num_two and assign the value to a variable division"
division = num_one / numm_two
print(division)

"Use modulus division to find num_two divided by num_one and assign the value to a variable remainder"
remainder = num_one // numm_two
print(remainder)

"Calculate num_one to the power of num_two and assign the value to a variable exp"
exp = num_one ** numm_two
print(exp)

"Find floor division of num_one by num_two and assign the value to a variable floor_division"
floor_division = num_one // numm_two
print(floor_division) 

"The radius of a circle is 30 meters."
circle = 30

"Calculate the area of a circle and assign the value to a variable name of area_of_circle"
area_of_circle = 3.14159 * (circle ** 2)
print(area_of_circle)

"Take radius as user input and calculate the area."
user = int(input("Enter radius: "))
print(3.14159 * (user ** 2))

"Use the built-in input function to get first name, last name, country and age from a user and store the value to their corresponding variable names"
user_firstname = input("Enter your first name: ")
first_name = user_firstname


user_lastname = input("Enter your last name: ")
last_name = user_lastname

user_country = input("enter your country: ")
country = user_country


user_age = int(input("enter you age: "))
age = user_age

print(first_name)
print(last_name)
print(user_country)
print(age)
