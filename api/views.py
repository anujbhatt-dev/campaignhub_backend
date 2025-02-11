import pandas as pd
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import UploadedFile, CampaignData
from .serializers import UploadedFileSerializer, CampaignDataSerializer
from django.db.models import Sum, Count
from django.db.models.functions import ExtractYear, ExtractMonth

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            self.process_data(uploaded_file)
            return Response({"message": "File uploaded and processed successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_data(self, uploaded_file):
        file_path = uploaded_file.file.path
        df = pd.read_excel(file_path)

        bulk_data = []
        for _, row in df.iterrows():
            bulk_data.append(
                CampaignData(
                    uploaded_file=uploaded_file,
                    client=row[0],
                    group_code=row[1],
                    mailing_code=row[2],
                    mlg_desc=row[3],
                    mail_date=row[4],
                    offer=row[5],
                    offer_desc=row[6],
                    product=row[7],
                    product_desc=row[8],
                    category=row[9],
                    source=row[10],
                    mailing_list=row[11],
                    segment=row[12],
                    ship_qty=row[13],
                    mailed=row[14],
                    ror_net_percent=row[15],
                    printing_cost=row[16],
                    lists_cost=row[17],
                    postage_cost=row[18],
                    lettershop_cost=row[19],
                    dp_cost=row[20],
                    misc_cost=row[21],
                    total_mailing_cost=row[22],
                    mail_orders=row[23],
                    phone_orders=row[24],
                    web_orders=row[25],
                    gross_orders=row[26],
                    gross_percent=row[27],
                    net_orders=row[28],
                    net_percent=row[29],
                    ac=row[30],
                    active_subs=row[31],
                    inquirers=row[32],
                    backorders=row[33],
                    bo_amount=row[34],
                    percent_with_bo=row[35],
                    prod_amount=row[36],
                    x_sell_amount=row[37],
                    misc_amount=row[38],
                    non_cc_amount=row[39],
                    cc_amount=row[40],
                    auto_ships=row[41],
                    gross_sales=row[42],
                    refunds=row[43],
                    product_cost=row[44],
                    call_ctr=row[45],
                    merch_fee=row[46],
                    royalties=row[47],
                    total_cost=row[48],
                    net_profit_loss=row[49],
                    net_roi=row[50],
                    percent_breakeven=row[51],
                    be_orders=row[52],
                    net_per_piece=row[53],
                    avg_order=row[54],
                    avg_with_autoship=row[55],
                    avg_turns=row[56],
                    mlg_cost=row[57],
                    net_pl_order=row[58],
                    avg_with_autoship_2=row[59],
                    nsf_count=row[60],
                    days=row[61],
                    aov=row[62],
                    be_aov=row[63],
                    lt_aov=row[64],
                    qty_mailed=row[65],
                    ntf_buyers=row[66],
                    fe_cost=row[67],
                    fe_cpo=row[68],
                    fe_purch=row[69],
                    fe_aov=row[70],
                    fe_roi=row[71],
                    subs_percent=row[72],
                    be_orders_2=row[73],
                    be_mlg_qty=row[74],
                    be_cost=row[75],
                    be_cpo=row[76],
                    be_purch=row[77],
                    be_aov_last=row[78],
                    tot_purch=row[79],
                    tot_cost=row[80],
                    net_pl=row[81],
                    lt_roi=row[82],
                    pl_per_buyers=row[83],
                    delta=row[84],
                    pl_per_buyer_total=row[85],
                    action=row[86],
                )
            )

        CampaignData.objects.bulk_create(bulk_data)

class UploadedFileListView(APIView):
    def get(self, request):
        files = UploadedFile.objects.all()
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UniqueFilterValuesView(APIView):
    def get(self, request, file_id):
        try:
            # Get all campaign data for the specific file
            campaign_data = CampaignData.objects.filter(uploaded_file_id=file_id)

            # Extract unique values and format them properly
            unique_values = [
                {"label": "Client", "options": list(campaign_data.values_list('client', flat=True).distinct())},
                {"label": "Year", "options": list(campaign_data.values_list('mail_date__year', flat=True).distinct())},
                {"label": "Campaign", "options": list(campaign_data.values_list('mailing_code', flat=True).distinct())},
                {"label": "Category", "options": list(campaign_data.values_list('category', flat=True).distinct())},
                {"label": "Offer", "options": list(campaign_data.values_list('offer', flat=True).distinct())},
                {"label": "Product", "options": list(campaign_data.values_list('product', flat=True).distinct())},
                {"label": "Source", "options": list(campaign_data.values_list('source', flat=True).distinct())},
                {"label": "Segment", "options": list(campaign_data.values_list('segment', flat=True).distinct())},
            ]


            return Response(unique_values, status=status.HTTP_200_OK)

        except CampaignData.DoesNotExist:
            return Response({"error": "No campaign data found for this file"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CampaignDataListView(APIView):
    def get(self, request):
        filters = Q()

        # Extract filters from request query parameters
        filter_params = {
            "client": "client__icontains",
            "year": "mail_date__year",
            "product": "product__icontains",
            "campaign": "mailing_code__icontains",
            "segment": "segment__icontains",
            "category": "category__icontains",
            "source": "source__icontains"
        }

        # Apply filters dynamically
        for param, field in filter_params.items():
            value = request.query_params.get(param)
            if value:
                filters &= Q(**{field: value})

        # Handle date range filtering
        days_from = request.query_params.get("days_from")
        days_to = request.query_params.get("days_to")
        if days_from and days_to:
            filters &= Q(days__gte=days_from, days__lte=days_to)

        # Filter the campaigns based on the applied filters
        campaigns = CampaignData.objects.filter(filters)
        serializer = CampaignDataSerializer(campaigns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CampaignDataDetailView(APIView):
    def get(self, request, pk):
        campaign = get_object_or_404(CampaignData, pk=pk)
        serializer = CampaignDataSerializer(campaign)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteUploadedFileView(APIView):
    def delete(self, request, pk):
        uploaded_file = get_object_or_404(UploadedFile, pk=pk)
        uploaded_file.delete()
        return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)







class AggregateMonthlyDataView(APIView):
    def get(self, request, file_id):
        try:
            # Ensure the file exists
            file_instance = UploadedFile.objects.get(pk=file_id)

            # Get all campaign records linked to this file
            campaigns = CampaignData.objects.filter(uploaded_file=file_instance)

            # Aggregate data by Year & Month
            aggregated_data = (
                campaigns.annotate(
                    year=ExtractYear('mail_date'),
                    month=ExtractMonth('mail_date')
                )
                .values('year', 'month')
                .annotate(
                    campaign_count=Count('id'),
                    shipped=Sum('ship_qty'),
                    mailed=Sum('mailed'),
                    days_since_making=Sum('days'),
                    ror_percent=Sum('ror_net_percent'),
                    mail_order=Sum('mail_orders'),
                    phone_order=Sum('phone_orders'),
                    web_order=Sum('web_orders'),
                    backorder=Sum('backorders'),
                    total_order=Sum('mail_orders') + Sum('phone_orders') + Sum('web_orders'),
                    cost=Sum('total_cost'),
                    sales=Sum('gross_sales'),
                    net_sales=Sum('net_orders'),
                    refund_count=Sum('refunds'),
                    refunds=Sum('refunds'),
                    profit=Sum('net_profit_loss'),
                    gross_orders=Sum('gross_orders'),
                )
                .order_by('-year', '-month')  # Order by most recent year/month
            )

            # Calculate refund percent after aggregation
            for data in aggregated_data:
                total_orders = data.get('total_order', 0)
                backorder = data.get('backorder', 0)
                if total_orders > 0:
                    data["refund_percent"] = (backorder / total_orders) * 100
                else:
                    data["refund_percent"] = 0

            return Response(aggregated_data, status=status.HTTP_200_OK)

        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
