from django.db import models

class modelselection(models.Model):
    session_id = models.CharField(max_length=36, null=True, blank=True)
    sophia_agent = models.TextField(default="True",null=True)
    weight_loss_agent = models.TextField(default="False",null=True)
    cgm_agent = models.TextField(default="False",null=True)
    dme_agent = models.TextField(default="False",null=True)

class weightlosspatient(models.Model):
    session_id = models.CharField(max_length=36, null=True, blank=True)
    name = models.CharField(max_length=255 , null=True)
    phone = models.CharField(max_length=20 , null=True)

    prescription_uploaded = models.TextField(null=True)

    delivery_method = models.CharField(
        max_length=20,
        choices=[
            ("pickup", "Pickup"),
            ("delivery_standard", "Delivery ($20)"),
            ("delivery_same_day", "Same-day Delivery ($30)")
        ],
        blank=True,
        null=True
    )

    callback_requested = models.TextField(default="False")
    callback_reason = models.TextField(blank=True, null=True)
    photo_1 = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DMEModel(models.Model):
    session_id = models.CharField(max_length=36, null=True, blank=True)
    name = models.CharField(max_length=255,null =  True)
    phone = models.CharField(max_length=20,null = True)
    item_requested = models.TextField(null=True)
    insurance_status = models.TextField(default="False")
    prescription_status = models.TextField(default="False")
    callback_requested = models.TextField(default="False")
    callback_reason = models.TextField(blank=True, null=True)
    BIN = models.TextField(null=True)
    PCN = models.TextField(null=True)
    Group = models.TextField(null = True)
    Member_ID = models.TextField(null=True)
    photo_1 = models.URLField(blank=True, null=True)
    photo_2 = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CGMLead(models.Model):
    session_id = models.CharField(max_length=36, null=True, blank=True)   
    full_name = models.CharField(max_length=255,null=True)
    date_of_birth = models.TextField(null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    has_insurance = models.TextField(default="False")
    insurance_name = models.CharField(max_length=255, blank=True, null=True)
    bin_number = models.CharField(max_length=50, blank=True, null=True)
    pcn_number = models.CharField(max_length=50, blank=True, null=True)
    group_number = models.CharField(max_length=50, blank=True, null=True)
    member_id = models.CharField(max_length=100, blank=True, null=True)
    diabetes_diagnosis = models.CharField(
        max_length=50,
        choices=[("Type 1", "Type 1"), ("Type 2", "Type 2"), ("Other", "Other")],
        blank=True,
        null=True,
    )
    on_insulin = models.TextField(default = "False")
    blood_sugar_testing_frequency = models.CharField(max_length=100, blank=True, null=True)
    hypoglycemia_history = models.TextField(null=True)
    recent_a1c = models.CharField(max_length=20, blank=True, null=True)
    has_doctor = models.TextField(default = "False")
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    doctor_phone = models.CharField(max_length=20, blank=True, null=True)
    has_prescription = models.TextField(default = "False")
    has_medical_necessity = models.TextField(default="False")
    telehealth_requested = models.TextField(default="False")
    docs_received = models.TextField(default="False")   
    needs_callback = models.TextField(default="False")
    photo_1 = models.URLField(blank=True, null=True)
    photo_2 = models.URLField(blank=True, null=True)
    photo_3 = models.URLField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SophiaLead(models.Model):

    full_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.CharField(max_length=255,null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    medication_name = models.CharField(max_length=255, null=True, blank=True)
    inquiry_type = models.CharField(
        max_length=50,
        choices=[
            ("availability", "Medication/Stock Availability"),
            ("refill", "Refill"),
            ("transfer", "Transfer"),
            ("insurance", "Insurance Inquiry"),
            ("provider", "Provider Inquiry"),
            ("other", "Other"),
        ],
        default="other"
    )

    callback_requested = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    controlled_medication = models.BooleanField(default=False)

    session_id = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ConversationHistory(models.Model):
    user = models.TextField(null = True)
    ai_message = models.TextField(null = True)
    session_id = models.CharField(max_length=36, null=True, blank=True)