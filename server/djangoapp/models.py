from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    # Name of the car make
    name = models.CharField(max_length=100)

    # Description of the car make
    description = models.TextField()

    # Any other fields you'd like to include
    # For example, founding year of the car make
    founding_year = models.IntegerField()

    def __str__(self):
        return self.name  


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    # Many-to-One relationship to CarMake model
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # Dealer ID referring to a dealer in Cloudant database
    dealer_id = models.IntegerField()

    # Name of the car model
    name = models.CharField(max_length=100)

    # Type of the car model with limited choices
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    car_type = models.CharField(max_length=5, choices=CAR_TYPES)

    # Year of the car model
    year = models.DateField()

    # Any other fields you'd like to include
    # For example, engine type, fuel type, etc.
    engine_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.car_make} - {self.name} ({self.year.year})"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    # Fields for CarDealer model
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    # Add any other fields you want for the CarDealer model
    full_name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)  # Assuming id is the primary key
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=50)
    st = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    # Many-to-One relationship to CarDealer model
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)

    # Fields for DealerReview model
    reviewer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    dealership = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    purchase = models.CharField(max_length=100)
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=10)  # Positive, Neutral, Negative
    id = models.IntegerField(primary_key=True)  # Assuming this is the unique identifier

    def __str__(self):
        return f"{self.dealership} - {self.name}"

    def __str__(self):
        return f"{self.car_dealer} - {self.reviewer_name}"

