from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATE_CHOICES = (
    ('ALABAMA', 'Alabama'),
    ('ALASKA', 'Alaska'),
    ('ARIZONA', 'Arizona'),
    ('ARKANSAS', 'Arkansas'),
    ('CALIFORNIA', 'California'),
    ('COLORADO', 'Colorado'),
    ('CONNECTICUT', 'Connecticut'),
    ('DELAWARE', 'Delaware'),
    ('FLORIDA', 'Florida'),
    ('GEORGIA', 'Georgia'),
    ('HAWAII', 'Hawaii'),
    ('IDAHO', 'Idaho'),
    ('ILLINOIS', 'Illinois'),
    ('INDIANA', 'Indiana'),
    ('IOWA', 'Iowa'),
    ('KANSAS', 'Kansas'),
    ('KENTUCKY', 'Kentucky'),
    ('LOUISIANA', 'Louisiana'),
    ('MAINE', 'Maine'),
    ('MARYLAND', 'Maryland'),
    ('MASSACHUSETTS', 'Massachusetts'),
    ('MICHIGAN', 'Michigan'),
    ('MINNESOTA', 'Minnesota'),
    ('MISSISSIPPI', 'Mississippi'),
    ('MISSOURI', 'Missouri'),
    ('MONTANA', 'Montana'),
    ('NEBRASKA', 'Nebraska'),
    ('NEVADA', 'Nevada'),
    ('NEW_HAMPSHIRE', 'New Hampshire'),
    ('NEW_JERSEY', 'New Jersey'),
    ('NEW_MEXICO', 'New Mexico'),
    ('NEW_YORK', 'New York'),
    ('NORTH_CAROLINA', 'North Carolina'),
    ('NORTH_DAKOTA', 'North Dakota'),
    ('OHIO', 'Ohio'),
    ('OKLAHOMA', 'Oklahoma'),
    ('OREGON', 'Oregon'),
    ('PENNSYLVANIA', 'Pennsylvania'),
    ('RHODE_ISLAND', 'Rhode Island'),
    ('SOUTH_CAROLINA', 'South Carolina'),
    ('SOUTH_DAKOTA', 'South Dakota'),
    ('TENNESSEE', 'Tennessee'),
    ('TEXAS', 'Texas'),
    ('UTAH', 'Utah'),
    ('VERMONT', 'Vermont'),
    ('VIRGINIA', 'Virginia'),
    ('WASHINGTON', 'Washington'),
    ('WEST_VIRGINIA', 'West Virginia'),
    ('WISCONSIN', 'Wisconsin'),
    ('WYOMING', 'Wyoming'),
)

class Rental(models.Model):
    state = models.CharField(blank=True, null=True, choices=STATE_CHOICES, default="CALIFORNIA", max_length=100)
    rent = models.IntegerField()
    description = models.CharField(blank=True, null=True, max_length=255)
    address = models.CharField(blank=True, null=True, max_length=255)
    building = models.BooleanField(default=False)
    lot_size = models.IntegerField(blank=True,null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    current_owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True,null=True)
    email = models.CharField(max_length=255, blank=True,null=True)
    about_description = models.TextField(max_length=255, blank=True,null=True)
    HOA_dues = models.IntegerField(blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)

    img1 = models.ImageField(blank=True,null=True, upload_to=f'uploads/')
    img2 = models.ImageField(blank=True,null=True, upload_to=f'uploads/')
    img3 = models.ImageField(blank=True,null=True, upload_to=f'uploads/')

    def __str__(self):
        return f'{self.state}, {self.address}, {self.rent}, {self.available}. ID: {self.id}'

class Tour(models.Model):
	tour_date = models.DateTimeField(blank=True,null=True)
	move_in_date = models.DateTimeField(blank=True,null=True)
	message = models.TextField(blank=True,null=True)
	rental = models.ForeignKey(Rental, on_delete=models.CASCADE, blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f'{self.rental}, {self.message}, {self.user}'

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=True)
    paid_ammount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    next_payment = models.DateTimeField()
    phone = models.CharField(blank=True, null=True, max_length=200)
    email = models.CharField(blank=True, null=True, max_length=200)

class Admin(models.Model):
    profit = models.IntegerField()