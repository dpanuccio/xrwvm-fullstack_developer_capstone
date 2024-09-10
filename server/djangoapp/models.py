from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

# CarMake model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=50, blank=True)  # Optional field

    def __str__(self):
        return self.name  # Returns the name of the car make


# CarModel model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    dealer_id = models.IntegerField()  # Refers to a dealer created in the Cloudant database
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"  # Return car make and model name

# Example of creating CarMake and CarModel instances with dealer_id
def create_sample_data():
    # Create a CarMake instance
    toyota = CarMake.objects.create(name="Toyota", description="Japanese car manufacturer")
    
    # Create a CarModel instance with dealer_id set
    CarModel.objects.create(
        car_make=toyota,     # Link to CarMake
        dealer_id=101,       # Ensure dealer_id is provided
        name="Corolla",      # Model name
        type="SEDAN",        # Type of car (e.g., Sedan)
        year=2020            # Manufacturing year
    )

    ford = CarMake.objects.create(name="Ford", description="American car manufacturer")

    CarModel.objects.create(
        car_make=ford,
        dealer_id=102,
        name="Mustang",
        type="WAGON",
        year=2018
    )
