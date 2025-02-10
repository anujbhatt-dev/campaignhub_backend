import re
from rest_framework import serializers
from .models import CampaignData, UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    """Serializer for handling file uploads."""

    class Meta:
        model = UploadedFile
        fields = "__all__"


class CampaignDataSerializer(serializers.ModelSerializer):
    """Serializer for sanitizing and storing campaign data."""

    def clean_number(self, value):
        """Convert comma-separated numbers (e.g., '2,431' → 2431)."""
        if isinstance(value, str):
            return int(value.replace(",", "")) if value.replace(",", "").isdigit() else None
        return value

    def clean_currency(self, value):
        """Convert currency fields (e.g., '$433.44' → 433.44)."""
        if isinstance(value, str):
            return float(value.replace("$", "").replace(",", "")) if re.match(r"^\$?\d+(\.\d+)?$", value) else None
        return value

    def clean_percentage(self, value):
        """Convert percentage fields (e.g., '99.05%' → 99.05)."""
        if isinstance(value, str):
            return float(value.replace("%", "")) if re.match(r"^\d+(\.\d+)?%$", value) else None
        return value

    def to_internal_value(self, data):
        """Sanitize data before storing in the database."""
        percentage_fields = [
            "ror_net_percent", "gross_percent", "net_percent",
            "percent_with_bo", "net_roi", "percent_breakeven",
            "subs_percent"
        ]

        currency_fields = [
            "printing_cost", "lists_cost", "postage_cost", "lettershop_cost", "dp_cost",
            "misc_cost", "total_mailing_cost", "prod_amount", "x_sell_amount",
            "misc_amount", "non_cc_amount", "cc_amount", "gross_sales", "refunds",
            "product_cost", "call_ctr", "merch_fee", "royalties", "total_cost",
            "net_profit_loss", "net_per_piece", "avg_order", "avg_with_autoship",
            "mlg_cost", "net_pl_order", "avg_with_autoship_2", "aov", "be_aov",
            "lt_aov", "fe_cost", "fe_cpo", "fe_aov", "fe_roi", "be_cost", "be_cpo",
            "be_aov", "tot_cost", "net_pl", "lt_roi", "pl_per_buyers", "delta",
            "pl_per_buyer_total"
        ]

        number_fields = [
            "ship_qty", "mailed", "mail_orders", "phone_orders", "web_orders",
            "gross_orders", "net_orders", "active_subs", "backorders",
            "be_orders", "be_orders_2", "nsf_count", "days", "qty_mailed",
            "ntf_buyers", "be_mlg_qty", "tot_purch"
        ]

        for field in percentage_fields:
            if field in data:
                data[field] = self.clean_percentage(data[field])

        for field in currency_fields:
            if field in data:
                data[field] = self.clean_currency(data[field])

        for field in number_fields:
            if field in data:
                data[field] = self.clean_number(data[field])

        return super().to_internal_value(data)

    class Meta:
        model = CampaignData
        fields = "__all__"
