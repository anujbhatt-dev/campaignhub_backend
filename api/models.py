import hashlib
from django.db import models
from django.core.exceptions import ValidationError


class UploadedFile(models.Model):
    name = models.CharField(max_length=40, default="NA", unique=True)
    file = models.FileField(upload_to="uploads/")
    file_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)  # Allow NULL
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Generate hash and ensure uniqueness before saving."""
        if not self.file_hash and self.file:  # Only generate hash if not already set
            self.file_hash = self.compute_file_hash()
        
        # Check uniqueness
        if UploadedFile.objects.filter(file_hash=self.file_hash).exists():
            raise ValidationError("File with the same content already exists.")

        super().save(*args, **kwargs)

    def compute_file_hash(self):
        """Compute SHA-256 hash of the file content."""
        hasher = hashlib.sha256()
        self.file.seek(0)  # Ensure we read from the beginning
        for chunk in self.file.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

class CampaignData(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name="campaign_data")
    
    client = models.CharField(max_length=255)
    group_code = models.CharField(max_length=255)
    mailing_code = models.CharField(max_length=255)
    mlg_desc = models.CharField(max_length=255)
    mail_date = models.DateField()
    offer = models.CharField(max_length=255)
    offer_desc = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    product_desc = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    mailing_list = models.CharField(max_length=255)
    segment = models.CharField(max_length=255)
    ship_qty = models.IntegerField()
    mailed = models.IntegerField()
    ror_net_percent = models.FloatField()
    
    printing_cost = models.FloatField()
    lists_cost = models.FloatField()
    postage_cost = models.FloatField()
    lettershop_cost = models.FloatField()
    dp_cost = models.FloatField()
    misc_cost = models.FloatField()
    total_mailing_cost = models.FloatField()

    mail_orders = models.IntegerField()
    phone_orders = models.IntegerField()
    web_orders = models.IntegerField()
    gross_orders = models.IntegerField()
    gross_percent = models.FloatField()
    net_orders = models.IntegerField()
    net_percent = models.FloatField()
    
    ac = models.IntegerField()
    active_subs = models.IntegerField()
    inquirers = models.IntegerField()
    backorders = models.IntegerField()
    bo_amount = models.FloatField()
    percent_with_bo = models.FloatField()
    
    prod_amount = models.FloatField()
    x_sell_amount = models.FloatField()
    misc_amount = models.FloatField()
    non_cc_amount = models.FloatField()
    cc_amount = models.FloatField()
    auto_ships = models.IntegerField()
    
    gross_sales = models.FloatField()
    refunds = models.FloatField()
    product_cost = models.FloatField()
    call_ctr = models.FloatField()
    merch_fee = models.FloatField()
    royalties = models.FloatField()
    total_cost = models.FloatField()
    net_profit_loss = models.FloatField()
    
    net_roi = models.FloatField()
    percent_breakeven = models.FloatField()
    be_orders = models.IntegerField()
    net_per_piece = models.FloatField()
    avg_order = models.FloatField()
    avg_with_autoship = models.FloatField()
    avg_turns = models.FloatField()
    
    mlg_cost = models.FloatField()
    net_pl_order = models.FloatField()
    avg_with_autoship_2 = models.FloatField()
    
    nsf_count = models.IntegerField()
    days = models.IntegerField()
    aov = models.FloatField()
    be_aov = models.FloatField()
    lt_aov = models.FloatField()
    qty_mailed = models.IntegerField()
    
    ntf_buyers = models.IntegerField()
    fe_cost = models.FloatField()
    fe_cpo = models.FloatField()
    fe_purch = models.IntegerField()
    fe_aov = models.FloatField()
    fe_roi = models.FloatField()
    subs_percent = models.FloatField()
    
    be_orders_2 = models.IntegerField()
    be_mlg_qty = models.IntegerField()
    be_cost = models.FloatField()
    be_cpo = models.FloatField()
    be_purch = models.IntegerField()
    be_aov_last = models.FloatField()
    
    tot_purch = models.IntegerField()
    tot_cost = models.FloatField()
    net_pl = models.FloatField()
    lt_roi = models.FloatField()
    pl_per_buyers = models.FloatField()
    delta = models.FloatField()
    pl_per_buyer_total = models.FloatField()
    
    action = models.CharField(max_length=255)
