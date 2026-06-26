from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .agent import *
from .models import *
from django.conf import settings

class PharmacyAgent(APIView):

    def post(self,request):

        query = request.data.get("query")
        session_id = request.data.get("session_id")
        

        response = main(query,session_id)

        return Response(str(response))
    
    def get(self, request):
        session_id = request.GET.get("session_id")
        if not session_id:
            return Response({"error": "session_id required"}, status=400)
            
        model_obj = modelselection.objects.filter(session_id=session_id).order_by("-id").first()
        if not model_obj:
            return Response({"current_bot": "sophia", "max_uploads": 0})
            
        # Determine current bot and max uploads
        if model_obj.weight_loss_agent == "True":
            current_bot = "weightloss"
            max_uploads = 1
        elif model_obj.cgm_agent == "True":
            current_bot = "cgm"
            max_uploads = 3
        elif model_obj.dme_agent == "True":
            current_bot = "dme"
            max_uploads = 2
        else:
            current_bot = "sophia"
            max_uploads = 0
            
        return Response({
            'current_bot': current_bot,
            'max_uploads': max_uploads
        })

    
class Upload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        session_id = request.data.get("session_id")
        file_obj = request.FILES.get("file")
        photo_slot = int(request.data.get("photo_slot", 1))
        
        if not session_id or not file_obj:
            return Response({"error": "session_id and file are required"}, status=400)
        
        # Get current bot type to determine patient type
        model_obj = modelselection.objects.filter(session_id=session_id).order_by("-id").first()
        if not model_obj:
            return Response({"error": "Session not found"}, status=404)
        
        # Determine patient type based on current bot
        if model_obj.weight_loss_agent == "True":
            patient_type = "weightloss"
        elif model_obj.cgm_agent == "True":
            patient_type = "cgm"
        elif model_obj.dme_agent == "True":
            patient_type = "dme"
        else:
            return Response({"error": "No upload allowed for current bot"}, status=400)
        
        response = photo_upload(file_obj, patient_type, session_id, photo_slot)
        return Response(response)


    
@method_decorator(csrf_exempt, name='dispatch')    
class Creation(APIView):

    def post(self,request):
        session_id = request.data.get("session_id")

        ConversationHistory.objects.create(session_id = session_id)

        CGMLead.objects.create(session_id=session_id)

        DMEModel.objects.create(session_id=session_id)

        weightlosspatient.objects.create(session_id=session_id)
    
        modelselection.objects.create(session_id=session_id)

        return Response()